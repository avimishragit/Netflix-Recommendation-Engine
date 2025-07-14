"""
Example data and helper functions for testing the Netflix Recommendation Streamlit app.
"""

EXAMPLE_USER_IDS = [1, 10, 50, 100]
EXAMPLE_QUERIES = [
    "What are the best rated genres?",
    "Recommend a movie for user 1",
    "Find me a comedy movie",
    "Tell me about Inception on IMDB",
    "Who directed The Godfather?"
]

def get_example_user_ids():
    """Returns a list of example user IDs for testing."""
    return EXAMPLE_USER_IDS

def get_example_queries():
    """Returns a list of example chatbot queries for testing."""
    return EXAMPLE_QUERIES


if __name__ == "__main__":
    print("Example user IDs:", get_example_user_ids())
    print("Example queries:", get_example_queries())
