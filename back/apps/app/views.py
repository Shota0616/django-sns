from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from app.models import Tweet, Comment, Like, Follow
from user.models import User
from app.forms import TweetForm, CommentForm
from app.utils import get_tweet_likes, get_user_liked_tweet, get_tweet_comment


# 初期画面
class IndexView(View):
    def get(self, request, *args, **kwargs):
        items_per_page = 10  # 1ページに表示するアイテム数
        # GETパラメータからページ番号を取得し、デフォルトは1ページ目とします
        page_number = request.GET.get('page', 1)
        if request.user.is_authenticated:
            # ログイン中のユーザーがフォローしているユーザーを取得
            following_user_ids = Follow.objects.filter(from_user_id=request.user).values_list('to_user_id', flat=True)
            tweets = Tweet.objects.select_related('user').prefetch_related('comments_tweet').filter(Q(user_id__in=following_user_ids) | Q(user_id=request.user)).order_by('created_at')
            if not tweets.exists():
                tweets = Tweet.objects.select_related('user').prefetch_related('comments_tweet').order_by('created_at').reverse()[:100]
        else:
            tweets = Tweet.objects.select_related('user').prefetch_related('comments_tweet').order_by('created_at').reverse()[:100]
        paginator = Paginator(tweets, items_per_page)
        # tweetごとのいいね数をdictで取得
        tweet_likes = get_tweet_likes(tweets)
        # tweetごとのコメント数をdictで取得
        tweet_comment = get_tweet_comment(tweets)

        # ページネーション
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # ページ番号が整数ではない場合は、最初のページを表示します
            page = paginator.page(1)
        except EmptyPage:
            # ページ番号が範囲外の場合は、最後のページを表示します
            page = paginator.page(paginator.num_pages)
        # ログインしているときの処理
        context = {
            'tweets': page,
            'page': page,
            'tweet_likes': tweet_likes,
            'tweet_comment': tweet_comment,
        }
        if request.user.is_authenticated:
            current_user = request.user
            # ログイン中のユーザーがいいねしているtweetを取得
            user_liked_tweet = get_user_liked_tweet(request, current_user)
            context['current_user'] = current_user
            context['is_user_liked_for_tweet'] = user_liked_tweet
        return render(request, 'app/index.html', context)


# 検索
class SearchView(View):
    def get(self, request, *args, **kwargs):
        search_items = request.GET.get('search-items', '')
        keywords = search_items.split()
        q_objects = Q()
        for keyword in keywords:
            q_objects |= Q(text__icontains=keyword)

        tweets = Tweet.objects.filter(q_objects).select_related('user').prefetch_related('comments_tweet').order_by('-created_at')

        tweet_likes = get_tweet_likes(tweets)
        tweet_comment = get_tweet_comment(tweets)

        paginator = Paginator(tweets, 10)
        page_number = request.GET.get('page', 1)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context = {
            'tweets': page,
            'page': page,
            'search_items': keywords,
            'search_items_original': search_items,
            'tweet_likes': tweet_likes,
            'tweet_comment': tweet_comment,
        }

        if request.user.is_authenticated:
            current_user = request.user
            user_liked_tweet = get_user_liked_tweet(request, current_user)
            context['current_user'] = current_user
            context['is_user_liked_for_tweet'] = user_liked_tweet

        return render(request, 'app/search_results.html', context)

class UserSearchView(View):
    def get(self, request, *args, **kwargs):
        search_items = request.GET.get('search-items', '')
        # スペースで区切って複数のキーワードを取得
        keywords = search_items.split()
        # Qオブジェクトを使用して複数のクエリを組み合わせる
        q_objects = Q()
        for keyword in keywords:
            q_objects |= Q(userid__icontains=keyword) | Q(nickname__icontains=keyword)

        users = User.objects.filter(q_objects)

        paginator = Paginator(users, 10)
        page_number = request.GET.get('page', 1)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        context = {
            'users': page,
            'page': page,
            'search_items': keywords,
            'search_items_original': search_items,
        }

        if request.user.is_authenticated:
            # follow情報を取得
            follow_datas = Follow.objects.filter(from_user=request.user)
            follower_list_queryset = follow_datas.values_list('to_user', flat=True)
            # ログイン中のユーザーがフォローしているユーザ
            follower_list = list(follower_list_queryset)
            context['follower_list'] = follower_list

        return render(request, 'app/user_search_results.html', context)

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
        context = {
            'tweet': tweet,
            'comments': comments,
            'current_user': current_user,
            'form': form,
            'tweet_likes': tweet_likes,
            'tweet_comment': tweet_comment,
        }
        if request.user.is_authenticated:
            user_liked_tweet = get_user_liked_tweet(request, current_user)
            context['is_user_liked_for_tweet'] = user_liked_tweet
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
        form = CommentForm(instance=comment)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.tweet.id)  # 一致しなければ、詳細ページにリダイレクト
        return render(request, 'app/comment_edit.html', {'form': form})

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.tweet.id)  # 一致しなければ、詳細ページにリダイレクト
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('tweet_detail', pk=comment.tweet.id)  # 編集後のTweetの詳細ページにリダイレクト
        else:
            return render(request, 'app/comment_edit.html', {'form': form})


# Comment削除
class CommentDeleteView(View):
    def get(self, request, pk, *args, **kwargs):
        comment = Comment.objects.select_related('user').get(id=pk)
        # ログインしているユーザーがツイートの作成者と一致するか確認
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.tweet.id)  # 一致しなければ、詳細ページにリダイレクト
        return render(request, 'app/comment_delete.html', {'tweet': comment})

    def post(self, request, pk, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=pk) # Add this line
        if request.user != comment.user:
            return redirect('tweet_detail', pk=comment.tweet.id)  # 一致しなければ、詳細ページにリダイレクト
        else:
            comment.delete()
            return redirect('tweet_detail', pk=comment.tweet.id)  # 詳細ページにリダイレクト


# フォロー情報の取得
class GetFollowView(View):
    def get(self, request, pk, *args, **kwargs):
        # ユーザのフォローリスト
        user_following_list = Follow.objects.select_related('to_user').filter(from_user=pk)
        context = {
            'pk': pk,
        }
        # ページネーション
        items_per_page = 10
        page_number = request.GET.get('page', 1)
        paginator = Paginator(user_following_list, items_per_page)
        try:
            page = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            page = paginator.page(1)

        if user_following_list.exists():
            context['user_following_list'] = page
            context['page'] = page

        if request.user.is_authenticated:
            # follow情報を取得
            follow_datas = Follow.objects.filter(from_user=request.user)
            follower_list_queryset = follow_datas.values_list('to_user', flat=True)
            # ログイン中のユーザーがフォローしているユーザ
            follower_list = list(follower_list_queryset)
            context['follower_list'] = follower_list
        return render(request, 'app/follow.html', context)


class GetFollowerView(View):
    def get(self, request, pk, *args, **kwargs):
        user_followers_list = Follow.objects.select_related('from_user').filter(to_user=pk)
        context = {
            'pk': pk,
        }

        # ページネーション
        items_per_page = 10
        page_number = request.GET.get('page', 1)
        paginator = Paginator(user_followers_list, items_per_page)
        try:
            page = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            page = paginator.page(1)

        if user_followers_list.exists():
            context['user_followers_list'] = page
            context['page'] = page

        if request.user.is_authenticated:
            # follow情報を取得
            follow_datas = Follow.objects.filter(from_user=request.user)
            follower_list_queryset = follow_datas.values_list('to_user', flat=True)
            # ログイン中のユーザーがフォローしているユーザ
            follower_list = list(follower_list_queryset)
            context['follower_list'] = follower_list
        return render(request, 'app/follower.html', context)

# ユーザのフォローとフォロー解除するための関数
def follow_unfollow_user(request):
    # ユーザーがログイン中のときのみ動作する
    if request.user.is_authenticated:
        # ログイン中のユーザー取得
        current_user = request.user
        to_user_id = int(request.POST.get('to_user_id'))
        from_user_id = int(request.POST.get('from_user_id'))
        is_following = Follow.objects.filter(from_user=from_user_id, to_user=to_user_id)

        if is_following.exists():
            is_following.delete()
            method = 'delete'
        else:
            from_user_instance = User.objects.get(id=from_user_id)
            to_user_instance = User.objects.get(id=to_user_id)
            is_following.create(from_user=from_user_instance, to_user=to_user_instance)
            method = 'create'

        # フォローデータを再度取得してJSONレスポンスに含める
        follow_datas = Follow.objects.filter(from_user=current_user)
        follower_list = list(follow_datas.values_list('to_user', flat=True))

        context = {
            'method': method,
            'follower_list': follower_list,
        }
        return JsonResponse(context)
    # ログイン中のユーザーじゃない場合はログインページに遷移
    else:
        # pass
        return render(request, 'account/login',)


# tweetのいいね用関数
def like_tweet(request):
    if request.user.is_authenticated:
        # likeボタンを押したtweetのpkを取得
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
    else:
        return render(request, 'account/login',)
