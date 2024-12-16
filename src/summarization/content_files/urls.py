from django.urls import path

from summarization.content_files.views import FileUploadViewSet

urlpatterns = [
    path("upload/", FileUploadViewSet.as_view({"post": "create"})),
]
