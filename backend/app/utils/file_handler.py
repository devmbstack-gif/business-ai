import os
import uuid
from pathlib import Path

from fastapi import UploadFile

from app.config.settings import get_settings

settings = get_settings()


async def save_upload_file(file: UploadFile) -> str:
    upload_path = Path(settings.upload_dir)
    upload_path.mkdir(parents=True, exist_ok=True)

    extension = Path(file.filename or "screenshot.png").suffix or ".png"
    filename = f"{uuid.uuid4().hex}{extension}"
    file_path = upload_path / filename

    content = await file.read()
    max_size = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_size:
        raise ValueError(f"File size exceeds {settings.max_upload_size_mb}MB limit")

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    return str(file_path)


def delete_file(file_path: str) -> None:
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
