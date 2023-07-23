from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from allauth.account import views
from allauth.account import forms

from user.models import User
from app.models import Tweet
from user.forms import ProfileEditForm, MyCustomSignupForm
from app.utils import get_tweet_likes, get_user_liked_tweet, get_tweet_comment


class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        user_data = User.objects.get(id=pk)
        current_user = request.user
        try:
            items_per_page = 10  # 1ページに表示するアイテム数
            # GETパラメータからページ番号を取得し、デフォルトは1ページ目とします
            page_number = request.GET.get('page', 1)
            tweets = Tweet.objects.select_related('user').filter(user=pk).order_by('created_at').reverse()
            paginator = Paginator(tweets, items_per_page)
        except Tweet.DoesNotExist:
            pass

        # ページネーション
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            # ページ番号が整数ではない場合は、最初のページを表示します
            page = paginator.page(1)
        except EmptyPage:
            # ページ番号が範囲外の場合は、最後のページを表示します
            page = paginator.page(paginator.num_pages)
        # tweetごとのいいね数をdictで取得
        tweet_likes = get_tweet_likes(tweets)
        # tweetごとのコメント数をdictで取得
        tweet_comment = get_tweet_comment(tweets)
        # ログイン中のユーザーがいいねしているtweetを取得
        if current_user.id == pk:
            user_liked_tweet = get_user_liked_tweet(request, current_user)
            context = {
                'user_data': user_data,
                'tweets': page,
                'page': page,
                'current_user': current_user,
                'tweet_likes': tweet_likes,
                'tweet_comment': tweet_comment,
                'is_user_liked_for_tweet': user_liked_tweet,
            }
        else:
            context = {
                'user_data': user_data,
                'tweets': page,
                'page': page,
                'current_user': current_user,
                'tweet_likes': tweet_likes,
                'tweet_comment': tweet_comment,
            }
        return render(request, 'account/profile.html', context)


# ユーザー情報編集View
class ProfileEditView(View):
    # 編集ボタンを押下したときに既存値を取得して表示
    def get(self, request, *args, **kwargs):
        user_data = User.objects.get(id=request.user.id)
        form = ProfileEditForm(
            # formにinit情報を設定
            initial={
                'nickname': user_data.nickname,
                'userid': user_data.userid,
                'introduction': user_data.introduction,
            }
        )
        return render(request, 'account/profile_edit.html', {'form': form})

    def post(self, request, *args, **kwargs):

        user_data = User.objects.get(id=request.user.id)
        form = ProfileEditForm(request.POST or None, request.FILES or None, instance=user_data)

        if form.is_valid():
            form.save(user_data)
            return redirect('profile', pk=user_data.pk)
        else:
            return render(request, 'account/profile.html', {'form': form})


# allauthのviewをオーバーライド
class SignupView(views.SignupView, MyCustomSignupForm):
    form_class = MyCustomSignupForm
    template_name = 'account/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        form.save(self.request)  # save()メソッドを呼び出す
        return response
