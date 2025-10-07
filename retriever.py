# New CODE/retriever.py
import chromadb
from config import VECTOR_DB_DIR
from embeddings import embed_documents_local

_collection = None

def get_collection():
    global _collection
    if _collection is None:
        _chroma_client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
        _collection = _chroma_client.get_or_create_collection("shark_tank_data")
    return _collection

def retrieve(query, k=5, return_digest=True):
    """
    Retrieves top-k relevant chunks and returns both structured items and a small digest string.
    """
    coll = get_collection()
    q_emb = embed_documents_local([query])[0]
    results = coll.query(query_embeddings=[q_emb], n_results=k)
    
    ids = results.get("ids", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    documents = results.get("documents", [[]])[0]

    items = []
    for i in range(len(ids)):
        items.append({
            "id": ids[i],
            "preview": documents[i],
            "metadata": metadatas[i],
            "score": distances[i]
        })

    if return_digest:
        digest_lines = []
        for it in items:
            # Correctly access the flattened metadata
            meta = it["metadata"]
            title = f"{meta.get('source_file', 'N/A')}:idx{meta.get('index', 'N/A')}-chunk{meta.get('chunk_index', 'N/A')}"
            snippet = it["preview"][:240].replace('\n', ' ')
            score = it.get("score")
            digest_lines.append(f"- {title}: {snippet} (score={score:.4f})")

        digest = "\n".join(digest_lines)
        return items, digest
    
    return items, None