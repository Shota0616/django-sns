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
