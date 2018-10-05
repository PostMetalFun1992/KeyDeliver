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


class TestKeyDetailRepay:
    def test_put(self, api_client):  # noqa: 811
        k = Key.objects.create(value='ZXCV', is_delivered=True)
        r = api_client.put(
            f'/keys/{k.id}/', {'value': k.value}, format='json'
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
        r = api_client.put(
            f'/keys/{k.id}/', {'value': checked_value}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert k.is_delivered
        assert not k.is_repayed

    def test_put_prevent_to_repay_not_delivered(self, api_client):  # noqa: 811
        k = Key.objects.create(value='TYUI')
        r = api_client.put(
            f'/keys/{k.id}/', {'value': k.value}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert not k.is_delivered
        assert not k.is_repayed

    def test_put_prevent_to_repay_twice(self, api_client):  # noqa: 811
        k = Key.objects.create(
            value='5432', is_delivered=True, is_repayed=True
        )
        r = api_client.put(
            f'/keys/{k.id}/', {'value': k.value}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert k.is_delivered
        assert k.is_repayed

    def test_put_prevent_to_repay_without_value(self, api_client):  # noqa: 811
        k = Key.objects.create(
            value='5432', is_delivered=True
        )
        r = api_client.put(f'/keys/{k.id}/')
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert k.is_delivered
        assert not k.is_repayed

    @pytest.mark.parametrize('field_name', ['is_delivered', 'is_repayed'])
    def test_put_prevent_to_inject_data(self, api_client, field_name):  # noqa: 811
        k = Key.objects.create(
            value='SDFG', is_delivered=True, is_repayed=True

        )
        r = api_client.put(
            f'/keys/{k.id}/', {field_name: False}, format='json'
        )
        k = Key.objects.get(pk=k.pk)

        assert r.status_code == status.HTTP_400_BAD_REQUEST

        assert k.is_delivered
        assert k.is_repayed
