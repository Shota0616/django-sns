from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

from allauth.account import views

from user.models import User
from app.models import Tweet, Follow
from user.forms import ProfileEditForm, MyCustomSignupForm
from app.utils import get_tweet_likes, get_user_liked_tweet, get_tweet_comment

class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        user_data = User.objects.get(id=pk)
        tweets = Tweet.objects.select_related('user').prefetch_related('comments_tweet').filter(user=pk).order_by('created_at').reverse()
        # follow, follower情報を取得
        follow_datas = Follow.objects.filter(from_user=request.user)
        follower_list_queryset = follow_datas.values_list('to_user', flat=True)
        # ログイン中のユーザーがフォローしているユーザ
        follower_list = list(follower_list_queryset)
        # follow, followerの数だけ取得
        to_user_count = Follow.objects.filter(to_user=pk).count()
        from_user_count = Follow.objects.filter(from_user=pk).count()

        context = {
            'user_data': user_data,
            'follow_datas': follow_datas,
            'to_user_count': to_user_count,
            'from_user_count': from_user_count,
            'follower_list': follower_list,
        }

        # ページネーション
        items_per_page = 10
        page_number = request.GET.get('page', 1)
        paginator = Paginator(tweets, items_per_page)
        try:
            page = paginator.page(page_number)
        except (EmptyPage, PageNotAnInteger):
            page = paginator.page(1)
        # tweetが存在するときはtweetの情報も取得
        if tweets.exists():
            # tweetごとのいいね数をdictで取得
            tweet_likes = get_tweet_likes(tweets)
            # tweetごとのコメント数をdictで取得
            tweet_comment = get_tweet_comment(tweets)
            context['tweet_likes'] = tweet_likes
            context['tweet_comment'] = tweet_comment
            context['tweets'] = page
            context['page'] = page

        # ユーザがログインしていたらログインしているユーザのいいねしている投稿を取得
        if request.user.is_authenticated:
            current_user = request.user
            user_liked_tweet = get_user_liked_tweet(request, current_user)
            context['is_user_liked_for_tweet'] = user_liked_tweet
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
