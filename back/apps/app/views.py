from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Tweet
from .forms import TweetForm, TweetEditForm

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
        tweet = Tweet.objects.all().select_related('user').get(id=pk) # Tweetを取得、存在しない場合は404エラーを表示
        current_user = request.user
        context = {
            'tweet': tweet,
            'current_user': current_user,
        }
        return render(request, 'app/tweet_detail.html', context)

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
        tweet = get_object_or_404(Tweet, pk=pk)
        return render(request, 'app/confirm_delete.html', {'tweet': tweet})

    def post(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        tweet.delete()
        return redirect('tweets:list')  # Tweetの一覧ページにリダイレクト
