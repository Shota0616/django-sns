from django.db.models import Count
from app.models import Like

# 各ツイートとそれぞれのlike数を取得する（引数に取得するツイートをクエリセットで渡す）
def get_tweet_likes(tweets):
    # 引数のtweetのidをtweet_idsに格納
    tweet_ids = [tweet.id for tweet in tweets]
    # tweet_likesに
    tweet_likes = (
        Like.objects
        .filter(tweet_id__in=tweet_ids)
        .values('tweet_id')
        .annotate(count=Count('id'))
    )
    tweet_likes_dict = {like['tweet_id']: like['count'] for like in tweet_likes}
    # tweet_likes_dict = list(tweet_likes.values())
    return tweet_likes_dict

def is_user_liked_for_tweet(user):
    return Like.objects.filter(user=user).exists()

