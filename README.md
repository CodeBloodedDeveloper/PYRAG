
# Multi-Agent RAG System with Gemini & ChromaDB

This project is a Python-based backend for a multi-agent AI application. It uses a Retrieval-Augmented Generation (RAG) architecture to provide contextual information to different AI agent personas (CEO, CTO, CFO, CMO). The backend is built with FastAPI, uses Google's Gemini Pro for generative capabilities, and ChromaDB as a persistent vector store.

The system is designed to automatically ingest and process data from a JSON file on its first startup, making it easy to deploy and run.

## Features

-   **FastAPI Backend**: A robust and fast web server for handling API requests.
-   **Multi-Agent Personas**: Pre-configured agents (CEO, CTO, etc.) with distinct system prompts to guide their responses.
-   **Retrieval-Augmented Generation (RAG)**: Retrieves relevant text chunks from a vector database to provide context for AI-generated answers.
-   **Local Embeddings**: Uses `sentence-transformers` to generate vector embeddings locally.
-   **Persistent Vector Store**: Leverages ChromaDB to store and query document embeddings.
-   **Automatic Data Ingestion**: On the first run, the server automatically populates the vector database from a source JSON file (`sample_data/conversations.json`).

---

## 🚀 Running the Project Locally

Follow these steps to set up and run the application on your local machine.

### 1. Prerequisites

-   Python 3.8 or newer.
-   `pip` for package management.

### 2. Clone the Repository

First, clone this repository to your local machine:
```bash
git clone <your-repository-url>
cd <your-repository-directory>
````

### 3\. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment
python -m venv venv

# Activate it
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
```

### 4\. Install Dependencies

Install all the required Python packages using the `requirements.txt` file.

```bash
pip install -r requirements.txt
```

### 5\. Set Up Environment Variables

The application requires a Google Gemini API key.

1.  Create a file named `.env` in the root directory of the project.

2.  Copy the contents from `.env.example` into your new `.env` file.

3.  Add your Google Gemini API key to the `.env` file:

    ```env
    GEMINI_API_KEY="your_gemini_api_key_here"
    ```

### 6\. Run the Application

Start the FastAPI server using `uvicorn`.

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Upon the first launch, you will see logs indicating that the data is being ingested into the ChromaDB vector store, which is created in the `/tmp/chroma_store` directory. Subsequent launches will skip this step as the database will already exist.

The API will be available at `http://localhost:8000`.

-----

## 🚀 Deploying to Hugging Face Spaces

You can easily deploy this application as a public service on Hugging Face Spaces.

### 1\. Create a New Hugging Face Space

1.  Go to [huggingface.co/new-space](https://huggingface.co/new-space).
2.  Give your Space a name.
3.  Select **Docker** as the Space SDK and choose the **Blank** template.
4.  Click **Create Space**.

### 2\. Upload Project Files

Upload all the project files (including this `README.md`, `requirements.txt`, and your Python scripts) to the Hugging Face repository. You can do this via the web interface or by cloning the repo and pushing your changes.

### 3\. Create a `Dockerfile`

In your Hugging Face repository, create a new file named `Dockerfile`. See the full file content in the section below.

### 4\. Set Repository Secrets

Your Gemini API key should be stored securely as a secret, not hardcoded.

1.  In your Hugging Face Space, go to the **Settings** tab.
2.  Find the **Repository secrets** section.
3.  Click **New secret**.
4.  Enter `GEMINI_API_KEY` as the **Name**.
5.  Paste your actual API key into the **Value** field.
6.  Click **Save secret**. The Space will automatically restart and use this secret as an environment variable.

Your Space should now build and run successfully. The application will perform the one-time data ingestion and then become available for requests.

-----

## 🐳 Dockerfile

Here is the complete `Dockerfile` for deployment.

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.13-slim
# Set the working directory in the container
WORKDIR /code
# Set a writeable cache directory for sentence-transformers models
ENV SENTENCE_TRANSFORMERS_HOME=/tmp/.cache
# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt
# Install any needed packages specified in requirements.txt
# --no-cache-dir ensures we don't store unnecessary files
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
# Copy the rest of your application code into the container
COPY . /code/
# Tell the port that your app will run on
EXPOSE 7860
# Command to run your Uvicorn server.
# The app will be accessible at port 7860 within the container.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
```

```
```
