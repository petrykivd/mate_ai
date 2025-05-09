import fitz  # PyMuPDF
from fastapi import UploadFile
from typing import Optional
import asyncio

from loguru import logger


async def read_pdf_text_from_upload_file(upload_file: UploadFile) -> Optional[str]:
    contents = await upload_file.read()

    def extract_text() -> str:
        logger.debug("Start reading PDF content")
        with fitz.open(stream=contents, filetype="pdf") as doc:
            return "".join(page.get_text() for page in doc).strip()

    try:
        # TODO: Can be improved (async context)
        return await asyncio.to_thread(extract_text)
    except Exception as e:
        print(f"Failed to read PDF: {e}")
        return None
