from rest_framework import generics, response


class KeyList(generics.ListAPIView):
    def list(request, *args, **kwargs):
        return response.Response(status=200)
