import pandas as pd
import pickle
from backend.logging_config import get_logger
from backend.chatbot import get_llm

MOVIES_PATH = 'Data/movies.csv'
RATINGS_PATH = 'Data/ratings.csv'
MODEL_PATH = 'Model/recommendation_model.pkl'


logger = get_logger("Recommender")
try:
    movies_df = pd.read_csv(MOVIES_PATH)
    ratings_df = pd.read_csv(RATINGS_PATH)
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    logger.info("Loaded movies, ratings, and model successfully.")
except Exception as e:
    logger.error(f"Error loading data or model: {e}")
    raise

movies_df['genres'] = movies_df['genres'].str.split('|')
movies_df_expanded = movies_df.explode('genres')

def get_movie_description(title: str) -> str:
    """Get a short description of a movie using Gemini LLM."""
    llm = get_llm()
    if llm is None:
        return "Description unavailable (LLM not configured)."
    try:
        prompt = f"Give a concise, engaging description of the movie '{title}'. Limit to 2-3 sentences."
        response = llm.invoke(prompt)
        if isinstance(response, dict):
            return response.get("output") or response.get("result") or str(response)
        return str(response)
    except Exception as e:
        logger = get_logger("MovieDescription")
        logger.error(f"Failed to get description for '{title}': {e}")
        return "Description unavailable (error)."

def get_user_recommendations(user_id, n=10):
    logger.info(f"Getting recommendations for user_id={user_id}, n={n}")
    # Input validation
    if not isinstance(user_id, (int, float)) or int(user_id) != user_id or user_id <= 0:
        logger.warning(f"Validation error: user_id must be a positive integer. Got: {user_id}")
        return {
            "success": False,
            "recommendations": None,
            "error": None,
            "validation_error": "user_id must be a positive integer."
        }
    if not isinstance(n, int) or n <= 0:
        logger.warning(f"Validation error: n must be a positive integer. Got: {n}")
        return {
            "success": False,
            "recommendations": None,
            "error": None,
            "validation_error": "n must be a positive integer."
        }
    try:
        movie_ids = ratings_df['movieId'].unique()
        rated_movie_ids = ratings_df[ratings_df['userId'] == user_id]['movieId'].unique()
        unrated_movie_ids = [mid for mid in movie_ids if mid not in rated_movie_ids]
        if not unrated_movie_ids:
            logger.warning(f"No unrated movies found for user {user_id}.")
            return {
                "success": False,
                "recommendations": [],
                "error": None,
                "validation_error": "No unrated movies found for this user."
            }
        predictions = [model.predict(user_id, mid) for mid in unrated_movie_ids]
        predictions.sort(key=lambda x: x.est, reverse=True)
        top_n_movie_ids = [pred.iid for pred in predictions[:n]]
        top_n_movies = movies_df[movies_df['movieId'].isin(top_n_movie_ids)]
        # Add LLM description for each movie
        recs = []
        for movie in top_n_movies.itertuples():
            description = get_movie_description(movie.title)
            recs.append({
                "movieId": movie.movieId,
                "title": movie.title,
                "genres": movie.genres,
                "description": description
            })
        logger.info(f"Recommendations for user {user_id}: {recs}")
        return {
            "success": True,
            "recommendations": recs,
            "error": None,
            "validation_error": None
        }
    except Exception as e:
        logger.error(f"Error in get_user_recommendations: {e}")
        return {
            "success": False,
            "recommendations": None,
            "error": f"Error in get_user_recommendations: {e}",
            "validation_error": None
        }

def get_genre_recommendations(user_id, n=1):
    logger.info(f"Getting genre recommendations for user_id={user_id}, n={n}")
    # Input validation
    if not isinstance(user_id, (int, float)) or int(user_id) != user_id or user_id <= 0:
        logger.warning(f"Validation error: user_id must be a positive integer. Got: {user_id}")
        return {
            "success": False,
            "genre_recommendations": None,
            "error": None,
            "validation_error": "user_id must be a positive integer."
        }
    if not isinstance(n, int) or n <= 0:
        logger.warning(f"Validation error: n must be a positive integer. Got: {n}")
        return {
            "success": False,
            "genre_recommendations": None,
            "error": None,
            "validation_error": "n must be a positive integer."
        }
    try:
        all_movies = movies_df[['movieId', 'title']]
        rated_movies = ratings_df[ratings_df['userId'] == user_id]['movieId']
        unrated_movies = all_movies[~all_movies['movieId'].isin(rated_movies)]
        if unrated_movies.empty:
            logger.warning(f"No unrated movies found for user {user_id}.")
            return {
                "success": False,
                "genre_recommendations": [],
                "error": None,
                "validation_error": "No unrated movies found for this user."
            }
        genre_map = movies_df_expanded.set_index('movieId')['genres'].to_dict()
        predictions = []
        for movie_id in unrated_movies['movieId']:
            pred = model.predict(user_id, movie_id)
            predictions.append({'movieId': movie_id, 'pred_rating': pred.est, 'genres': genre_map.get(movie_id, [])})
        pred_df = pd.DataFrame(predictions).explode('genres')
        best_per_genre = pred_df.groupby('genres').apply(lambda x: x.nlargest(n, 'pred_rating')).reset_index(drop=True)
        result = best_per_genre[['genres', 'movieId', 'pred_rating']].to_dict(orient='records')
        logger.info(f"Genre recommendations for user {user_id}: {result}")
        return {
            "success": True,
            "genre_recommendations": result,
            "error": None,
            "validation_error": None
        }
    except Exception as e:
        logger.error(f"Error in get_genre_recommendations: {e}")
        return {
            "success": False,
            "genre_recommendations": None,
            "error": f"Error in get_genre_recommendations: {e}",
            "validation_error": None
        }
