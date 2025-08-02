# app/services/vector_store.py

import chromadb
from chromadb.config import Settings

# Global client and collection management
client = chromadb.Client(Settings(
    persist_directory=".chromadb"  # SQLite will store vectors here
))

# Dictionary to hold collections by doc_id
collections = {}

def store_embeddings(doc_id: str, chunks: list[str], embeddings: list[list[float]]):
    """
    Store document chunks and their embeddings into ChromaDB collection.
    """
    if doc_id not in collections:
        # Create a collection for the document
        collections[doc_id] = client.create_collection(name=doc_id)

    collection = collections[doc_id]
    
    # Add chunks with embeddings
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{doc_id}_{i}" for i in range(len(chunks))]
    )

def search_similar_chunks(query: str, doc_id: str, top_k: int = 5) -> list[str]:
    """
    Search for the most similar chunks in ChromaDB.
    """
    from app.services.embedder import embed_chunks

    if doc_id not in collections:
        raise ValueError("No document found for given ID")

    collection = collections[doc_id]
    query_vector = embed_chunks([query])[0]

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=top_k
    )

    return results["documents"][0]
