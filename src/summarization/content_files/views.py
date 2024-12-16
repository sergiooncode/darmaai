import uuid
from http import HTTPStatus

import structlog
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework import viewsets

from summarization.content_files.serializers import FileUploadSerializer
from summarization.jobs.tasks import summarize_file_content_task

logger = structlog.get_logger(__name__)


class FileUploadViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser,)
    serializer_class = FileUploadSerializer

    def get(self, request, *args, **kwargs):
        return Response("Upload view")

    def _get_file_uploaded_and_send_task(self, instance, request, data):
        file_name_with_extension = request.FILES["file"].name
        file_name = file_name_with_extension.split(".")[0]
        job_id = uuid.uuid4()
        summarize_file_content_task.apply_async(
            args=(
                data.get("file"),
                file_name,
                instance.id,
                job_id,
            )
        )
        data = {
            **data,
            "job_id": str(job_id)
        }
        return data

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                instance = serializer.save()
                data = self._get_file_uploaded_and_send_task(instance, request, serializer.data)
                return Response(
                    data,
                    status=status.HTTP_201_CREATED
                )
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error("Unexpected error while retrieving job", exc_info=e)
            return Response(
                {"detail": "Unexpected error when file submitted"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
