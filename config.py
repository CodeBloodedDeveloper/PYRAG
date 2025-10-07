# New CODE/config.py

import os
import google.generativeai as genai

# This makes the code work both locally and when deployed to Streamlit
try:
    # Try to load the key from Streamlit's secrets management
    import streamlit as st
    GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
except (ImportError, KeyError):
    # If not on Streamlit, load from a local .env file
    from dotenv import load_dotenv
    load_dotenv()
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Models & Vector DB config
EMBED_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-1.5-flash-latest"
VECTOR_DB_DIR = "./chroma_store"

def get_genai_client():
    if not GEMINI_API_KEY:
        raise RuntimeError("❌ GEMINI_API_KEY missing. For local use, set it in .env. For Streamlit, add it to Secrets.")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai