# NUCLEAR FIX - Completely new file to force Render deployment
# This file replaces the old embedder.py completely
# Deployment ID: NUCLEAR-FORCE-REFRESH-2024

import os
import requests
import json

def embed_chunks(chunks):
    """
    Generate embeddings for document chunks using direct HTTP requests.
    This bypasses the openai library issues completely.
    """
    # Get environment variables
    api_key = os.getenv("AZURE_OPENAI_EMBEDDING_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_EMBEDDING_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    
    print(f"🔗 Embedding Endpoint: {endpoint}")
    print(f"🔑 Embedding API Key (last 5): {api_key[-5:] if api_key else 'MISSING'}")
    print(f"🤖 Embedding Deployment: {deployment}")
    
    # Construct the API URL
    api_url = f"{endpoint}/openai/deployments/{deployment}/embeddings?api-version=2024-02-01"
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    # Prepare request body
    data = {
        "input": chunks
    }
    
    try:
        print("🚀 Making direct HTTP request to Azure OpenAI...")
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        embeddings = [item["embedding"] for item in result["data"]]
        
        print(f"✅ Successfully generated {len(embeddings)} embeddings")
        return embeddings
        
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP request failed: {e}")
        raise RuntimeError(f"Failed to generate embeddings via HTTP: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        raise RuntimeError(f"Failed to parse embedding response: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise RuntimeError(f"Failed to generate embeddings: {e}")
