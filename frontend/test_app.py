"""
Basic tests for the Streamlit Netflix Recommendation app.
Run with: pytest test_app.py
"""

import pytest
import requests
import logging


BACKEND_URL = "http://localhost:8000"
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("TestApp")

@pytest.mark.parametrize("user_id", [1, 10, 50])
def test_recommendations_endpoint(user_id):
    logger.info(f"Testing /recommend/user/{user_id}")
    resp = requests.get(f"{BACKEND_URL}/recommend/user/{user_id}")
    logger.info(f"Response: {resp.status_code} {resp.text}")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

@pytest.mark.parametrize("user_id", [1, 10, 50])
def test_genre_recommendations_endpoint(user_id):
    logger.info(f"Testing /recommend/genre/{user_id}")
    resp = requests.get(f"{BACKEND_URL}/recommend/genre/{user_id}")
    logger.info(f"Response: {resp.status_code} {resp.text}")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_chatbot_endpoint():
    logger.info("Testing /chatbot endpoint")
    resp = requests.post(f"{BACKEND_URL}/chatbot", json={"message": "Tell me about Inception on IMDB"})
    logger.info(f"Response: {resp.status_code} {resp.text}")
    assert resp.status_code == 200
    assert "response" in resp.json()
