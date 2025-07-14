# Netflix-Recommendation-Engine

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-brightgreen)](https://streamlit.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-blueviolet)](https://fastapi.tiangolo.com/)

## Overview
This project is an industry-standard Netflix-style movie recommendation system. It features a robust backend for serving recommendations and a modern, multi-page Streamlit frontend for user interaction. The system also includes an AI-powered chatbot that leverages LangChain, Gemini, DuckDuckGo search, and IMDB data for rich conversational experiences.

## Features
- **Personalized Movie Recommendations:**
  - Get top-N movie recommendations for any user.
  - Find the best movie for a user in every genre.
- **Data Exploration:**
  - Explore most popular and most liked genres.
  - Visualize data distributions and statistics.
- **AI Chatbot:**
  - Ask questions about movies, genres, and recommendations.
  - Integrates LangChain, Gemini LLM, DuckDuckGo search, and IMDB API.
- **Modern Frontend:**
  - Multi-page Streamlit app: Home, Recommendations, Chatbot, About.
  - Clean, user-friendly interface with example queries and test buttons.
- **Backend API:**
  - FastAPI backend serving recommendations and chatbot responses.

## Project Structure
```
Netflix_recommendation/
│
├── backend/
│   ├── app.py                # FastAPI backend
│   ├── recommender.py        # Recommendation logic
│   ├── chatbot.py            # Chatbot logic
│   ├── imdb_utils.py         # IMDB API utilities
│   └── requirements.txt      # Backend dependencies
│
├── frontend/
│   ├── Home.py               # Streamlit Home page
│   ├── Recommend.py          # Recommendations page
│   ├── Chatbot.py            # Chatbot page
│   ├── About.py              # About page (shows this README)
│   ├── examples.py           # Example queries and user IDs
│   ├── test_app.py           # API tests (pytest)
│   └── requirements.txt      # Frontend dependencies
│
├── Data/
│   ├── movies.csv
│   └── ratings.csv
│
├── Model/
│   └── recommendation_model.pkl
│
├── .env                      # API keys and secrets
└── README.md
```

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repo-url>
cd Netflix_recommendation
```

### 2. Set Up Python Environments
- Create and activate a virtual environment for both backend and frontend (recommended: Python 3.8+).
- Install dependencies:
  - Backend: `pip install -r backend/requirements.txt`
  - Frontend: `pip install -r frontend/requirements.txt`

### 3. Configure API Keys
- Edit the `.env` file and add your OMDB and Gemini API keys:
  ```env
  IMDB_API_KEY=your_imdb_api_key_here
  GEMINI_API_KEY=your_gemini_api_key_here
  ```

### 4. Prepare Data and Model
- Place your `movies.csv` and `ratings.csv` in the `Data/` directory.
- The trained model (`recommendation_model.pkl`) should be in the `Model/` directory.

### 5. Run the Backend
```bash
uvicorn backend.app:app --reload
```

### 6. Run the Frontend
```bash
streamlit run frontend/Home.py
```
- Use the sidebar to navigate between Home, Recommendations, Chatbot, and About pages.
- Try the example user IDs and queries provided on each page.

## API Endpoints
- `GET /recommend/user/{user_id}`: Get top-N recommendations for a user.
- `GET /recommend/genre/{user_id}`: Get best movie per genre for a user.
- `POST /chatbot`: Chatbot endpoint (expects JSON `{ "message": "..." }`).

## Chatbot Capabilities
- Movie and genre Q&A
- IMDB lookups
- DuckDuckGo web search
- Gemini LLM-powered conversation

## Testing
- Basic API tests are provided in `frontend/test_app.py` (requires `pytest`).
- Run tests with:
  ```bash
  cd frontend
  pytest test_app.py
  ```

## Customization
- Update the model or retrain as needed.
- Extend the chatbot with more tools or APIs.
- Add more Streamlit pages or visualizations as desired.

## License
MIT License

## Authors
- Avinash Mishra
- Contributors welcome!
