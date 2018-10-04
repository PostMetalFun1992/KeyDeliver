from rest_framework import generics, status
from rest_framework.response import Response

from key_deliver_app.models import Key
from key_deliver_app.serializers import KeySerializer
from key_deliver_app.utils import generate_value


class KeyList(generics.GenericAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def get(self, request, *args, **kwargs):
        keys = self.get_serializer(self.get_queryset(), many=True).data

        return Response({
            'count': Key.objects.count(),
            'delivered': Key.objects.count_delivered(),
            'repayed': Key.objects.count_repayed(),
            'keys': keys,
        })

    def get_serializer_with_data(self):
        is_valid = False
        while not is_valid:
            serializer = self.get_serializer(data={'value': generate_value()})
            is_valid = serializer.is_valid()

        return serializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_with_data()
        self.perform_create(serializer)

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class KeyDetail(generics.RetrieveUpdateAPIView):
    queryset = Key.objects.all()
    serializer_class = KeySerializer

    def patch(self, request, *args, **kwargs):
        request.data.clear()
        request.data.update({'is_delivered': True})

        return super().patch(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        request.data.clear()
        request.data.update({'is_repayed': True})

        return super().put(request, *args, **kwargs)
