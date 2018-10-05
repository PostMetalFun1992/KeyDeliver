import re

import pytest
from rest_framework import status

from key_deliver_app.models import Key


class TestKeyList:
    def test_list(self, api_client):  # noqa: 811
        Key.objects.bulk_create([
            Key(value='1234'),
            Key(value='ABCD', is_delivered=True),
            Key(value='12AB', is_delivered=True, is_repayed=True),
        ])

        r = api_client.get('/keys/')

        assert r.status_code == status.HTTP_200_OK

        assert r.data.keys() == {'count', 'delivered', 'repayed', 'keys'}
        assert r.data['count'] == 3
        assert r.data['delivered'] == 2
        assert r.data['repayed'] == 1
        assert len(r.data['keys']) == 3

    def test_create(self, api_client):  # noqa: 811
        r = api_client.post('/keys/')
        k = Key.objects.all().first()

        assert Key.objects.count() == 1
        assert r.status_code == status.HTTP_201_CREATED

        assert r.data.keys() == {'id', 'value', 'is_delivered', 'is_repayed'}
        assert not r.data['is_delivered']
        assert not r.data['is_repayed']

        assert re.match(r'^.{4}$', k.value)
        assert not k.is_delivered
        assert not k.is_repayed

    @pytest.mark.parametrize('keys_count', [100])
    def test_create_many(self, api_client, keys_count):  # noqa: 811
        for _ in range(keys_count):
            assert api_client.post('/keys/').status_code == \
                status.HTTP_201_CREATED
