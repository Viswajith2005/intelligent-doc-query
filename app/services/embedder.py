import os
from openai import AzureOpenAI

def embed_chunks(chunks):
    """
    Generate embeddings for document chunks.
    """
    # Get environment variables
    api_key = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    
    print(f"🔗 Embedding Endpoint: {endpoint}")
    print(f"🔑 Embedding API Key (last 5): {api_key[-5:] if api_key else 'MISSING'}")
    print(f"🤖 Embedding Deployment: {deployment}")
    
    # Set API version as environment variable to avoid proxies issue
    os.environ["OPENAI_API_VERSION"] = "2024-02-01"
    
    # Create embedding client with minimal configuration
    try:
        embedding_client = AzureOpenAI(
            api_key=api_key,
            azure_endpoint=endpoint
        )
        print("✅ Embedding client initialized successfully")
    except Exception as e:
        print(f"❌ Embedding client initialization failed: {e}")
        raise RuntimeError(f"Failed to initialize embedding client: {e}")
    
    try:
        response = embedding_client.embeddings.create(
            model=deployment,
            input=chunks
        )
        return [item.embedding for item in response.data]
    except Exception as e:
        print(f"❌ Embedding generation error: {e}")
        raise RuntimeError(f"Failed to generate embeddings: {e}")
