from django.urls import path, include
from rest_framework import routers
from summarization.content_files.views import FileUploadViewSet
from summarization.jobs.views import JobsViewSet

router = routers.DefaultRouter()
router.register(r'upload', FileUploadViewSet, basename="upload")
router.register(r'jobs', JobsViewSet, basename="jobs")

urlpatterns = [
    path("", include(router.urls)),
    path("api/", include("summarization.content_files.urls")),
    path("api/", include("summarization.jobs.urls")),
]
