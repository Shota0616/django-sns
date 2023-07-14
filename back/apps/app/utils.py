from django.db.models import Count
from .models import Like


def get_tweet_likes(tweets):
    tweet_ids = [tweet.id for tweet in tweets]
    tweet_likes = (
        Like.objects
        .filter(tweet_id__in=tweet_ids)
        .values('tweet_id')
        .annotate(count=Count('id'))
    )
    tweet_likes_dict = {like['tweet_id']: like['count'] for like in tweet_likes}
    return tweet_likes_dict or ""

def is_user_liked_for_tweet(user):
    return Like.objects.filter(user=user).exists()