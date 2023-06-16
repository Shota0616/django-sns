from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin


from .models import Tweet
from .forms import TweetForm


# 初期画面
class IndexView(TemplateView):
    template_name = "app/index.html"


# Tweetの一覧を表示(非ログイン時)
class TweetListView(View):
    def get(self, request, *args, **kwargs):
        tweets = Tweet.objects.all()  # 全てのツイートを取得
        return render(request, 'tweets/list.html', {'tweets': tweets})

# 新しいTweetを作成
class TweetCreateView(View):
    def get(self, request, *args, **kwargs):
        form = TweetForm()  # フォームを初期化
        return render(request, 'tweets/create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user  # ログインしているユーザーを設定
            tweet.save()
            return redirect('tweets:list')  # Tweetの一覧ページにリダイレクト
        else:
            return render(request, 'tweets/create.html', {'form': form})

# Tweetの詳細を表示
class TweetDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)  # Tweetを取得、存在しない場合は404エラーを表示
        return render(request, 'tweets/detail.html', {'tweet': tweet})

# Tweetを編集
class TweetUpdateView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        form = TweetForm(instance=tweet)  # フォームを初期化、初期値はtweet
        return render(request, 'tweets/update.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        form = TweetForm(request.POST, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweets:detail', pk=tweet.pk)  # 編集後のTweetの詳細ページにリダイレクト
        else:
            return render(request, 'tweets/update.html', {'form': form})

# Tweetを削除
class TweetDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        return render(request, 'tweets/confirm_delete.html', {'tweet': tweet})

    def post(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        tweet.delete()
        return redirect('tweets:list')  # Tweetの一覧ページにリダイレクト
