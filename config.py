import os
import google.generativeai as genai
from dotenv import load_dotenv

# Get the absolute path of the directory where this config.py file is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load environment variables from a .env file
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Models & Vector DB config
EMBED_MODEL = "models/embedding-001"
CHAT_MODEL = "gemini-2.0-flash"
# Use an absolute path for the vector database
VECTOR_DB_DIR = os.path.join(BASE_DIR, "chroma_store")

def get_genai_client():
    """
    Initializes and returns the Generative AI client.
    """
    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not set. Please add it to your .env file.")
    genai.configure(api_key=GEMINI_API_KEY)
    return genai