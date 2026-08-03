import os
from typing import Optional

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

try:
    from google import genai
except ImportError:  # pragma: no cover - dependency may be absent until install
    genai = None


def load_screen_time_data(csv_path: str = "screentime.csv") -> pd.DataFrame:
    """Load the screen-time dataset and normalize the date and minutes columns."""
    df = pd.read_csv(csv_path)
    df["Date"] = pd.to_datetime(df["Date"]).dt.strftime("%Y-%m-%d")
    df["Minutes_Used"] = pd.to_numeric(df["Minutes_Used"], errors="coerce").fillna(0).astype(int)
    return df.sort_values("Date").reset_index(drop=True)


def create_summary_text(selected_day_df: pd.DataFrame) -> str:
    """Convert the aggregate category usage into readable text."""
    if selected_day_df.empty:
        return "No data available for the selected day."

    category_totals = (
        selected_day_df.groupby("Category")["Minutes_Used"].sum().sort_values(ascending=False).reset_index()
    )
    lines = [f"{row['Category']} : {int(row['Minutes_Used'])} minutes" for _, row in category_totals.iterrows()]
    return "\n".join(lines)


def build_analysis_prompt(selected_day: str, summary_text: str, total_minutes: int, goal: int) -> str:
    """Create the analysis prompt for the Gemini coaching model."""
    return f"""You are Life-OS.
You are a brutally honest but supportive productivity coach.
Analyze today's screen-time habits for {selected_day}.

Daily summary:
{summary_text}

Daily total: {total_minutes} minutes
Goal: {goal} minutes

Do NOT simply tell the user to reduce phone usage.
Instead:
- Identify unhealthy habits.
- Identify productive habits.
- Mention strengths.
- Mention weaknesses.
- Suggest realistic offline replacements.

Examples of replacements:
Walking
Gym
Reading
Meal Preparation
Meditation
Journaling
Deep Work
Stretching

If Coding time is high, encourage it.
If Education is low, recommend learning.
If Entertainment dominates, suggest a healthier balance.

End with a motivational challenge for tomorrow.
Return the response in beautiful Markdown.
"""


def call_gemini_analysis(prompt: str) -> str:
    """Send the analysis prompt to Gemini and return the generated response."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to the .env file.")

    if genai is None:
        raise RuntimeError("The google-genai package is not installed. Run pip install -r requirements.txt")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    if hasattr(response, "text") and response.text:
        return response.text
    return str(response)


def generate_avatar_prompt(selected_day_df: pd.DataFrame, total_minutes: int, goal: int) -> str:
    """Ask Gemini to generate a short image prompt for the guilt-trip avatar."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to the .env file.")

    if genai is None:
        raise RuntimeError("The google-genai package is not installed. Run pip install -r requirements.txt")

    if total_minutes > goal:
        persona = "A tired zombie endlessly scrolling a glowing smartphone in a dark room, cinematic digital art."
    else:
        persona = "A disciplined warrior studying with books at sunrise, realistic digital illustration."

    prompt = (
        f"Generate only one short image prompt for a digital artwork. "
        f"Use this persona: {persona}"
    )

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(model="gemini-2.0-flash", contents=prompt)

    if hasattr(response, "text") and response.text:
        return response.text.strip()
    return persona


def download_avatar_image(image_url: str) -> bytes:
    """Download the generated avatar image from Pollinations."""
    response = requests.get(image_url, timeout=30)
    response.raise_for_status()
    return response.content
