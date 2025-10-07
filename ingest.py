# New CODE/ingest.py

import json, uuid, os
from config import VECTOR_DB_DIR
import chromadb # type: ignore
from embeddings import embed_documents_with_cache
from chunker import smart_chunk

# --- New Path Logic ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# ---

# --- ChromaDB Setup ---
client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
collection = client.get_or_create_collection("shark_tank_data")

# The function's default path now uses the absolute path
def ingest_json_file(path=os.path.join(BASE_DIR, "sample_data", "conversations.json")):
    """
    Ingests conversations.json into ChromaDB by correctly parsing its nested structure.
    """
    if not os.path.exists(path):
        print(f"❌ Input file not found: {path}")
        return
    # ... the rest of the file is unchanged ...
    # ... just make sure this function signature is updated ...

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_docs = []
    # This loop correctly parses the rich, nested JSON structure.
    for item in data:
        content = item.get("content")
        if not content or not content.get("title"):
            continue # Skip entries without content or a title

        title = content.get("title", "No Title")
        overview = content.get("overview", "")
        takeaway = content.get("takeaway", "")
        guest = content.get("podcast_details", {}).get("guest", "N/A")

        # Combine the most important parts into a single text document for embedding.
        doc_text = f"Title: {title}\nGuest: {guest}\nOverview: {overview}\nTakeaway: {takeaway}"

        # Add key insights for even richer context
        insights_text = ""
        for insight in content.get("key_insights", []):
            heading = insight.get("heading", "")
            points = "\n- ".join(insight.get("points", []))
            if heading and points:
                insights_text += f"\n\nInsight: {heading}\n- {points}"
        
        if insights_text:
            doc_text += insights_text

        raw_docs.append(doc_text)

    # Smart-chunk long documents into smaller pieces
    chunked_docs = []
    chunk_sources = []
    for i, d in enumerate(raw_docs):
        # Find the original item in the data list to get the file_name
        # This is more robust than relying on the index `i` if `raw_docs` was filtered
        original_item = next((item for item in data if item.get("content", {}).get("title") in d), None)
        
        chunks = smart_chunk(d, max_tokens=500, overlap_tokens=100)
        for c_idx, c in enumerate(chunks):
            chunked_docs.append(c)
            source_file = original_item.get("file_name", path) if original_item else path
            chunk_sources.append({"source_file": source_file, "index": i, "chunk_index": c_idx})

    if not chunked_docs:
        print("No valid documents to ingest after parsing.")
        return

    ids = [str(uuid.uuid4()) for _ in chunked_docs]
    vectors = embed_documents_with_cache(chunked_docs, use_local=True, batch_size=32)
    previews = [d[:512] for d in chunked_docs]
    metadatas = [{**src, "preview": prev} for src, prev in zip(chunk_sources, previews)]

    collection.upsert(ids=ids, embeddings=vectors, metadatas=metadatas, documents=previews)
    print(f"🚀 Ingested {len(previews)} chunk(s) into ChromaDB from {len(raw_docs)} source document(s).")