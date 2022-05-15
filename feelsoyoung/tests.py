from django.test import TestCase

# Create your tests here.
from sentiment_analysis import sentiment

sentiment_result = sentiment()
title = list(sentiment_result['title'])
artist = list(sentiment_result['artist'])

res = {"song": {}}
for a, t in title, artist:
    res["song"][a] = t

print(res)