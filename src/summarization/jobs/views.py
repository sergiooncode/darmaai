from http import HTTPStatus
from uuid import UUID

import structlog
from django.http import Http404
from rest_framework.generics import get_object_or_404
from rest_framework import mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets

from summarization.jobs.models import SummarizationJob
from summarization.jobs.serializers import JobsSerializer, JobSummarizedContentSerializer

logger = structlog.get_logger(__name__)


class JobsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = JobsSerializer

    def get_queryset(self):
        return SummarizationJob.objects

    def list(self, request: Request) -> Response:
        try:
            serializer = self.get_serializer(data=self.get_queryset(), many=True)
            serializer.is_valid()
            return Response(serializer.data, status=HTTPStatus.OK)
        except Exception as e:
            logger.error("Unexpected error while listing jobs", exc_info=e)
            return Response(
                {"detail": "Jobs could not be listed"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )

    def retrieve(self, request: Request, pk: UUID) -> Response:
        try:
            queryset = self.get_queryset()
            job = get_object_or_404(queryset, pk=pk)
            serializer = self.get_serializer(job)
            return Response(serializer.data, status=HTTPStatus.OK)
        except Http404 as e:
            logger.error("Job does not exist", exc_info=e)
            return Response(
                {"detail": "Job does not exist"},
                status=HTTPStatus.NOT_FOUND
            )
        except Exception as e:
            logger.error("Unexpected error while retrieving job", exc_info=e)
            return Response(
                {"detail": "Unexpected error while retrieving job"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )


class JobSummarizedContentViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = JobSummarizedContentSerializer

    def get_queryset(self):
        return SummarizationJob.objects

    def retrieve(self, request: Request, pk: UUID) -> Response:
        try:
            queryset = self.get_queryset()
            job = get_object_or_404(queryset, pk=pk)
            serializer = self.get_serializer(job)
            return Response(serializer.data, status=HTTPStatus.OK)
        except Http404 as e:
            logger.error("Job does not exist", exc_info=e)
            return Response(
                {"detail": "Job does not exist"},
                status=HTTPStatus.NOT_FOUND
            )
        except Exception as e:
            logger.error("Unexpected error while retrieving job", exc_info=e)
            return Response(
                {"detail": "Unexpected error while retrieving job"},
                status=HTTPStatus.INTERNAL_SERVER_ERROR
            )
