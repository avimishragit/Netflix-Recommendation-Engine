from langchain_community.tools import DuckDuckGoSearchRun
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
import os
from dotenv import load_dotenv

from backend.logging_config import get_logger
from backend.imdb_utils import search_imdb

# Load environment variables from .env file
load_dotenv()

# Define IMDB as a LangChain tool
def imdb_tool_func(query: str) -> str:
    """Search IMDB for movie information."""
    logger = get_logger("IMDBTool")
    try:
        result = search_imdb(query)
        logger.info(f"IMDB search for query: {query} | Result: {result}")
        return str(result)
    except Exception as e:
        logger.error(f"IMDB search failed for query '{query}': {e}")
        return f"IMDB search error: {e}"

imdb_tool = Tool(
    name="IMDB Search",
    func=imdb_tool_func,
    description="Useful for searching movie information from IMDB."
)

duckduckgo_tool = DuckDuckGoSearchRun()

# Lazy-load Gemini LLM to avoid import-time credential errors
def get_llm():
    try:
        return ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    except Exception as e:
        logger = get_logger("GeminiLLM")
        logger.error(f"Failed to initialize Gemini LLM: {e}")
        return None



def get_agent():
    llm = get_llm()
    if llm is None:
        return None
    return initialize_agent(
        [imdb_tool, duckduckgo_tool],
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False
    )



def chat_with_bot(message: str) -> dict:
    """Chat with the AI agent using LangChain, Gemini, DuckDuckGo, and IMDB.
    Returns a structured dict with keys: success, response, error (if any), validation_error (if any).
    """
    logger = get_logger("Chatbot")
    agent = get_agent()
    if not isinstance(message, str) or not message.strip():
        logger.error("Validation error: Input message must be a non-empty string.")
        return {
            "success": False,
            "response": None,
            "error": None,
            "validation_error": "Input message must be a non-empty string."
        }
    if agent is None:
        logger.error("Gemini LLM is not configured. Please set up Google credentials.")
        return {
            "success": False,
            "response": None,
            "error": "Gemini LLM is not configured. Please set up Google credentials.",
            "validation_error": None
        }
    try:
        logger.info(f"User message: {message}")
        response = agent.invoke({"input": message})
        # If the response is a dict (as with new agent API), extract 'output' or 'result'
        if isinstance(response, dict):
            logger.info(f"Agent response: {response}")
            output = response.get("output") or response.get("result") or str(response)
        else:
            logger.info(f"Agent response: {response}")
            output = str(response)
        return {
            "success": True,
            "response": output,
            "error": None,
            "validation_error": None
        }
    except Exception as e:
        logger.error(f"Chatbot error for message '{message}': {e}")
        return {
            "success": False,
            "response": None,
            "error": f"Sorry, there was an error processing your request: {e}",
            "validation_error": None
        }
