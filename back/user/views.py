from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from allauth.account import views
from allauth.account import forms

from user.models import MyUser
from user.forms import ProfileForm, MyCustomSignupForm, ResetPasswordForm, ResetPasswordKeyForm


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_data = MyUser.objects.get(id=request.user.id)

        return render(request, 'account/profile.html', {
            'user_data': user_data,
        })

class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user_data = MyUser.objects.get(id=request.user.id)
        form = ProfileForm(
            request.POST or None,
            initial={
                'first_name': user_data.first_name,
                'last_name': user_data.last_name,
            }
        )

        return render(request, 'account/profile_edit.html', {
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST or None)
        if form.is_valid():
            user_data = MyUser.objects.get(id=request.user.id)
            user_data.first_name = form.cleaned_data['first_name']
            user_data.last_name = form.cleaned_data['last_name']
            user_data.save()
            return redirect('profile')

        return render(request, 'account/profile.html', {
            'form': form
        })

# allauthのviewをオーバーライド
class SignupView(views.SignupView, MyCustomSignupForm):
    
    def signup(request):
        form = MyCustomSignupForm(request.POST or None)
        if form.is_valid():
            # Do something with the form data
            pass
        return render(request, 'signup.html', {'form': form})


# class ConfirmEmailView(views.ConfirmEmailView):
#     template_name = "account/email_confirm.html"

# class LoginView(views.LoginView):
#     template_name = 'account/login.html'

# class LogoutView(views.LogoutView):
#     template_name = 'account/logout.html'

#     def post(self, *args, **kwargs):
#         if self.request.user.is_authenticated:
#             self.logout()
#         return redirect('/')

# class PasswordChangeView(views.PasswordChangeView):
#     template_name = 'account/password_change.html'
#     success_url = reverse_lazy('')
#     form_class = forms.ChangePasswordForm

# class PasswordResetView(views.PasswordResetView):
#     """パスワード変更用URLの送付ページ"""
#     # subject_template_name = 'register/mail_template/password_reset/subject.txt'
#     # email_template_name = 'register/mail_template/password_reset/message.txt'
#     template_name = 'account/password_reset.html'
#     form_class = ResetPasswordForm
#     # success_url = reverse_lazy('user:password_reset_done')


# class PasswordResetDoneView(views.PasswordResetDoneView):
#     """パスワード変更用URLを送りましたページ"""
#     template_name = 'account/password_reset_done.html'

# class PasswordResetFromKeyView(views.PasswordResetFromKeyView):
#     template_name = 'account/password_reset_from_key.html'
#     form_class = ResetPasswordKeyForm

# class PasswordResetFromKeyDoneView(views.PasswordResetFromKeyDoneView):
#     template_name = "account/password_reset_from_key_done.html"