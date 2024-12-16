import os
import uuid
from datetime import datetime
from uuid import UUID

import structlog

from common.exceptions import SummarizationLLMSetupException
from summarization.content_files.models import ProcessedContentFile, SubmittedContentFile
from summarization.jobs.models import SummarizationJob, SummarizationJobStatus
from summarization.services.llm.google.gemini import GeminiLLMModel
from summarization.task_queue.worker.app import app

logger = structlog.get_logger(__name__)


def _init_llm_model_and_process_file(file_path):
    model = GeminiLLMModel()
    processed_content = model.generate_content_from_file(
        file_path=f"./{file_path}")
    return processed_content


def _generate_processed_file_and_store_content(file_name, processed_content):
    processed_file_name = f"{file_name}_processed_{uuid.uuid4()}.txt"
    processed_files_dir = f"./file_store/processed/{datetime.today().strftime('%Y-%m-%d')}"
    if not os.path.exists(processed_files_dir):
        os.makedirs(processed_files_dir)
    processed_file_path = f"{processed_files_dir}/{processed_file_name}"
    with open(processed_file_path, "w") as fd:
        fd.write(processed_content)
    return processed_file_path


@app.task(
    name="summarization.task_queue.summarize_file_content",
    retry_kwargs={"max_retries": 2},
    retry_backoff=True,
    ignore_results=True,
)
def summarize_file_content_task(
        file_path: str, file_name: str, submitted_file_id: UUID, job_id: UUID):
    job = None
    try:
        processed_file = ProcessedContentFile.objects.create(
            submitted_file_id=submitted_file_id
        )
        submitted_file = SubmittedContentFile.objects.get(pk=submitted_file_id)
        job = SummarizationJob.objects.create(
            id=job_id,
            submitted_file=submitted_file,
            processed_file=processed_file
        )
        processed_content = _init_llm_model_and_process_file(file_path)
        processed_file_path = _generate_processed_file_and_store_content(file_name, processed_content)
        processed_file.file_path = processed_file_path
        processed_file.save()

        job.status = SummarizationJobStatus.COMPLETED
        job.save()

        logger.info("File content summarized successfully")
    except FileNotFoundError as e:
        logger.error("File path provided doesn't exist", exc_info=e)
    except SummarizationLLMSetupException as e:
        logger.error(
            "Exception setting up LLM model, check you have API key configured")
    except Exception as e:
        logger.error("Unexpected error happened", exc_info=e)
    finally:
        if job and job.status != SummarizationJobStatus.COMPLETED:
            job.status = SummarizationJobStatus.FAILED
            job.save()
