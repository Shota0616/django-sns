from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password

from allauth.account.forms import SignupForm, LoginForm, ResetPasswordForm, ResetPasswordKeyForm, PasswordField

from .models import MyUser


# フォームクラス作成
class UserForm(forms.ModelForm):
    # パスワード入力：非表示対応
    password = forms.CharField(widget=forms.PasswordInput(),label="パスワード")

    class Meta():
        # ユーザー認証
        model = User
        # フィールド指定
        fields = ('username','email','password')
        # フィールド名指定
        labels = {'username':"ユーザー名",'email':"Eメール"}

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=30, label='姓')
    last_name = forms.CharField(max_length=30, label='名')


# allauthForm
# class MyCustomSignupForm(SignupForm):
#     pass

    # class Meta(UserCreationForm.Meta):
    #     model   = MyUser
    #     fields  = ("first_name","last_name","email","profile_image")

class MyCustomSignupForm(SignupForm, UserCreationForm):
    
    first_name = forms.CharField(max_length=30, label='姓',
        widget=forms.TextInput(
        attrs={'placeholder':'姓', 'class':'form-control'}))
    last_name = forms.CharField(max_length=30, label='名',
        widget=forms.TextInput(
        attrs={'placeholder':'名', 'class':'form-control'}))
    email = forms.EmailField(max_length=255,
        widget=forms.TextInput(
        attrs={'type':'email', 'name':'login', "autocomplete":"email", 'placeholder':'メールアドレス', 'class':'form-control'}))
    profile_image = forms.ImageField(required=False)
    password1 = forms.CharField(max_length=128,)
    password2 = forms.CharField(max_length=128,)

    class Meta:
        model = MyUser
        fields = ['first_name', 'last_name', 'email', 'profile_image',]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("メールアドレスは必須です。")
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("こちらのメールアドレスは既に登録済みです。")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        validate_password(password2, self.instance)
        return password2
    
    # def save(self, request):
    #     user = super(MyCustomSignupForm, self).save(request)
    #     user.first_name = self.cleaned_data['first_name']
    #     user.last_name = self.cleaned_data['last_name']
    #     user.profile_image = self.cleaned_data['profile_image']
    #     user.save()
    #     return user

# class MyLoginForm(LoginForm):
#     pass
    # email = forms.EmailField(max_length=255,
    #     widget=forms.TextInput(
    #     attrs={'type':'email', 'name':'login', "autocomplete":"email", 'placeholder':'メールアドレス', 'class':'form-control'}))
    # password = PasswordField(max_length=128,
    #     widget=forms.TextInput(
    #     attrs={'autocomplete':'current-password', 'placeholder':'パスワード', 'class':'form-control'}))
    # remember = forms.BooleanField(label=("ログイン状態を保持する"), required=False)

# class LoginForm(LoginForm):
#     pass

# class ResetPasswordForm(ResetPasswordForm):
#     pass


# class ResetPasswordKeyForm(ResetPasswordKeyForm):
#     pass

# class ChangePasswordForm(authforms.ChangePasswordForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs['class'] = 'form-control'

#     oldpassword = authforms.PasswordField(
#         label=("Current Password"), autocomplete="current-password"
#     )
#     password1 = authforms.SetPasswordField(label=("New Password"))
#     password2 = authforms.PasswordField(label=("New Password (again)"))

#     def __init__(self, *args, **kwargs):
#         super(ChangePasswordForm, self).__init__(*args, **kwargs)
#         self.fields["password1"].user = self.user

#     def clean_oldpassword(self):
#         if not self.user.check_password(self.cleaned_data.get("oldpassword")):
#             raise forms.ValidationError(("Please type your current password."))
#         return self.cleaned_data["oldpassword"]

#     def save(self):
#         get_adapter().set_password(self.user, self.cleaned_data["password1"])