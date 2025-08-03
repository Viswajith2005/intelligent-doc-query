# app/services/vector_store.py

import chromadb
from chromadb.config import Settings
import os

# Global client and collection management
# Use persistent storage for production
persist_directory = os.getenv("CHROMA_PERSIST_DIR", ".chromadb")
client = chromadb.Client(Settings(
    persist_directory=persist_directory,
    anonymized_telemetry=False  # Disable telemetry for production
))

# Dictionary to hold collections by doc_id
collections = {}

def store_embeddings(doc_id: str, chunks: list[str], embeddings: list[list[float]]):
    """
    Store document chunks and their embeddings into ChromaDB collection.
    """
    try:
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
        print(f"✅ Stored {len(chunks)} chunks for document {doc_id}")
    except Exception as e:
        print(f"❌ Error storing embeddings: {e}")
        raise RuntimeError(f"Failed to store embeddings: {str(e)}")

def search_similar_chunks(query: str, doc_id: str, top_k: int = 5) -> list[str]:
    """
    Search for the most similar chunks in ChromaDB.
    """
    from app.services.embedder import embed_chunks

    try:
        if doc_id not in collections:
            raise ValueError(f"No document found for ID: {doc_id}")

        collection = collections[doc_id]
        query_vector = embed_chunks([query])[0]

        results = collection.query(
            query_embeddings=[query_vector],
            n_results=top_k
        )

        return results["documents"][0]
    except Exception as e:
        print(f"❌ Error searching chunks: {e}")
        # Return empty list if search fails
        return []
