from rest_framework import serializers

from key_deliver_app.models import Key


class KeySerializer(serializers.ModelSerializer):
    def validate(self, d):
        if d['is_repayed'] and not d['is_delivered']:
            raise serializers.ValidationError(
                'Cannot repay key before delivery'
            )

        return d

    class Meta:
        model = Key
        fields = ('id', 'value', 'is_delivered', 'is_repayed')
