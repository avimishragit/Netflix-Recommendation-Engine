import streamlit as st
import requests
from examples import get_example_user_ids

st.title("🎬 Movie Recommendations")
st.markdown("Use the sidebar to navigate between features.")


def fetch_recommendations(user_id: int):
    """
    Fetch top-N movie recommendations for a user from the backend API.

    Args:
        user_id (int): The user ID.

    Returns:
        list: List of recommended movies or None if error.
    """
    resp = requests.get(f"http://localhost:8000/recommend/user/{user_id}")
    if resp.status_code == 200:
        return resp.json()
    return {"success": False, "recommendations": None, "error": f"Status code: {resp.status_code}", "validation_error": None}


def fetch_genre_recommendations(user_id: int):
    """
    Fetch best movie per genre for a user from the backend API.

    Args:
        user_id (int): The user ID.

    Returns:
        list: List of recommendations or None if error.
    """
    resp = requests.get(f"http://localhost:8000/recommend/genre/{user_id}")
    if resp.status_code == 200:
        return resp.json()
    return {"success": False, "genre_recommendations": None, "error": f"Status code: {resp.status_code}", "validation_error": None}


example_ids = get_example_user_ids()
st.markdown("**Example User IDs:** " + ", ".join(str(uid) for uid in example_ids))
user_id = st.number_input("Enter User ID", min_value=1, step=1)

col1, col2 = st.columns(2)
with col1:
    if st.button("Get Recommendations"):
        recs = fetch_recommendations(user_id)
        if recs.get("validation_error"):
            st.warning(f"Validation error: {recs['validation_error']}")
        elif not recs.get("success"):
            st.error(recs.get("error") or "Unknown error.")
        else:
            st.success("Recommendations:")
            st.write(recs.get("recommendations"))

with col2:
    if st.button("Get Genre Recommendations"):
        genre_recs = fetch_genre_recommendations(user_id)
        if genre_recs.get("validation_error"):
            st.warning(f"Validation error: {genre_recs['validation_error']}")
        elif not genre_recs.get("success"):
            st.error(genre_recs.get("error") or "Unknown error.")
        else:
            st.success("Genre Recommendations:")
            st.write(genre_recs.get("genre_recommendations"))

if st.button("Test with Example User (ID 1)"):
    recs = fetch_recommendations(1)
    if recs.get("validation_error"):
        st.warning(f"Validation error: {recs['validation_error']}")
    elif not recs.get("success"):
        st.error(recs.get("error") or "Unknown error.")
    else:
        st.success("Example recommendations for User 1:")
        st.write(recs.get("recommendations"))
