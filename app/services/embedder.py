import os
from openai import AzureOpenAI

def embed_chunks(chunks):
    """
    Generate embeddings for document chunks.
    """
    # Create embedding client inside function to avoid module-level initialization issues
    embedding_client = AzureOpenAI(
        api_key=os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY"),
        api_version="2024-02-15-preview",
        azure_endpoint=os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
    )
    
    response = embedding_client.embeddings.create(
        model=os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT"),
        input=chunks
    )
    return [item.embedding for item in response.data]
