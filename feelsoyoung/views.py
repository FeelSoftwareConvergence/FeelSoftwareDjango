from django.shortcuts import render
from sentiment_analysis import sentiment
from sentiment_analysis import recommend_music
from image_emotion import emotion_from_image
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.decorators import api_view
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import os
import glob

# Create your views here.
@api_view(["POST"])
def post(request):
    image = request.FILES["image"]
    content = request.POST["content"]

    path = default_storage.save('target_image.png', ContentFile(image.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)

    print(content)  
    print("path: " + tmp_file)

    text_result = sentiment(content)
    img_result = emotion_from_image(tmp_file)

    sentiment_result = recommend_music(content, text_result, img_result)

    title = list(sentiment_result['title'])
    artist = list(sentiment_result['artist'])

    content = {'title': title, 'artist': artist}
    
    # delete image
    trash_image = glob.glob(settings.MEDIA_ROOT + '/*.png')
    for i in trash_image:
        os.remove(i)

    return Response(status=HTTP_200_OK, data=content)
