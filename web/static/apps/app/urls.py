from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tweet/create', views.TweetCreateView.as_view(), name='tweet_create')
]