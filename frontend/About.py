import streamlit as st
import os

def load_readme(path: str) -> str:
    """
    Loads the README.md file content.
    Args:
        path (str): Path to the README.md file.
    Returns:
        str: Content of the README.md file, or error message if not found.
    """
    if not os.path.exists(path):
        return "README.md file not found."
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

st.set_page_config(page_title="About - Netflix Recommendation System")
st.title("ℹ️ About This Project")
st.markdown("Use the sidebar to navigate between features.")

# Try both relative and absolute paths for robustness
readme_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "README.md"))
readme_content = load_readme(readme_path)

st.markdown(readme_content)
