# embeddings.py
# Provides local embedding functions with persistent caching.
# Falls back to raising an error if sentence-transformers is not available.
from emb_cache import EmbeddingCache
import numpy as np

_model = None

def get_local_model(model_name="all-MiniLM-L6-v2"):
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except Exception as e:
            raise RuntimeError("sentence-transformers not installed. Install it or use remote embeddings.") from e
        _model = SentenceTransformer(model_name)
    return _model

def embed_documents_local(docs, batch_size=32):
    """
    Return list of embeddings (as lists) for provided docs using local model.
    """
    model = get_local_model()
    embeddings = []
    for i in range(0, len(docs), batch_size):
        batch = docs[i:i+batch_size]
        emb = model.encode(batch, show_progress_bar=False, convert_to_numpy=True)
        # convert to native Python lists for serialization compatibility with Chroma
        embeddings.extend([list(x.astype(float)) for x in emb])
    return embeddings

def embed_documents_with_cache(docs, use_local=True, batch_size=32):
    """
    Use the persistent cache to avoid re-embedding unchanged documents.
    If use_local=True, uses the local sentence-transformers model.
    """
    to_embed = []
    idxs = []
    embeddings = [None]*len(docs)
    with EmbeddingCache() as cache:
        for i, d in enumerate(docs):
            cached = cache.get(d)
            if cached is not None:
                embeddings[i] = cached
            else:
                idxs.append(i)
                to_embed.append(d)
        if to_embed:
            if use_local:
                new_embs = embed_documents_local(to_embed, batch_size=batch_size)
            else:
                raise RuntimeError("Remote embedding option not implemented in this helper. Set use_local=True or implement remote batching.")
            # persist + fill
            cache.bulk_set(to_embed, new_embs)
            for ii, e in zip(idxs, new_embs):
                embeddings[ii] = e
    return embeddings
