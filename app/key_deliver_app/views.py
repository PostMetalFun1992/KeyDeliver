from rest_framework import generics
from rest_framework.response import Response

from key_deliver_app.models import Key
from key_deliver_app.serializers import KeySerializer


class KeyList(generics.ListCreateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer


class KeyDetail(generics.RetrieveUpdateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def update(self, request, *args, **kwargs):
        key = self.get_object()
        key.is_delivered = True
        key.save()

        return Response(self.get_serializer(key).data)
