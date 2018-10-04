from rest_framework import status


class TestKeyList:
    def test_list(self, api_client):  # noqa: 811
        response = api_client.post('/keys/')

        assert response.status_code == status.HTTP_201_CREATED
