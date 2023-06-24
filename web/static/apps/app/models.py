from django.db import models

from user.models import User


# Tweetモデル
class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tweet_user')
    text = models.CharField(max_length=300,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_tweet"


# Likeモデル
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='like_user')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='like_tweet')
    liked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')
        db_table = "app_like"


# Commentモデル
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='comments_tweet')
    text = models.CharField(max_length=300,blank=False,null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "app_comment"


# Retweetモデル
class Retweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='retweet_user')
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name='retweet_tweet')
    retweeted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')
        db_table = "app_retweet"


# Followモデル
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    followed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        db_table = "app_follow"
