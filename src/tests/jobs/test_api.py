import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestJobSummarizedContentViewSet:
    def test_(self):
        client = APIClient()
        response = client.get(
            path="/api/jobs/2dc0f455-9fa5-43e0-a928-ba6416a6b3f1/summarized-content/"
        )

        assert response.data == {}
