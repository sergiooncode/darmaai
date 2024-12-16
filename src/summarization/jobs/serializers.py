from rest_framework import serializers

from summarization.jobs.models import SummarizationJob


class JobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummarizationJob
        fields = '__all__'


class JobSummarizedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = SummarizationJob
        fields = [
            "id"
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        with open(f"{instance.processed_file.file_path}") as fd:
            content = fd.read()
        representation["summarized_content"] = content
        return representation
