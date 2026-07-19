# 🎨 AI Image Studio

A beginner-friendly Streamlit application for generating AI images using the Pollinations AI API. Create beautiful, creative images by describing what you want and customizing the art style, dimensions, and quality settings.

---

## ✨ Features

- **Prompt UI** (beginner friendly): Describe an image idea and choose an art style

> Note: Pollinations image endpoint now requires authentication in this environment. This project uses a free **no-auth** placeholder image API so the app works without keys.

- **Art Style Selection**: Choose from 5 different art styles (Realistic, Anime, Fantasy, Watercolor, Sketch)

- **Custom Dimensions**: Set custom image width and height (256 to 1024 pixels)
- **Prompt Booster**: Adds quality keywords to the prompt text
- **Inspire Me Button**: Shows random prompt ideas
- **Generate Image + Download**: Fetches an image and lets you download it as PNG
- **Error Handling**: User-friendly error messages and timeout handling
- **Real-time Feedback**: Loading spinner while generating images


---

## 🛠️ Technology Used

- **Python**: Core programming language
- **Streamlit**: Web framework for creating interactive UI
- **Requests**: HTTP library for API calls
- **Pollinations AI API**: Free AI image generation service
- **urllib.parse**: URL encoding for safe prompt transmission

---

## 📦 Installation

### Step 1: Clone or Download the Project

```bash
cd AI_IMAGE_STUDIO
```

### Step 2: Create a Virtual Environment (Recommended)

```bash
python -m venv venv
```

### Step 3: Activate Virtual Environment

**On Windows:**
```bash
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Run Commands

### Run the Application

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

---

## 📁 Project Structure

```
AI_IMAGE_STUDIO/
│
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation
```

### File Descriptions

- **app.py**: Contains all the Streamlit UI components, logic for image generation, error handling, and API integration
- **requirements.txt**: Lists Python package dependencies (streamlit, requests)
- **README.md**: This documentation file

---

## 🎓 Learning Outcomes

By completing this project, you will learn:

1. **Streamlit Basics**: How to build interactive web apps without JavaScript
2. **API Integration**: Making HTTP requests to external APIs
3. **URL Encoding**: Safely encoding user input for URLs using `urllib.parse.quote()`
4. **User Input Handling**: Working with text inputs, sliders, dropdowns, and buttons
5. **Error Handling**: Implementing try-except blocks for robust applications
6. **State Management**: Understanding how Streamlit handles user interactions
7. **Image Processing**: Downloading and displaying binary image data
8. **Code Documentation**: Writing clear comments for beginner-level projects

---


## 🌟 How to Use

1. **Enter a Prompt**: Type what you want to see in the text box (e.g., "A futuristic city")
2. **Choose Art Style**: Select your preferred art style from the dropdown
3. **Set Dimensions**: Use sliders to set image width and height
4. **Enable Prompt Booster** (Optional): Check the box to enhance image quality
5. **Click Generate Image**: Wait for the AI to create your image
6. **Download or Share**: Save your generated image as PNG

**Alternative**: Click the "🎲 Inspire Me" button to get random prompt ideas!

---

## 🎨 Example Prompts to Try

- A robot cooking pizza
- A panda riding a bicycle
- A magical forest
- A floating castle
- A cat astronaut
- A futuristic classroom
- A dragon reading books
- An underwater city

---



## 🤝 Support

If you encounter issues:

1. Make sure all dependencies are installed: `pip install -r requirements.txt`
2. Check your internet connection (API requires network access)
3. Verify Python version is 3.7 or higher: `python --version`
4. Try restarting the Streamlit app: `streamlit run app.py`

---

## 💡 Tips for Success

- Start with simple prompts before trying complex ones
- Experiment with different art styles for the same prompt
- Use the Prompt Booster for better quality results
- Higher dimensions (1024x1024) take longer but are higher quality
- The API is free but may have rate limiting, so don't spam requests

---

**Happy Creating! 🎨✨**
