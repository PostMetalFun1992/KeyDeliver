import pytest
from rest_framework import status

from key_deliver_app.models import Key


class TestKeyRepayer:
    def test_put(self, api_client):  # noqa: 811
        k = Key.objects.create(value='ZXCV', is_delivered=True)
        r = api_client.patch(
            '/keys_repayer/', {'id': k.id, 'value': k.value}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_200_OK

        assert r.data['is_delivered']
        assert r.data['is_repayed']

        assert k.is_delivered
        assert k.is_repayed

    @pytest.mark.parametrize('value, checked_value', [
        ('TYUI', 'valu'),
        ('valu', 'VALU'),
        ('valu', 'valU'),
    ])
    def test_put_prevent_to_repay_not_matched_key(
        self, api_client, value, checked_value
    ):  # noqa: 811
        k = Key.objects.create(value=value, is_delivered=True)
        r = api_client.patch(
            '/keys_repayer/',
            {'id': k.id, 'value': checked_value},
            format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert k.is_delivered
        assert not k.is_repayed

    def test_put_prevent_to_repay_not_delivered(self, api_client):  # noqa: 811
        k = Key.objects.create(value='TYUI')
        r = api_client.patch(
            '/keys_repayer/', {'id': k.id, 'value': k.value}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert not k.is_delivered
        assert not k.is_repayed

    def test_put_prevent_to_repay_twice(self, api_client):  # noqa: 811
        k = Key.objects.create(
            value='5432', is_delivered=True, is_repayed=True
        )
        r = api_client.patch(
            '/keys_repayer/', {'id': k.id, 'value': k.value}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert k.is_delivered
        assert k.is_repayed

    def put_prevent_to_repay_with_wrong_id(self, api_client):  # noqa: 811
        k = Key.objects.create(
            value='5432', is_delivered=True
        )
        r = api_client.patch(
            '/keys_repayer/', {'id': (k.id + 1), 'value': k.value}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert k.is_delivered
        assert not k.is_repayed
