from rest_framework import generics, status
from rest_framework.response import Response

from key_deliver_app.models import Key
from key_deliver_app.serializers import KeySerializer
from key_deliver_app.utils import generate_value


class KeyList(generics.ListCreateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def create(self, request, *args, **kwargs):
        # TODO: catch not unique error
        data = {'value': generate_value()}

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
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
