# app/services/llm_service.py

import os
from openai import AzureOpenAI

def query_llm(prompt, context_chunks):
    """
    Query GPT-4.1 with context chunks.
    """
    # Load environment variables
    API_KEY = os.getenv("AZURE_OPENAI_CHAT_API_KEY")
    ENDPOINT = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
    DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

    print(f"🔗 Azure Endpoint: {ENDPOINT}")
    print(f"🔑 API Key (last 5): {API_KEY[-5:] if API_KEY else 'MISSING'}")
    print(f"🤖 Deployment: {DEPLOYMENT}")

    # Create Azure OpenAI Client with multiple fallback attempts
    client = None
    
    # First attempt: with api_version
    try:
        client = AzureOpenAI(
            api_key=API_KEY,
            api_version="2024-02-15-preview",
            azure_endpoint=ENDPOINT
        )
        print("✅ Client initialized with api_version")
    except Exception as e:
        print(f"❌ First initialization failed: {e}")
        # Second attempt: with different api_version
        try:
            client = AzureOpenAI(
                api_key=API_KEY,
                api_version="2024-05-01",
                azure_endpoint=ENDPOINT
            )
            print("✅ Client initialized with alternative api_version")
        except Exception as e2:
            print(f"❌ Second initialization failed: {e2}")
            # Third attempt: without api_version
            try:
                client = AzureOpenAI(
                    api_key=API_KEY,
                    azure_endpoint=ENDPOINT
                )
                print("✅ Client initialized without api_version")
            except Exception as e3:
                print(f"❌ Third initialization failed: {e3}")
                raise RuntimeError(f"Failed to initialize Azure OpenAI client after 3 attempts: {e}")

    if not client:
        raise RuntimeError("Failed to initialize Azure OpenAI client")

    context = "\n\n".join(context_chunks)
    final_prompt = f"{prompt}\n\nContext:\n{context}"

    try:
        response = client.chat.completions.create(
            model=DEPLOYMENT,
            messages=[{"role": "user", "content": final_prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ LLM error: {e}")
        raise RuntimeError(f"Connection error to Azure OpenAI: {e}")
