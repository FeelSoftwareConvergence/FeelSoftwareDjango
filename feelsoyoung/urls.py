from django.urls import path
from feelsoyoung import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [ 
    #path("sentiment_analysis/", views.sentiment_views),
    path("recommend/", views.post),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
