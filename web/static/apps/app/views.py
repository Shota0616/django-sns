from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Tweet, Comment
from .forms import TweetForm, TweetEditForm, CommentForm

# 初期画面
class IndexView(View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.select_related('user').order_by('updated_at').reverse().all()  # 全てのツイートを取得
        return render(request, 'app/index.html', {'tweets': tweets})

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
        context = {
            'tweet': tweet,
            'comments': comments,
            'current_user': current_user,
            'form': form,
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
        form = TweetEditForm(instance=tweet)  # フォームを初期化、初期値はtweet
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != tweet.user:
            return redirect('tweet_detail', pk=tweet.pk)  # 一致しなければ、詳細ページにリダイレクト
        return render(request, 'app/tweet_edit.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != tweet.user:
            return redirect('tweet_detail', pk=tweet.pk)  # 一致しなければ、詳細ページにリダイレクト
        form = TweetEditForm(request.POST, instance=tweet)
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
