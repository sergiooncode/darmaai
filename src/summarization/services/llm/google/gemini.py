import structlog
from django.conf import settings

import google.generativeai as genai
from google.auth.exceptions import DefaultCredentialsError

from common.exceptions import SummarizationLLMSetupException

logger = structlog.get_logger(__name__)


class GeminiLLMModel:
    def __init__(self, model_version: str = "gemini-1.5-flash"):
        genai.configure(api_key=settings.GEMINI_LLM_API_KEY)
        self._model = genai.GenerativeModel(model_version)

    def generate_content(self, prompt: str):
        response = self._model.generate_content(prompt)
        return response

    def generate_content_from_file(
            self, file_path: str,
            prompt: str = "Summarize the content in the file shared"):
        try:
            content_file = genai.upload_file(file_path)
            response = self._model.generate_content([prompt, content_file])
        except DefaultCredentialsError as e:
            logger.error("Unexpected error while setting up the LLM model")
            raise SummarizationLLMSetupException(message=str(e))
        except Exception as e:
            logger.error("Unexpected error while generating content", exc_info=e)
            return ""
        return response.text
