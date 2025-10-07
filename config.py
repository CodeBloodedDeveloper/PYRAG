# New CODE/config.py

import os
import google.generativeai as genai # type: ignore
import streamlit as st # type: ignore

# --- New Path Logic ---
# Get the absolute path of the directory where this config.py file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ---

# This makes the code work both locally and when deployed to Streamlit
try:
    # Try to load the key from Streamlit's secrets management
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (ImportError, KeyError):
    # If not on Streamlit, load from a local .env file
    from dotenv import load_dotenv
    # Use an absolute path to find the .env file
    load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Models & Vector DB config
EMBED_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-1.5-flash-latest"
# Use an absolute path for the vector database
VECTOR_DB_DIR = os.path.join(BASE_DIR, "chroma_store")

def get_genai_client():
    if not GEMINI_API_KEY:
        st.error("GEMINI_API_KEY is not set. Please add it to your Streamlit Secrets or .env file.")
        st.stop()
    genai.configure(api_key=GEMINI_API_KEY)
    return genai