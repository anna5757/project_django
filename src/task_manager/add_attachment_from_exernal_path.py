from pathlib import Path
from django.core.files import File
from .models import Attachments

def add_attachment_from_external(task, name: str, file_path: str):
    with open(file_path, 'rb') as f:
        attachment = Attachments(
            name = name,
            task = task
        )
        attachment.file.save(Path(file_path).name, File(f), save=True)
    return attachment