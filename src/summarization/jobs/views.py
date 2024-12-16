from http import HTTPStatus
from uuid import UUID

import structlog
from django.http import Http404
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from summarization.jobs.models import SummarizationJob
from summarization.jobs.serializers import JobsSerializer, JobSummarizedContentSerializer

logger = structlog.get_logger(__name__)


class JobsViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    serializer_class = JobsSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return SummarizationJob.objects

    def list(self, request: Request) -> Response:
        try:
            queryset = SummarizationJob.objects.all()
            page = self.paginate_queryset(queryset)

            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
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
