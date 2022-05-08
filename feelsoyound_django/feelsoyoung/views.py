from django.shortcuts import render
from sentiment_analysis import sentiment

# Create your views here.

def sentiment_views(request) :
    sentiment_result = sentiment()
    title = list(sentiment_result['title'])
    artist = list(sentiment_result['artist'])
    for t in title :
        print(t)
    for a in artist :
        print(a)

    content = {'title' : title, 'artist' : artist}
    return render(request , 'sentiment_analysis.html',content)
