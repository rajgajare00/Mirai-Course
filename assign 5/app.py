import streamlit as st
import google.generativeai as genai
import requests
import json
from gtts import gTTS
from PIL import Image
from io import BytesIO
import urllib.parse
import os

# -------------------------
# Configure Gemini
# -------------------------

API_KEY = "AQ.Ab8RN6Jbtr6j8jzgn7ULm1U4jiPIvheFLeCQQzyeY6r_TfB_kQ"



genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

@st.cache_resource
def load_model():
    return genai.GenerativeModel("gemini-flash-latest")

model = load_model()

# -------------------------
# Sidebar
# -------------------------
import urllib.parse
from PIL import Image
from io import BytesIO

try:
    prompt = urllib.parse.quote(scene["image_prompt"])

    url = f"https://image.pollinations.ai/prompt/{prompt}?width=768&height=768"

    response = requests.get(url, timeout=30)

    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        st.image(image, use_container_width=True)

except Exception:
    st.toast("Image server busy. Skipping image...")
st.sidebar.title("📖 Story Settings")


genre = st.sidebar.selectbox(
    "Story Genre",
    [
        "Fantasy",
        "Sci-Fi",
        "Mystery",
        "Adventure",
        "Horror",
        "Comedy"
    ]
)

art_style = st.sidebar.selectbox(
    "Art Style",
    [
        "Anime",
        "Photorealistic",
        "Fantasy Art",
        "Sketch",
        "Watercolor",
        "Pixel Art"
    ]
)

# -------------------------
# Session State
# -------------------------

if "story" not in st.session_state:
    st.session_state.story = []

# -------------------------
# Gemini Function
# -------------------------

def get_story(user_action):

    prompt = f"""
You are an AI Visual Novel Engine.

Genre:
{genre}

Art Style:
{art_style}

Return ONLY valid JSON.

Format:

{{
"story_text":"Narrative here",
"image_prompt":"Detailed image prompt",
"options":[
"Choice 1",
"Choice 2",
"Choice 3"
]
}}

Player Action:

{user_action}

Do not write anything outside JSON.
"""

    try:

        response = model.generate_content(prompt)

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        return json.loads(text)

    except Exception as e:

        st.error(f"Gemini Error: {e}")

        return None


# -------------------------
# Page
# -------------------------

st.title("🎮 AI Visual Novel")

st.write("Choose your own adventure!")

# -------------------------
# Start Story
# -------------------------

if len(st.session_state.story) == 0:

    if st.button("Start Story"):

        result = get_story("Start the story")

        if result:
            st.session_state.story.append(result)
            st.rerun()

# -------------------------
# Display Story
# -------------------------

for scene in st.session_state.story:

    st.markdown("---")

    st.subheader("📜 Story")

    st.write(scene["story_text"])

    # -------------------------
    # Image
    # -------------------------

    try:

        encoded_prompt = urllib.parse.quote(scene["image_prompt"])

        image_url = (
            f"https://image.pollinations.ai/prompt/{encoded_prompt}"
        )

        response = requests.get(image_url, timeout=20)

        image = Image.open(BytesIO(response.content))

        st.image(image, use_container_width=True)

    except:

        st.toast("Image server is busy, skipping visual...")

    # -------------------------
    # Audio
    # -------------------------

    try:

        filename = "story.mp3"

        tts = gTTS(scene["story_text"])

        tts.save(filename)

        audio_file = open(filename, "rb")

        st.audio(audio_file.read())

    except:

        st.toast("Audio generation failed.")

# -------------------------
# Dynamic Choices
# -------------------------

if len(st.session_state.story) > 0:

    latest = st.session_state.story[-1]

    st.markdown("---")

    st.subheader("Choose your next move")

    for option in latest["options"]:

        if st.button(option):

            result = get_story(option)

            if result:

                st.session_state.story.append(result)

                st.rerun()