# New CODE/ingest.py

import json
import uuid
import os
from embeddings import embed_documents_with_cache
from chunker import smart_chunk
from retriever import get_collection # <-- IMPORT the shared function

# --- The local ChromaDB setup is now REMOVED ---

# --- New Path Logic ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def ingest_json_file(path=os.path.join(BASE_DIR, "sample_data", "conversations.json")):
    """
    Ingests conversations.json into ChromaDB using the single, cached collection.
    """
    # Use the one and only collection from the retriever
    collection = get_collection()

    if not os.path.exists(path):
        print(f"❌ Input file not found: {path}")
        return

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    raw_docs = []
    for item in data:
        content = item.get("content")
        if not content or not content.get("title"):
            continue 

        title = content.get("title", "No Title")
        overview = content.get("overview", "")
        takeaway = content.get("takeaway", "")
        guest = content.get("podcast_details", {}).get("guest", "N/A")

        doc_text = f"Title: {title}\nGuest: {guest}\nOverview: {overview}\nTakeaway: {takeaway}"

        insights_text = ""
        for insight in content.get("key_insights", []):
            heading = insight.get("heading", "")
            points = "\n- ".join(insight.get("points", []))
            if heading and points:
                insights_text += f"\n\nInsight: {heading}\n- {points}"
        
        if insights_text:
            doc_text += insights_text

        raw_docs.append(doc_text)

    chunked_docs = []
    chunk_sources = []
    for i, d in enumerate(raw_docs):
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