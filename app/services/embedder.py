import os
from openai import AzureOpenAI

def embed_chunks(chunks):
    """
    Generate embeddings for document chunks.
    """
    # Create embedding client with error handling
    try:
        embedding_client = AzureOpenAI(
            api_key=os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY"),
            api_version="2024-02-15-preview",
            azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
        )
    except Exception as e:
        print(f"❌ Embedding client initialization error: {e}")
        raise RuntimeError(f"Failed to initialize embedding client: {e}")
    
    try:
        response = embedding_client.embeddings.create(
            model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
            input=chunks
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        raise RuntimeError(f"Failed to generate embeddings: {e}")
