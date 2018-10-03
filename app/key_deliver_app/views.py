from rest_framework import generics

from key_deliver_app.models import Key
from key_deliver_app.serializers import KeySerializer


class KeyList(generics.ListCreateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer


class KeyDetail(generics.RetrieveUpdateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer
