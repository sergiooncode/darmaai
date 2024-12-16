import uuid

from django.db import models


class SubmittedContentFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to="./file_store/uploaded/%Y-%m-%d/")
    uploaded_on = models.DateTimeField(auto_now_add=True)


class ProcessedContentFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file_path = models.FilePathField()
    processed_on = models.DateTimeField(auto_now_add=True)

    submitted_file = models.ForeignKey(
        "content_files.SubmittedContentFile",
        null=True, on_delete=models.SET_NULL)
