from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tweet/create', views.TweetCreateView.as_view(), name='tweet_create'),
    path('tweet/detail/<int:pk>', views.TweetDetailView.as_view(), name='tweet_detail'),
    path('tweet/edit/<int:pk>', views.TweetEditView.as_view(), name='tweet_edit'),
    path('tweet/delete/<int:pk>', views.TweetDeleteView.as_view(), name='tweet_delete'),
]