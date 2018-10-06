from rest_framework import serializers

from key_deliver_app.models import Key


class KeySerializer(serializers.ModelSerializer):
    value = serializers.CharField(required=False)

    def validate_value(self, value):
        if not value == self.instance.value:
            raise serializers.ValidationError('Don\'t match')

        return value

    def validate_is_repayed(self, is_repayed):
        if is_repayed and not self.instance.is_delivered:
            raise serializers.ValidationError('Cannot repay before delivery')

        if is_repayed and self.instance.is_repayed:
            raise serializers.ValidationError('Cannot repay two times')

        return is_repayed

    class Meta:
        model = Key
        fields = ('id', 'value', 'is_delivered', 'is_repayed')
