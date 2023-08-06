from django.db.models import Count
from app.models import Like, Comment, Follow


# 各ツイートとそれぞれのlike数を取得する（引数に取得するツイートをクエリセットで渡す）
def get_tweet_likes(tweets):
    # 引数のtweetのidをtweet_idsに格納
    try:
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
    except:
        pass


# 引数に指定したuserのlike済のtweetを取得
def get_user_liked_tweet(request, user):
    if request.user.is_authenticated:
        is_user_liked_for_tweet = Like.objects.filter(user=user).values_list('tweet_id', flat=True)
        is_user_liked_for_tweet_list = list(is_user_liked_for_tweet)
        return is_user_liked_for_tweet_list
    else:
        pass


# ツイートのコメントを取得
def get_tweet_comment(tweets):
    try:
        # 引数のtweetのidをtweet_idsに格納
        try:
            tweet_ids = [tweet.id for tweet in tweets]
        except:
            tweet_ids = [tweets.id]
        # カウント
        tweet_comments = (
            Comment.objects
            .filter(tweet_id__in=tweet_ids)
            .values('tweet_id')
            .annotate(count=Count('id'))
        )
        tweet_comments_dict = {like['tweet_id']: like['count'] for like in tweet_comments}
        if len(tweet_comments_dict) == 0:
            tweet_comments_dict = {tweets.id : ""}
        return tweet_comments_dict
    except:
        pass
