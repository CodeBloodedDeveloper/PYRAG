# New CODE/embeddings.py

import streamlit as st
import numpy as np

@st.cache_resource
def get_local_model(model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"):
    """
    Loads and caches the SentenceTransformer model.
    """
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise RuntimeError("sentence-transformers is not installed. Please add it to requirements.txt")
    return SentenceTransformer(model_name)

def embed_documents_local(docs, batch_size=32):
    """
    Return list of embeddings (as lists) for provided docs using local model.
    """
    model = get_local_model()
    # model.encode is a method of the SentenceTransformer object
    emb = model.encode(docs, show_progress_bar=False, convert_to_numpy=True)
    # convert to native Python lists for serialization compatibility
    return [e.tolist() for e in emb]

def embed_documents_with_cache(docs, use_local=True, batch_size=32):
    """
    Simplified function that bypasses the cache and directly embeds documents.
    This is for debugging the emb_cache.py import error.
    """
    if not use_local:
        raise NotImplementedError("This simplified version only supports local embeddings.")
    
    print(f"Embedding {len(docs)} documents directly (caching disabled).")
    return embed_documents_local(docs, batch_size=batch_size)