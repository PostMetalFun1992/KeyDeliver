from rest_framework import generics, status
from rest_framework.response import Response

from key_deliver_app.models import Key
from key_deliver_app.serializers import KeySerializer
from key_deliver_app.utils import generate_unique_key_value


class KeyList(generics.ListCreateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def list(self, request, *args, **kwargs):
        keys = self.get_serializer(self.get_queryset(), many=True).data

        return Response({
            'count': Key.objects.count(),
            'delivered': Key.objects.count_delivered(),
            'repayed': Key.objects.count_repayed(),
            'keys': keys,
        })

    def create(self, request, *args, **kwargs):
        key = Key.objects.create(value=generate_unique_key_value())

        return Response(
            self.get_serializer(key).data,
            status=status.HTTP_201_CREATED
        )


class KeyDetail(generics.RetrieveAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def patch(self, request, *args, **kwargs):
        key = self.get_object()
        serializer = self.get_serializer(
            key,
            data={'value': key.value, 'is_delivered': True}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            self.get_object(),
            data={'value': request.data.get('value'), 'is_repayed': True}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
