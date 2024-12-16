import uuid

from django.db import models
from django.utils import timezone


class SummarizationJobStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", "IN_PROGRESS"
    FAILED = "FAILED", "FAILED"
    COMPLETED = "COMPLETED", "COMPLETED"


class SummarizationJob(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    status = models.CharField(
        max_length=11,
        choices=SummarizationJobStatus.choices,
        null=False,
        blank=False,
        default=SummarizationJobStatus.IN_PROGRESS,
    )
    created_at = models.DateTimeField(default=timezone.now, null=False, blank=False)
    updated_at = models.DateTimeField(auto_now_add=True)

    submitted_file = models.ForeignKey(
        "content_files.SubmittedContentFile",
        related_name="jobs_submitted_file",
        null=True, on_delete=models.SET_NULL)
    processed_file = models.ForeignKey(
        "content_files.ProcessedContentFile",
        related_name="jobs_processed_file",
        null=True, on_delete=models.SET_NULL)
