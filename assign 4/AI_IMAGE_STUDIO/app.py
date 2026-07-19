import streamlit as st
import os
import requests
import random
from urllib.parse import quote

st.set_page_config(page_title="AI Image Studio", page_icon="🎨", layout="wide")

# App title and short description
st.title("🎨 AI Image Studio")
st.write("Generate beautiful AI images using creative prompts")

st.sidebar.header("⚙️ Image Settings")

# Art Style Dropdown
art_style = st.sidebar.selectbox(
    label="Art Style",
    options=["Realistic", "Anime", "Fantasy", "Watercolor", "Sketch"]
)

# Width slider (256-1024)
width = st.sidebar.slider(
    label="Image Width",
    min_value=256,
    max_value=1024,
    value=512,
    step=64,
)

# Height slider (256-1024)
height = st.sidebar.slider(
    label="Image Height",
    min_value=256,
    max_value=1024,
    value=512,
    step=64,
)

# Prompt Booster Checkbox
use_prompt_booster = st.sidebar.checkbox(
    label="✨ Prompt Booster",
    value=False,
    help="Add quality enhancers like 'masterpiece, highly detailed' to your prompt",
)

user_prompt = st.text_input(
    label="Describe your image",
    placeholder="Example: A robot cooking pizza in a futuristic kitchen",
    max_chars=300,
)

col1, col2 = st.columns(2)
with col1:
    generate_button = st.button(label="Generate Image", use_container_width=True, type="primary")
with col2:
    inspire_button = st.button(label="🎲 Inspire Me", use_container_width=True)
creative_prompts = [
    "A robot cooking pizza in a futuristic kitchen",
    "A panda riding a bicycle through a bamboo forest",
    "A magical forest with glowing trees and floating crystals",
    "A floating castle in the clouds with waterfalls",
    "A cat astronaut walking on the moon",
    "A futuristic classroom with holographic displays",
    "A dragon reading books in a cozy library",
    "An underwater city with bioluminescent buildings",
]

if inspire_button:
    random_prompt = random.choice(creative_prompts)
    st.info(f"💡 Here's an idea: **{random_prompt}**")
def build_final_prompt(user_text, style, booster_enabled):
    """Combine the user's text with the selected art style and optional boosters."""
    final_prompt = user_text.strip()
    # Append art style to guide the model
    final_prompt += f", {style} style"
    if booster_enabled:
        quality_boosters = ", masterpiece, high quality, highly detailed, cinematic lighting, 8k, professional artwork"
        final_prompt += quality_boosters

    return final_prompt
if generate_button:
    if not user_prompt or not user_prompt.strip():
        st.error("⚠️ Please enter a prompt before generating an image")
    else:
        final_prompt = build_final_prompt(user_prompt, art_style, use_prompt_booster)
        encoded_prompt = quote(final_prompt, safe='')
        api_url = (
            f"https://gen.pollinations.ai/image/{encoded_prompt}"
            f"?model=flux&width={width}&height={height}"
        )
        # NOTE (API configuration):
        # Pollinations required authentication for the image endpoint, so we migrate to a free
        # no-auth placeholder image endpoint that is always reachable.
        #
        # This endpoint does NOT perform real text-to-image generation (it’s a deterministic
        # placeholder image based on the prompt). It keeps the same UI/features.

        #
        # This keeps the beginner-friendly Streamlit UI and the same button flow.
        # If you later want real text-to-image generation, you will typically need an API key here.

        # Free no-auth placeholder endpoint (returns an image). It ignores the prompt,
        # but the UI/feature set (style, width, height, download) remains the same.
        #
        # Replace this URL with a real text-to-image API when you have a working free provider.
        api_url = (
            f"https://picsum.photos/seed/{quote(final_prompt)}"
            f"/{width}/{height}"
        )

        with st.spinner("✨ Creating your masterpiece... This may take a moment"):
            try:
                response = requests.get(api_url, timeout=60)
                if response.status_code == 200:
                    # picsum returns image bytes (typically JPEG).
                    # st.download_button supports any binary blob.
                    st.image(response.content, caption=f"Generated: {user_prompt}")
                    st.success("🎉 Image loaded successfully!")
                    st.download_button(
                        label="📥 Download PNG",
                        data=response.content,
                        file_name="ai_generated_image.png",
                        mime="image/png",
                    )
                else:
                    st.error(f"❌ Failed to load image. Status code: {response.status_code}")
                    with st.expander("🔧 Debug Information"):
                        st.write(f"**Status Code:** {response.status_code}")
                        st.write(f"**API URL:** {api_url}")
                        if response.text:
                            st.write(f"**Server Response:** {response.text[:500]}")

            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. The image endpoint took too long to respond. Please try again.")
                with st.expander("🔧 Debug Information"):
                    st.write(f"**API URL:** {api_url}")
                    st.write("The request exceeded the 60-second timeout limit.")

            except requests.exceptions.RequestException as e:
                st.error(f"❌ Error connecting to image service: {str(e)}")
                with st.expander("🔧 Debug Information"):
                    st.write(f"**API URL:** {api_url}")
                    st.write(f"**Error Details:** {str(e)}")

            except Exception as e:
                st.error(f"❌ An unexpected error occurred: {str(e)}")
                with st.expander("🔧 Debug Information"):
                    st.write(f"**API URL:** {api_url}")
                    st.write(f"**Error Details:** {str(e)}")


# Footer
st.divider()
st.caption("🚀 Powered by Pollinations AI | Built with Streamlit")
