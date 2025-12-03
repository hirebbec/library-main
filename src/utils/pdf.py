import io

import fitz  # type: ignore


async def extract_pdf_text(file_bytes: io.BytesIO) -> str:
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        text = ""
        for page in doc:
            text += page.get_text()
    return text
