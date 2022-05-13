from django.urls import path
from feelsoyoung import views

urlpatterns = [
    path("sentiment_analysis/", views.sentiment_views),
    path("recommend/", views.post),
]