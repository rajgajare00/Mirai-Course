# Life-OS – AI Wellbeing Dashboard

## Project Overview

Life-OS is a polished Streamlit dashboard that helps users reflect on their digital habits through a calm and modern analytics experience. It combines screen-time insights, category breakdowns, and AI-powered coaching to encourage healthier technology use without feeling preachy.

## Features

- Daily screen-time analytics with interactive charts
- KPI cards for total usage, most-used app, and goal status
- AI-generated wellbeing analysis using Google Gemini
- Bonus guilt-trip avatar image generation with Pollinations
- Responsive dark-themed SaaS-style dashboard experience
- Quick wellness tips and a healthy habits checklist

## Screenshots

- Screenshot 1: Dashboard overview
- Screenshot 2: AI analysis panel
- Screenshot 3: Avatar generation section

## Installation

1. Clone or download this project folder.
2. Navigate to the project directory.
3. Create a virtual environment and activate it.
4. Install the dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a file named .env using the sample below:

```env
GEMINI_API_KEY=your_google_gemini_api_key_here
```

## Running Locally

Run the app with:

```bash
streamlit run app.py
```

## Deployment on Streamlit Cloud

1. Push the project to GitHub.
2. Create a new Streamlit Cloud app.
3. Select the repository and the main file as app.py.
4. Add the GEMINI_API_KEY secret in the Streamlit Cloud environment settings.

## Folder Structure

```text
life-os-dashboard/
├── app.py
├── screentime.csv
├── requirements.txt
├── README.md
├── .env.example
├── .gitignore
├── assets/
└── utils.py
```

## Technologies Used

- Python
- Streamlit
- Pandas
- Plotly
- Google Gemini API
- python-dotenv
- Requests

## Future Improvements

- Add user authentication for personalized history
- Support weekly and monthly wellbeing summaries
- Export reports as PDF or CSV
- Integrate with real device screen-time APIs
