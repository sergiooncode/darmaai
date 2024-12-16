from rest_framework import serializers

from summarization.content_files.models import SubmittedContentFile, ProcessedContentFile
from summarization.jobs.tasks import summarize_file_content_task


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubmittedContentFile
        fields = ('file', 'uploaded_on',)

    #def create(self, validated_data, *kargs, **kwargs):
    #    instance = ProcessedContentFile(**validated_data)
    #    file_name_with_extension = self.context["request"].FILES["file"].name
    #    print(file_name_with_extension)
    #    print(validated_data.get("file"))
    #    file_name = file_name_with_extension.split(".")[0]
    #    summarize_file_content_task.apply_async(
    #        args=(
    #            validated_data.get("file"),
    #            file_name,
    #            instance.id
    #        )
    #    )
