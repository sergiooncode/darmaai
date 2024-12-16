import pytest
from unittest.mock import patch, mock_open

from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestJobSummarizedContentViewSet:
    def test_job_retrieved_with_summarized_content_successfully(self, job):
        with patch("builtins.open", mock_open(read_data="data")):
            client = APIClient()
            response = client.get(
                path=f"/api/jobs/{job.id}/summarized-content/"
            )

        assert response.data == {
            'id': '2dc0f455-9fa5-43e0-a928-ba6416a6b3f1',
            'summarized_content': 'data'
        }
