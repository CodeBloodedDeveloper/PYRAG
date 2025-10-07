from fastapi import FastAPI
from pydantic import BaseModel
from agents import run_agent
from fastapi.middleware.cors import CORSMiddleware # Import the CORS middleware

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