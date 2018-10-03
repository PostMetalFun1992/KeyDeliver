from rest_framework import serializers

from key_deliver_app.models import Key


class KeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Key
        fields = ('id', 'value', 'is_delivered', 'is_repayed')
