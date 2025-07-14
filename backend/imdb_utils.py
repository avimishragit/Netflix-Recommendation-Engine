
import requests
from backend.logging_config import get_logger

def search_imdb(query):
    logger = get_logger("IMDBUtils")
    # Example: Use OMDb API (http://www.omdbapi.com/) for IMDB data
    # You need to set your OMDb API key as an environment variable or config
    import os
    api_key = os.getenv('IMDB_API_KEY', 'demo')
    url = f'http://www.omdbapi.com/?apikey={api_key}&t={query}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info(f"IMDB API success for query '{query}'")
            return response.json()
        else:
            logger.error(f"IMDB API error for query '{query}': {response.status_code}")
            return {'error': 'IMDB API error'}
    except Exception as e:
        logger.error(f"Exception in search_imdb for query '{query}': {e}")
        return {'error': str(e)}
