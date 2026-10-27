from datetime import datetime, timezone
from io import BytesIO

import pymupdf

from docx import Document
from fastapi import HTTPException, UploadFile

from app.modules.resume import repository


MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


async def upload_resume(file: UploadFile):
    filename = file.filename or ""

    if not filename.lower().endswith((".pdf", ".docx")):
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported",
        )

    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File size must not exceed 5 MB",
        )

    try:
        if filename.lower().endswith(".pdf"):
            with pymupdf.open(stream=content, filetype="pdf") as document:
                text = "\n".join(
                    page.get_text() for page in document
                )

        else:
            document = Document(BytesIO(content))

            paragraphs = [
                paragraph.text
                for paragraph in document.paragraphs
                if paragraph.text.strip()
            ]

            # Include text stored in document tables.
            for table in document.tables:
                for row in table.rows:
                    for cell in row.cells:
                        if cell.text.strip():
                            paragraphs.append(cell.text)

            text = "\n".join(paragraphs)

    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Unable to read the uploaded document",
        ) from exc

    if not text.strip():
        raise HTTPException(
            status_code=422,
            detail="No readable text found in the resume",
        )

    resume_data = {
        "filename": filename,
        "content": text.strip(),
        "uploaded_at": datetime.now(timezone.utc),
    }

    await repository.save_resume(resume_data)

    return resume_data


async def get_resume():
    resume = await repository.get_resume()

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found",
        )

    return resume