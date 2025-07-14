
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from backend.recommender import get_user_recommendations, get_genre_recommendations
from backend.chatbot import chat_with_bot
from backend.logging_config import get_logger


app = FastAPI()
logger = get_logger("BackendApp")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend/user/{user_id}")
def recommend_user(user_id: int, n: int = 10):
    logger.info(f"Recommendation request for user_id: {user_id}, n: {n}")
    try:
        result = get_user_recommendations(user_id, n)
        logger.info(f"Recommendations for user {user_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in recommend_user: {e}")
        return {"error": str(e)}

@app.get("/recommend/genre/{user_id}")
def recommend_genre(user_id: int):
    logger.info(f"Genre recommendation request for user_id: {user_id}")
    try:
        result = get_genre_recommendations(user_id)
        logger.info(f"Genre recommendations for user {user_id}: {result}")
        return result
    except Exception as e:
        logger.error(f"Error in recommend_genre: {e}")
        return {"error": str(e)}


@app.post("/chatbot")
async def chatbot_endpoint(request: Request):
    data = await request.json()
    user_message = data.get("message", "")
    logger.info(f"Chatbot endpoint called with message: {user_message}")
    response = chat_with_bot(user_message)
    logger.info(f"Chatbot structured response: {response}")
    return response
