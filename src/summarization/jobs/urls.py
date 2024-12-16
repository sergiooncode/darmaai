from django.urls import path

from summarization.jobs.views import JobsViewSet, JobSummarizedContentViewSet

urlpatterns = [
    path("jobs/", JobsViewSet.as_view({"get": "list"})),
    path("jobs/<uuid:pk>/status/", JobsViewSet.as_view({"get": "retrieve"})),
    path("jobs/<uuid:pk>/summarized-content/", JobSummarizedContentViewSet.as_view({"get": "retrieve"})),
]
