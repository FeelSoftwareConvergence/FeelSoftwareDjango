from django.shortcuts import render
from sentiment_analysis import sentiment
from sentiment_analysis import recommend_music
from image_emotion import emotion_from_image
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view


# Create your views here.
@api_view(["POST"])
def post(request):
    reply = request.data["content"]
    img = request.data["image"]

    print(reply)
    print(img)

    text_result = sentiment(reply)
    img_result = emotion_from_image(img)

    sentiment_result = recommend_music(reply, text_result, img_result)

    title = list(sentiment_result['title'])
    artist = list(sentiment_result['artist'])

    content = {'title': title, 'artist': artist}

    return Response(status=HTTP_200_OK, data=content)
