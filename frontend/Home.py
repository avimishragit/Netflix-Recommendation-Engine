import streamlit as st
import os

st.set_page_config(page_title="Netflix Recommendation System", layout="wide")

# Sidebar navigation
st.sidebar.title("Navigation")
pages = {
    "Home": "Home.py",
    "Recommendations": "Recommend.py",
    "Chatbot": "Chatbot.py",
    "About": "About.py"
}
selected_page = st.sidebar.radio("Go to", list(pages.keys()))

if selected_page != "Home":
    os.system(f"streamlit run frontend/{pages[selected_page]}")
    st.stop()

st.title("Netflix Recommendation System")
st.markdown("""
Welcome to the Netflix Recommendation System demo!

Use the sidebar to navigate between:
- Home
- Recommendations
- Chatbot
- About

Explore all features and try the example queries!
""")
