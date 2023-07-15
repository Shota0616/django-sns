from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from app.models import Tweet, Comment, Like
from app.forms import TweetForm, CommentForm
from app.utils import get_tweet_likes, get_user_liked_tweet

# 初期画面
class IndexView(View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related('user').order_by('-updated_at')
        current_user = request.user
        # tweetごとのいいね数をdictで取得
        tweet_likes = get_tweet_likes(tweets)
        # ログイン中のユーザーがいいねしているtweetを取得
        user_liked_tweet = get_user_liked_tweet(current_user)

        context = {
            'tweets': tweets,
            'current_user': current_user,
            'tweet_likes': tweet_likes,
            'is_user_liked_for_tweet': user_liked_tweet,
        }
        return render(request, 'app/index.html', context)

# Tweetを作成
class TweetCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TweetForm()
        return render(request, 'app/tweet_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # ログインしているユーザーを設定
            tweet.save()
            return redirect('profile')  # Tweetの一覧ページにリダイレクト
        else:
            return render(request, 'app/tweet_create.html', {'form': form})

# Tweet詳細
class TweetDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        tweet = Tweet.objects.select_related('user').get(id=pk) # Tweetを取得、存在しない場合は404エラーを表示
        comments = Comment.objects.select_related('user').filter(tweet_id=pk)
        current_user = request.user
        tweet_likes = get_tweet_likes(tweet)
        user_liked_tweet = get_user_liked_tweet(current_user)
        context = {
            'tweet': tweet,
            'comments': comments,
            'current_user': current_user,
            'form': form,
            'tweet_likes': tweet_likes,
            'is_user_liked_for_tweet': user_liked_tweet,
        }
        return render(request, 'app/tweet_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user  # ログインしているユーザーを設定
            comment.tweet = Tweet.objects.get(id=pk)  # コメントの対象となるTweetを取得
            comment.save()
            return redirect('tweet_detail', pk=pk)  # Tweetの詳細ページにリダイレクト
        else:
            return render(request, 'app/tweet_detail.html', {'form': form})

# Tweet編集
class TweetEditView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        form = TweetForm(instance=tweet)  # フォームを初期化、初期値はtweet
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != tweet.user:
            return redirect('tweet_detail', pk=tweet.pk)  # 一致しなければ、詳細ページにリダイレクト
        return render(request, 'app/tweet_edit.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != tweet.user:
            return redirect('tweet_detail', pk=tweet.pk)  # 一致しなければ、詳細ページにリダイレクト
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_detail', pk=tweet.pk)  # 編集後のTweetの詳細ページにリダイレクト
        else:
            return render(request, 'app/tweet_edit.html', {'form': form})

# Tweet削除
class TweetDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = Tweet.objects.select_related('user').get(id=pk)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != tweet.user:
            return redirect('tweet_detail', pk=tweet.pk)  # 一致しなければ、詳細ページにリダイレクト
        return render(request, 'app/tweet_delete.html', {'tweet': tweet})

    def post(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk) # Add this line
        if request.user != tweet.user:
            return redirect('tweet_detail', pk=tweet.pk)  # 一致しなければ、詳細ページにリダイレクト
        else:
            tweet.delete()
            return redirect('profile')  # Tweetの一覧ページにリダイレクト


# Comment編集
class CommentEditView(View):
    def get(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        form = CommentForm(request.POST, instance=comment)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.pk)  # 一致しなければ、詳細ページにリダイレクト
        return render(request, 'app/tweet_edit.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.pk)  # 一致しなければ、詳細ページにリダイレクト
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('tweet_detail', pk=comment.pk)  # 編集後のTweetの詳細ページにリダイレクト
        else:
            return render(request, 'app/tweet_edit.html', {'form': form})


# Comment削除
class CommentDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        comment = Comment.objects.select_related('user').get(id=pk)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.pk)  # 一致しなければ、詳細ページにリダイレクト
        return render(request, 'app/tweet_delete.html', {'tweet': comment})

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk) # Add this line
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.pk)  # 一致しなければ、詳細ページにリダイレクト
        else:
            comment.delete()
            return redirect('profile')  # Tweetの一覧ページにリダイレクト

# tweetのいいね用関数
def like_tweet(request):
    # likeボタンを押したtweetのpkを取得
    # tweet_pk = request.POST.get('tweet_pk')
    tweet_pk = int(request.POST.get('tweet_pk'))
    # tweetをいいねしたユーザーをcontextに格納
    context = {
        'user': f'{ request.user }',
    }
    tweet = Tweet.objects.get(id=tweet_pk)
    like = Like.objects.filter(tweet=tweet, user=request.user)

    if like.exists():
        like.delete()
        context['method'] = 'delete'
    else:
        like.create(tweet=tweet, user=request.user)
        context['method'] = 'create'

    tweet_likes_dict = get_tweet_likes(tweet)
    context['tweet_likes'] = tweet_likes_dict[tweet_pk]

    return JsonResponse(context)

