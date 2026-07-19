import streamlit as st
import requests
import random

st.title("MY AI Image Generator")


st.sidebar.header("SETTINGS")

art_style = st.sidebar.selectbox(
    "Select desired art style",
    ["Photorealistic", "Anime", "Vintage Victorian", "Sketch"]
)

magic_enhance = st.sidebar.checkbox(
    "Enable Magic Enhance",
)

surprise_prompts = [
    "A giant panda working as a barista in a cozy coffee shop",
    "A medieval knight ordering food at a modern drive-thru",
    "A floating island with waterfalls flowing into the clouds",
    "A tiny dragon sleeping inside a teacup",
    "A duck dressed as Sherlock Holmes solving a mystery"
]

width = st.sidebar.slider("Select image width", min_value=256, max_value=1024, value=768)
height = st.sidebar.slider("Select image height", min_value=256, max_value=1024, value=768)

user_prompt = st.text_input("Enter your image idea")

generate = st.button("Generate Image")
surprise = st.button("🎲 Surprise Me!")

if generate or surprise:
    if surprise:
        user_prompt = random.choice(surprise_prompts)
    if user_prompt:
        with st.spinner("Creating your artwork..."):
            full_prompt = f"{user_prompt}, use this art style: {art_style} and the image should have height:{height} and width: {width}"
            
            # Enhance the prompt for better image quality
            if magic_enhance:
                full_prompt += (
                    ", masterpiece, best quality, ultra detailed, "
                    "sharp focus, cinematic lighting, dramatic composition, "
                    "highly realistic, vibrant colors, professional photography"
                )

            url  = f"https://image.pollinations.ai/prompt/{full_prompt}?width={width}&height={height}"
            response = requests.get(url)

            if response.status_code == 200:
                # replacing the space between art style names into underscore
                clean_art_style = art_style.replace(" ", "_")

                st.success("Image Generated")
                st.image(response.content, caption=full_prompt)   #converting the binary into pixels or an actual image
                
                #adding image download button
                st.download_button(
                    label="Download your image",
                    data=response.content,
                    file_name= f"{clean_art_style}_image.png",
                    mime= "image/png"
                )
            else:
                st.error("Something happened")
    else:
        st.error("Please add an image idea first")