# app/services/chunker.py

def chunk_document(document: str, max_chunk_size: int = 500) -> list:
    words = document.split()
    chunks = []
    for i in range(0, len(words), max_chunk_size):
        chunk = " ".join(words[i:i + max_chunk_size])
        chunks.append(chunk.strip())
    return chunks
