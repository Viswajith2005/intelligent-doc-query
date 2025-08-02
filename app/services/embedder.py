import os
from openai import AzureOpenAI

# Create embedding client
embedding_client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY"),  # Correct key for embeddings
    api_version="2024-02-15-preview",  # ✅ stable version (not 2024-12)
    azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")  # Embedding endpoint
)

def embed_chunks(chunks):
    """
    Generate embeddings for document chunks.
    """
    response = embedding_client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),  # text-embedding-3-large
        input=chunks
    )
    return [item.embedding for item in response.data]
