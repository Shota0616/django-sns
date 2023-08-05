from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('tweet/create', views.TweetCreateView.as_view(), name='tweet_create'),
    path('tweet/detail/<int:pk>', views.TweetDetailView.as_view(), name='tweet_detail'),
    path('tweet/edit/<int:pk>', views.TweetEditView.as_view(), name='tweet_edit'),
    path('tweet/delete/<int:pk>', views.TweetDeleteView.as_view(), name='tweet_delete'),
    path('comment/edit/<int:pk>', views.CommentEditView.as_view(), name='comment_edit'),
    path('comment/delete/<int:pk>', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('like_tweet', views.like_tweet, name='like_tweet'),
    path('follow', views.follow_unfollow_user, name='user_follow'),
    path('following/<int:pk>', views.GetFollowView.as_view(), name='following'),
    path('followers/<int:pk>', views.GetFollowerView.as_view(), name='followers'),
]
