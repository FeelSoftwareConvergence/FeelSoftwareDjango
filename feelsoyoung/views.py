from django.shortcuts import render
from sentiment_analysis import sentiment
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.decorators import api_view


# Create your views here.

def sentiment_views(request):
    sentiment_result = sentiment()
    title = list(sentiment_result['title'])
    artist = list(sentiment_result['artist'])
    # for t in title:
    #     print(t)
    # for a in artist:
    #     print(a)

    content = {'title': title, 'artist': artist}
    return render(request, 'sentiment_analysis.html', content)


@api_view(["POST"])
def post(request):
    try:
        reply = request.data["content"]
        img = request.data["image"]

        sentiment_result = sentiment(reply)
        title = list(sentiment_result['title'])
        artist = list(sentiment_result['artist'])

        content = {'title': title, 'artist': artist}
    except KeyError:
        return Response(status=HTTP_400_BAD_REQUEST, data="there is no content or image url")
    except OSError:
        return Response(status=HTTP_500_INTERNAL_SERVER_ERROR, data="processing fail")
    return Response(status=HTTP_200_OK, data=content)
