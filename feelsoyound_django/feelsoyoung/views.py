from django.shortcuts import render
from sentiment_analysis import sentiment

# Create your views here.

def sentiment_views(request) :
    sentiment_result = sentiment()
    content = {'sentiment' : sentiment_result}
    return render(request , 'sentiment_analysis.html',content)