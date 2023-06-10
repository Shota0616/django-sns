from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from allauth.account import views
from allauth.account import forms

from user.models import MyUser
from user.forms import ProfileEditForm, MyCustomSignupForm


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = MyUser.objects.get(id=request.user.id)
        return render(request, 'account/profile.html', {
            'user_data': user_data,
        })


# ユーザー情報編集View
class ProfileEditView(View):
    # 編集ボタンを押下したときに既存値を取得して表示
    def get(self, request, *args, **kwargs):
        user_data = MyUser.objects.get(id=request.user.id)
        form = ProfileEditForm(
            request.POST or None,
            # formにinit情報を設定
            initial={
                'nickname': user_data.nickname,
                'userid': user_data.userid,
                'introduction': user_data.introduction,
            }
        )
        return render(request, 'account/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileEditForm(request.POST or None)
        # if not form.is_valid():  # バリデーションを行う
        #     # データが不正だったらフォームを再描画する
        #     return render(request, 'account/profile_edit.html', {
        #         'form': form
        #     })
        # else:
        #     user_data = MyUser.objects.get(id=request.user.id)
        #     user_data.nickname = form.cleaned_data['nickname']
        #     user_data.userid = form.cleaned_data['userid']
        #     user_data.introduction = form.cleaned_data['introduction']
        #     # 画像未設定の場合は、デフォルト値を入れておく
        #     if not form.cleaned_data['profile_image']:
        #         user_data.profile_image = 'common/default.png'
        #     else:
        #         user_data.profile_image = form.cleaned_data['profile_image']
        #     user_data.save()
        #     return render(request, 'account/profile.html', {
        #     'form': form,
        #     })

        # if form.is_valid():
        #     user_data = MyUser.objects.get(id=request.user.id)
        #     user_data.nickname = form.cleaned_data['nickname']
        #     user_data.userid = form.cleaned_data['userid']
        #     user_data.introduction = form.cleaned_data['introduction']
        #     # 画像未設定の場合は、デフォルト値を入れておく
        #     if not form.cleaned_data['profile_image']:
        #         user_data.profile_image = 'common/default.png'
        #     else:
        #         user_data.profile_image = form.cleaned_data['profile_image']
        #     user_data.save()
        #     return redirect('profile')
        # return render(request, 'account/profile.html', {
        #     'form': form,
        # })


# allauthのviewをオーバーライド
class SignupView(views.SignupView, MyCustomSignupForm):
    form_class = MyCustomSignupForm
    template_name = 'account/signup.html'
    success_url = 'account/profile.html'

    # def form_valid(self, form):
    #     self.user = form.save(self.request)
    #     if not self.user:
    #         return get_adapter(self.request).respond_email_verification_sent(
    #             self.request, None
    #         )
    #     try:
    #         return complete_signup(
    #             self.request,
    #             self.user,
    #             app_settings.EMAIL_VERIFICATION,
    #             self.get_success_url(),
    #         )
    #     except ImmediateHttpResponse as e:
    #         return e.response

    # def signup(request):
    #     form = MyCustomSignupForm(request.POST or None)
    #     if form.is_valid():
    #         # Do something with the form data
    #         pass
    #     return render(request, 'signup.html', {'form': form})
