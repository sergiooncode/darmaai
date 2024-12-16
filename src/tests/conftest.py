import pytest

from summarization.content_files.models import ProcessedContentFile, SubmittedContentFile
from summarization.jobs.models import SummarizationJob


@pytest.fixture
def submitted_file():
    submitted_file_id = "b48af157-6731-4a8c-8595-2b637e99c141"
    return SubmittedContentFile.objects.create(
        id=submitted_file_id
    )


@pytest.fixture
def processed_file():
    processed_file_id = "0e8e0633-44b1-4521-b8a7-809cf6c473bf"
    return ProcessedContentFile.objects.create(
        id=processed_file_id,
        file_path="/path/to/file/processed_file.txt"
    )


@pytest.fixture
def job(submitted_file, processed_file):
    job_id = "2dc0f455-9fa5-43e0-a928-ba6416a6b3f1"
    return SummarizationJob.objects.create(
            id=job_id,
            submitted_file=submitted_file,
            processed_file=processed_file
        )