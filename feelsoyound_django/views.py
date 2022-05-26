from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(["GET"])
def root(request):
    return Response(status=200, data="hello k-net", content_type="text/html")
