import os
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
    print("Checking for vector database on startup...")
    # Check if the chroma_store directory exists
    if not os.path.exists(VECTOR_DB_DIR):
        print(f"Database not found at {VECTOR_DB_DIR}. Starting one-time ingestion...")
        # If it doesn't exist, run your ingestion script
        ingest_json_file()
        print("Ingestion complete. Application is ready.")
    else:
        print("Database already exists. Skipping ingestion.")
    
    # This 'yield' is where the application runs
    yield
    # Code below 'yield' would run on shutdown
    print("Application shutting down.")
# ------------------------------------
app = FastAPI()

# --- Add CORS Middleware ---
# This allows your frontend (running on any domain) to communicate with your backend.
origins = ["*"] # In production, you would restrict this to your frontend's domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, etc.)
    allow_headers=["*"], # Allows all headers
)
# -------------------------

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
