# app/utils/helpers.py

import os
import uuid
import hashlib
import aiofiles
from typing import Any
from pathlib import Path
from loguru import logger

class FileManager:
    def __init__(self, upload_dir: str = "./data/uploads"):
        self.upload_dir = Path(upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_uploaded_file(self, file_content: bytes, filename: str) -> str:
        file_id = str(uuid.uuid4())
        ext = Path(filename).suffix
        unique_filename = f"{file_id}{ext}"
        file_path = self.upload_dir / unique_filename

        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(file_content)
        logger.info(f"Saved: {file_path}")
        return str(file_path)

    async def cleanup_file(self, file_path: str):
        try:
            os.remove(file_path)
            logger.info(f"Removed: {file_path}")
        except Exception as e:
            logger.warning(f"Failed cleanup: {file_path} — {e}")

    def generate_document_id(self, filename: str, content_hash: str = None) -> str:
        if content_hash:
            return hashlib.sha256(f"{filename}_{content_hash}".encode()).hexdigest()[:16]
        return str(uuid.uuid4())[:16]

class ResponseFormatter:
    @staticmethod
    def format_success_response(data: Any, message: str = "Success"):
        return {"status": "success", "message": message, "data": data}
