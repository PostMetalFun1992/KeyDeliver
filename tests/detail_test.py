import pytest
from rest_framework import status

from key_deliver_app.models import Key


class TestKeyDetail:
    def test_retrieve(self, api_client):  # noqa: 811
        k = Key.objects.create(value='5678')
        Key.objects.create(value='EDGK', is_delivered=True)

        r = api_client.get(f'/keys/{k.id}/')

        assert r.status_code == status.HTTP_200_OK

        assert r.data.keys() == {'id', 'value', 'is_delivered', 'is_repayed'}

        assert r.data['id'] == k.id
        assert r.data['value'] == k.value
        assert r.data['is_delivered'] == k.is_delivered
        assert r.data['is_repayed'] == k.is_repayed


class TestKeyDetailDeliver:
    def test_patch(self, api_client):  # noqa: 811
        k = Key.objects.create(value='QWER')
        r = api_client.patch(f'/keys/{k.id}/')
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_200_OK

        assert r.data['is_delivered']
        assert not r.data['is_repayed']

        assert k.is_delivered
        assert not k.is_repayed

    def test_patch_prevent_to_inject_data(self, api_client):  # noqa: 811
        start_value = 'SDFG'
        k = Key.objects.create(value=start_value)
        r = api_client.patch(
            f'/keys/{k.id}/',
            {'value': 'bnmv', 'is_repayed': True},
            format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_200_OK

        assert r.data['value'] == start_value
        assert r.data['is_delivered']
        assert not r.data['is_repayed']

        assert k.value == start_value
        assert k.is_delivered
        assert not k.is_repayed
