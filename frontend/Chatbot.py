import streamlit as st
import requests
from examples import get_example_queries

# Sidebar navigation for consistency
st.sidebar.title("Navigation")
pages = {
    "Home": "Home.py",
    "Recommendations": "Recommend.py",
    "Chatbot": "Chatbot.py",
    "About": "About.py"
}
selected_page = st.sidebar.radio("Go to", list(pages.keys()), index=2)
if selected_page != "Chatbot":
    import os
    os.system(f"streamlit run frontend/{pages[selected_page]}")
    st.stop()

st.title("🤖 AI Chatbot (IMDB, DuckDuckGo, Gemini)")
st.markdown("Use the sidebar to navigate between features.")


def ask_chatbot(message: str):
    """
    Send a message to the chatbot backend and return the structured response.
    Args:
        message (str): User's message.
    Returns:
        dict: Structured chatbot response.
    """
    try:
        resp = requests.post("http://localhost:8000/chatbot", json={"message": message})
        if resp.status_code == 200:
            return resp.json()
        return {"success": False, "response": None, "error": f"Error contacting chatbot. Status code: {resp.status_code}", "validation_error": None}
    except Exception as e:
        return {"success": False, "response": None, "error": f"Error contacting chatbot: {e}", "validation_error": None}

example_queries = get_example_queries()
st.markdown("**Example Queries:**")
for q in example_queries:
    st.code(q)


user_input = st.text_input("Ask me anything about movies, Netflix, or IMDB:")
if st.button("Ask"):
    if user_input.strip():
        result = ask_chatbot(user_input)
        if result.get("validation_error"):
            st.warning(f"Validation error: {result['validation_error']}")
        elif not result.get("success"):
            st.error(result.get("error") or "Unknown error.")
        else:
            st.success(result.get("response"))
    else:
        st.warning("Please enter a question.")

if st.button("Test Example Query"):
    result = ask_chatbot(example_queries[0])
    st.success(f"Example response for: {example_queries[0]}")
    if result.get("validation_error"):
        st.warning(f"Validation error: {result['validation_error']}")
    elif not result.get("success"):
        st.error(result.get("error") or "Unknown error.")
    else:
        st.success(result.get("response"))
