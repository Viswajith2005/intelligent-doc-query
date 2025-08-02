# app/services/llm_service.py

import os
from openai import AzureOpenAI

# Load environment variables
API_KEY = os.getenv("AZURE_OPENAI_CHAT_API_KEY")
ENDPOINT = os.getenv("AZURE_OPENAI_CHAT_ENDPOINT")
DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT")

print(f"🔗 Azure Endpoint: {ENDPOINT}")
print(f"🔑 API Key (last 5): {API_KEY[-5:] if API_KEY else 'MISSING'}")
print(f"🤖 Deployment: {DEPLOYMENT}")

# Azure OpenAI Client (GPT-4.1)
client = AzureOpenAI(
    api_key=API_KEY,
    api_version="2024-02-15-preview",  # ✅ stable version (not 2024-12)
    azure_endpoint=ENDPOINT
)

def query_llm(prompt, context_chunks):
    """
    Query GPT-4.1 with context chunks.
    """
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
        raise RuntimeError("Connection error to Azure OpenAI.")
