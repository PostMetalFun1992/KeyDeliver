from rest_framework import generics, status
from rest_framework.response import Response

from key_deliver_app.models import Key
from key_deliver_app.serializers import KeySerializer
from key_deliver_app.utils import generate_value


class KeyList(generics.ListCreateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def get_serializer_with_data(self):
        is_valid = False
        while not is_valid:
            serializer = self.get_serializer(data={'value': generate_value()})
            is_valid = serializer.is_valid()

        return serializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_with_data()
        self.perform_create(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class KeyDetail(generics.RetrieveUpdateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def update(self, request, *args, **kwargs):
        key = self.get_object()
        key.is_delivered = True
        key.save()

        return Response(
            self.get_serializer(key).data,
            status=status.HTTP_200_OK
        )
