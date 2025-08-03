# COMPLETE NUCLEAR SOLUTION - New file to force Render deployment
# This file completely replaces the old llm_service.py
# Deployment ID: COMPLETE-NUCLEAR-SOLUTION-2024

import os
import requests
import json

def query_llm(prompt, context_chunks):
    """
    Query GPT-4.1 with context chunks using direct HTTP requests.
    This bypasses the openai library issues completely.
    """
    # Load environment variables
    API_KEY = os.getenv("AZURE_OPENAI_CHAT_API_KEY")
    ENDPOINT = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
    DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    print(f"🔗 Azure Endpoint: {ENDPOINT}")
    print(f"🔑 API Key (last 5): {API_KEY[-5:] if API_KEY else 'MISSING'}")
    print(f"🤖 Deployment: {DEPLOYMENT}")

    # Construct the API URL
    api_url = f"{ENDPOINT}/openai/deployments/{DEPLOYMENT}/chat/completions?api-version=2024-12-01-preview"
    
    # Prepare headers
    headers = {
        "Content-Type": "application/json",
        "api-key": API_KEY
    }
    
    # Prepare context and prompt
    context = "\n\n".join(context_chunks)
    final_prompt = f"{prompt}\n\nContext:\n{context}"
    
    # Prepare request body
    data = {
        "messages": [
            {
                "role": "user",
                "content": final_prompt
            }
        ],
        "max_tokens": 1000,
        "temperature": 0.7
    }
    
    try:
        print("🚀 Making direct HTTP request to Azure OpenAI...")
        response = requests.post(api_url, headers=headers, json=data, timeout=60)
        response.raise_for_status()
        
        result = response.json()
        answer = result["choices"][0]["message"]["content"]
        
        print("✅ Successfully generated LLM response")
        return answer
        
    except requests.exceptions.RequestException as e:
        print(f"❌ HTTP request failed: {e}")
        raise RuntimeError(f"Failed to query LLM via HTTP: {e}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        raise RuntimeError(f"Failed to parse LLM response: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise RuntimeError(f"Failed to query LLM: {e}") 