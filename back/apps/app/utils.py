from django.db.models import Count
from app.models import Like


# 各ツイートとそれぞれのlike数を取得する（引数に取得するツイートをクエリセットで渡す）
def get_tweet_likes(tweets):
    # 引数のtweetのidをtweet_idsに格納
    try:
        tweet_ids = [tweet.id for tweet in tweets]
    except:
        tweet_ids = [tweets.id]
    # カウント
    tweet_likes = (
        Like.objects
        .filter(tweet_id__in=tweet_ids)
        .values('tweet_id')
        .annotate(count=Count('id'))
    )
    tweet_likes_dict = {like['tweet_id']: like['count'] for like in tweet_likes}
    if len(tweet_likes_dict) == 0:
        tweet_likes_dict = {tweets.id : ""}
    return tweet_likes_dict


# 引数に指定したuserのlike済のtweetを取得
def get_user_liked_tweet(user):
    is_user_liked_for_tweet = Like.objects.filter(user=user).values_list('tweet_id', flat=True)
    is_user_liked_for_tweet_list = list(is_user_liked_for_tweet)
    return is_user_liked_for_tweet_list

#    tweet_likes = Like.objects.filter(tweet_id__in=tweet_ids).values('tweet_id').annotate(count=Count('id'))
