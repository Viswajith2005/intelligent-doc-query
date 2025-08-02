# app/models/schemas.py

from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query: str
    answer: str
    evaluation: str
    execution_time_seconds: float

class ChunkedDocument(BaseModel):
    document_id: str
    chunks: List[str]
