# app.py

import os
import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from pydantic import BaseModel
from agents import run_agent
from fastapi.middleware.cors import CORSMiddleware

# --- IMPORTS FOR STARTUP INGESTION ---
from ingest import ingest_json_file
from config import VECTOR_DB_DIR
# ------------------------------------

# --- LIFESPAN FUNCTION TO RUN ON STARTUP ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    This function runs once when the application starts.
    It checks if the vector database exists and ingests data if it doesn't.
    """
    print("--- Application starting up... ---")
    try:
        # Check if the chroma_store directory exists
        if not os.path.exists(VECTOR_DB_DIR) or not os.listdir(VECTOR_DB_DIR):
            print(f"Database not found or empty at {VECTOR_DB_DIR}.")
            print("--- Starting one-time data ingestion... ---")
            
            # If it doesn't exist, run your ingestion script
            ingest_json_file()
            
            print("--- Ingestion complete. Application is ready. ---")
        else:
            print("--- Database found. Skipping ingestion. ---")
    except Exception as e:
        # If any error occurs during startup, log it and exit.
        print(f"FATAL: An error occurred during startup ingestion: {e}", file=sys.stderr)
        # You might want to exit if ingestion is critical and fails
        # sys.exit(1)

    # This 'yield' is where the application runs
    yield
    # Code below 'yield' would run on shutdown
    print("--- Application shutting down. ---")
# ------------------------------------


# Initialize the FastAPI app with the lifespan manager
app = FastAPI(lifespan=lifespan)

# --- Add CORS Middleware ---
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------

# ... (the rest of your app.py remains the same) ...
class QueryRequest(BaseModel):
    role: str
    query: str

@app.get("/")
def root():
    return {"message": "✅ Multi-agent AI backend running"}

@app.post("/ask")
def ask_post(request: QueryRequest):
    result = run_agent(request.role, request.query)
    return result

@app.get("/ask/{role}")
def ask_get(role: str, query: str):
    result = run_agent(role, query)
    return result
