import os
from datetime import datetime
from urllib.parse import quote
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv

# ── FIX #2: load_dotenv() must run BEFORE `from utils import ...` ───────────
# utils.py reads GEMINI_API_KEY when it's imported / when its functions are
# defined at module scope, so the .env file has to be loaded first, otherwise
# utils gets a None key and keeps using it even after you fix the .env path
# (Python only imports a module once, then reuses it).
load_dotenv(dotenv_path=Path(__file__).parent / ".env", override=True)

from utils import (
    build_analysis_prompt,
    call_gemini_analysis,
    create_summary_text,
    download_avatar_image,
    generate_avatar_prompt,
    load_screen_time_data,
)

# ── FIX #3: st.set_page_config() must be the FIRST Streamlit command ────────
# Nothing else from `st` can run before this call, or Streamlit throws
# "set_page_config() can only be called once and must be the first command."
st.set_page_config(page_title="Life-OS | AI Wellbeing Dashboard", page_icon="🧠", layout="wide")

# ── FIX: removed the raw API key debug line (st.write("API Key:", ...)) ─────
# Never print a real API key to the screen/logs — use a safe boolean check
# instead if you need to confirm it loaded.
if not os.getenv("GEMINI_API_KEY"):
    st.sidebar.warning("⚠️ GEMINI_API_KEY not found — check your .env file.", icon="⚠️")

st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #07111f 0%, #101c33 100%);
        color: #f8fafc;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
    }
    .hero-card {
        background: rgba(15, 23, 42, 0.88);
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 18px;
        padding: 1.2rem 1.4rem;
        box-shadow: 0 12px 35px rgba(0, 0, 0, 0.25);
    }
    .metric-card {
        background: rgba(15, 23, 42, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 16px;
        padding: 0.85rem 1rem;
    }
    .stSidebar {
        background: #020617;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def render_dashboard():
    """Render the full Life-OS dashboard experience."""
    df = load_screen_time_data("screentime.csv")

    if df.empty:
        st.error("No screen-time data is available. Please check the CSV dataset.")
        return

    dates = sorted(df["Date"].unique().tolist())

    st.sidebar.header("Life-OS")
    st.sidebar.markdown("AI Wellbeing Dashboard")
    st.sidebar.markdown("---")

    selected_day = st.sidebar.selectbox(
        "Select Day",
        options=dates,
        format_func=lambda value: datetime.strptime(value, "%Y-%m-%d").strftime("%b %d, %Y"),
    )
    goal = st.sidebar.slider("Daily Goal (minutes)", min_value=60, max_value=600, value=240, step=30)

    st.sidebar.markdown("### Theme")
    st.sidebar.info("🌙 Dark mode • Calm analytics • AI coaching")
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"📅 Current date: {datetime.now().strftime('%b %d, %Y')}")
    st.sidebar.markdown(f"🗓️ Total tracked days: {len(dates)}")

    selected_day_df = df[df["Date"] == selected_day].copy()

    if selected_day_df.empty:
        st.warning("No data exists for the selected day.")
        return

    total_minutes = int(selected_day_df["Minutes_Used"].sum())
    top_app_series = selected_day_df.groupby("App_Name")["Minutes_Used"].sum().sort_values(ascending=False)
    top_app_name = top_app_series.index[0] if not top_app_series.empty else "No data"
    top_app_minutes = int(top_app_series.iloc[0]) if not top_app_series.empty else 0

    goal_delta = total_minutes - goal
    goal_status = "Over goal" if goal_delta > 0 else "On track"
    delta_text = f"{abs(goal_delta)} min over goal" if goal_delta > 0 else f"{abs(goal_delta)} min under goal"
    delta_color = "inverse" if goal_delta > 0 else "normal"

    st.markdown(
        """
        <div class="hero-card">
            <h1 style="margin-bottom:0.2rem;">Life-OS</h1>
            <p style="margin-top:0; color:#cbd5e1;">AI wellbeing dashboard with calm, reflective analytics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Today's Total Screen Time", f"{total_minutes} min", delta=delta_text, delta_color=delta_color)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Most Used App", f"{top_app_name}", delta=f"{top_app_minutes} min")
        st.markdown("</div>", unsafe_allow_html=True)

    with col3:
        st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
        st.metric("Goal Status", goal_status, delta=f"Goal: {goal} min")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("")

    trend_df = df.groupby("Date", as_index=False)["Minutes_Used"].sum()
    trend_fig = px.line(
        trend_df,
        x="Date",
        y="Minutes_Used",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#7c3aed"],
    )
    trend_fig.update_layout(
        title="Daily Screen Time Trend",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title="Date",
        yaxis_title="Minutes",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    if selected_day in trend_df["Date"].values:
        trend_fig.add_vline(x=selected_day, line_dash="dash", line_color="#f59e0b", annotation_text="Selected day")

    category_df = selected_day_df.groupby("Category", as_index=False)["Minutes_Used"].sum().sort_values("Minutes_Used", ascending=False)
    category_fig = px.bar(
        category_df,
        x="Category",
        y="Minutes_Used",
        color="Category",
        color_discrete_sequence=px.colors.sequential.Magma,
    )
    category_fig.update_layout(
        title="Category Distribution",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    app_df = selected_day_df.groupby("App_Name", as_index=False)["Minutes_Used"].sum().sort_values("Minutes_Used", ascending=False)
    app_fig = px.bar(
        app_df.head(8),
        x="Minutes_Used",
        y="App_Name",
        orientation="h",
        color="App_Name",
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    app_fig.update_layout(
        title="Top Apps Used",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    pie_fig = px.pie(
        category_df,
        values="Minutes_Used",
        names="Category",
        hole=0.45,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    pie_fig.update_layout(
        title="Category Pie Chart",
        template="plotly_dark",
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(trend_fig, use_container_width=True)
        st.plotly_chart(category_fig, use_container_width=True)
    with chart_col2:
        st.plotly_chart(app_fig, use_container_width=True)
        st.plotly_chart(pie_fig, use_container_width=True)

    st.markdown("---")
    st.subheader("AI Analysis")

    summary_text = create_summary_text(selected_day_df)
    prompt = build_analysis_prompt(selected_day, summary_text, total_minutes, goal)

    with st.spinner("Life-OS is reflecting on your habits..."):
        try:
            ai_response = call_gemini_analysis(prompt)
        except Exception as exc:
            ai_response = (
                f"Gemini analysis is temporarily unavailable. {exc}\n\n"
                "Please verify your GEMINI_API_KEY in the .env file and try again."
            )

    if total_minutes < goal:
        st.info(ai_response)
    else:
        st.warning(ai_response)

    with st.expander("🔍 AI reasoning details"):
        st.markdown(f"**Selected Day:** {selected_day}")
        st.markdown(f"**Summary:**\n{summary_text}")
        st.code(prompt, language="text")

    st.markdown("### Quick Wellness Tips")
    tips = [
        "🚶 Walk for 15 minutes after lunch to reset your focus.",
        "🧘 Practice 5 minutes of meditation before your next deep work block.",
        "📚 Replace one scrolling session with a chapter of reading.",
        "🏋️ Pair your next break with light stretching or a short workout.",
    ]
    for tip in tips:
        st.markdown(f"- {tip}")

    st.markdown("### Healthy Daily Habits Checklist")
    habits = [
        "Hydrate before starting work",
        "Take a real lunch break",
        "Keep phone notifications minimal",
        "Protect one focus block without distractions",
        "Log off at a consistent time",
    ]
    for index, habit in enumerate(habits):
        st.checkbox(habit, value=False, key=f"habit_{index}")

    st.markdown("---")
    st.subheader("Guilt-Trip Avatar")
    try:
        image_prompt = generate_avatar_prompt(selected_day_df, total_minutes, goal)
        image_url = f"https://image.pollinations.ai/prompt/{quote(image_prompt)}"
        image_bytes = download_avatar_image(image_url)
        st.image(image_bytes, caption=image_prompt, use_container_width=True)
    except Exception as exc:
        st.caption(f"Avatar generation is unavailable right now: {exc}")

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center; color:#94a3b8; margin-top:2rem;'>Built by <strong>RAJ</strong> for the MirAI School of Technology Virtual Summer Internship Assignment 7.</div>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    render_dashboard()
