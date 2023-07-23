from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views import generic
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from app.models import Tweet, Comment, Like
from app.forms import TweetForm, CommentForm
from app.utils import get_tweet_likes, get_user_liked_tweet, get_tweet_comment

# # 初期画面
# class IndexView(View):
#     def get(self, request, *args, **kwargs):
#         tweets = Tweet.objects.select_related('user').prefetch_related('comments_tweet').order_by('created_at').reverse()
#         # tweetごとのいいね数をdictで取得
#         tweet_likes = get_tweet_likes(tweets)
#         # tweetごとのコメント数をdictで取得
#         tweet_comment = get_tweet_comment(tweets)
#         # ログインしているときの処理
#         if request.user.is_authenticated:
#             current_user = request.user
#             # ログイン中のユーザーがいいねしているtweetを取得
#             user_liked_tweet = get_user_liked_tweet(request, current_user)
#             context = {
#                 'tweets': tweets,
#                 'current_user': current_user,
#                 'tweet_likes': tweet_likes,
#                 'tweet_comment': tweet_comment,
#                 'is_user_liked_for_tweet': user_liked_tweet,
#             }
#         # ゲストユーザーのときの処理
#         else:
#             # ログイン中のユーザーがいいねしているtweetを取得
#             context = {
#                 'tweets': tweets,
#                 'tweet_likes': tweet_likes,
#                 'tweet_comment': tweet_comment,
#             }
#         return render(request, 'app/index.html', context)


# 初期画面
class IndexView(View):
    def get(self, request, *args, **kwargs):
        items_per_page = 10  # 1ページに表示するアイテム数
        # GETパラメータからページ番号を取得し、デフォルトは1ページ目とします
        page_number = request.GET.get('page', 1)
        tweets = Tweet.objects.select_related('user').prefetch_related('comments_tweet').order_by('created_at').reverse()
        paginator = Paginator(tweets, items_per_page)
        # tweetごとのいいね数をdictで取得
        tweet_likes = get_tweet_likes(tweets)
        # tweetごとのコメント数をdictで取得
        tweet_comment = get_tweet_comment(tweets)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # ページ番号が整数ではない場合は、最初のページを表示します
            page = paginator.page(1)
        except EmptyPage:
            # ページ番号が範囲外の場合は、最後のページを表示します
            page = paginator.page(paginator.num_pages)
        # ログインしているときの処理
        if request.user.is_authenticated:
            current_user = request.user
            # ログイン中のユーザーがいいねしているtweetを取得
            user_liked_tweet = get_user_liked_tweet(request, current_user)
            context = {
                'page': page,
                'tweets': tweets,
                'current_user': current_user,
                'tweet_likes': tweet_likes,
                'tweet_comment': tweet_comment,
                'is_user_liked_for_tweet': user_liked_tweet,
            }
        # ゲストユーザーのときの処理
        else:
            # ログイン中のユーザーがいいねしているtweetを取得
            context = {
                'page': page,
                'tweets': tweets,
                'tweet_likes': tweet_likes,
                'tweet_comment': tweet_comment,
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
            return redirect('profile', pk=tweet.user.pk)  # Tweetの一覧ページにリダイレクト
        else:
            return render(request, 'app/tweet_create.html', {'form': form})

# Tweet詳細
class TweetDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        form = CommentForm(request.POST)
        tweet = Tweet.objects.select_related('user').get(id=pk) # Tweetを取得、存在しない場合は404エラーを表示
        comments = Comment.objects.select_related('user').filter(tweet_id=pk)
        # tweetごとのコメント数をdictで取得
        tweet_comment = get_tweet_comment(tweet)
        current_user = request.user
        tweet_likes = get_tweet_likes(tweet)
        if request.user.is_authenticated:
            user_liked_tweet = get_user_liked_tweet(request, current_user)
            context = {
                'tweet': tweet,
                'comments': comments,
                'current_user': current_user,
                'form': form,
                'tweet_likes': tweet_likes,
                'tweet_comment': tweet_comment,
                'is_user_liked_for_tweet': user_liked_tweet,
            }
        else:
            context = {
                'tweet': tweet,
                'comments': comments,
                'current_user': current_user,
                'form': form,
                'tweet_likes': tweet_likes,
                'tweet_comment': tweet_comment,
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
            return redirect('profile', pk=request.user.pk)  # Tweetの一覧ページにリダイレクト


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
            return redirect('profile', pk=request.user.pk)  # Tweetの一覧ページにリダイレクト

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

