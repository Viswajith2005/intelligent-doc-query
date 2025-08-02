# tests/test_services.py

from app.services.chunker import chunk_document
from app.services.embedder import embed_chunks
from app.services.vector_store import store_embeddings, search_similar_chunks

def test_chunker():
    text = "This is a sample document text to test chunking." * 30
    chunks = chunk_document(text, max_chunk_size=50)
    assert isinstance(chunks, list)
    assert len(chunks) > 0

def test_embedder():
    chunks = ["Test embedding chunk"]
    embeddings = embed_chunks(chunks)
    assert isinstance(embeddings, list)
    assert len(embeddings) == 1

def test_vector_store_search():
    chunks = ["Test vector store chunk"]
    embeddings = embed_chunks(chunks)
    store_embeddings("doc1", chunks, embeddings)
    results = search_similar_chunks("vector", "doc1", top_k=1)
    assert isinstance(results, list)
    assert len(results) > 0
