from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import password_validation, get_user
from allauth.account.forms import SignupForm

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

class ProfileEditForm(forms.Form):
    userid = forms.CharField(max_length=30, label='ユーザーID',
        widget=forms.TextInput(
        attrs={'placeholder':'ユーザーID', 'class':'form-control'}))
    nickname = forms.CharField(max_length=30, label='名前',
        widget=forms.TextInput(
        attrs={'placeholder':'名前', 'class':'form-control'}))
    introduction = forms.CharField(max_length=1000, label='自己紹介',
        widget=forms.Textarea(
        attrs={'placeholder':'自己紹介', 'class':'form-control'}))
    profile_image = forms.ImageField(required=False, initial='common/default.png')

    def __init__(self, *args, **kwargs):
        for field in self.base_fields.values():
            field.widget.attrs["class"] = "form-control"
        super().__init__(*args, **kwargs)

    # バリデーション
    def clean_userid(self):
        userid = self.cleaned_data.get('userid')
        user = get_user(self.login_user)
        if MyUser.objects.exclude(id=user.id).filter(userid=userid).exists():
            raise forms.ValidationError('こちらのユーザーIDはすでに使用されています。')
        return userid

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if len(nickname) >= 30:
            raise forms.ValidationError('ニックネームは30文字以内で入力してください。')
        return nickname


class MyCustomSignupForm(SignupForm):

    email = forms.EmailField(max_length=255, required=False,
        widget=forms.TextInput(
        attrs={'type':'email', 'name':'login', "autocomplete":"email", 'placeholder':'メールアドレス', 'class':'form-control'}))
    password1 = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput())
    userid = forms.CharField(max_length=30, label='ユーザーID', required=False,
        widget=forms.TextInput(
        attrs={'placeholder':'ユーザーID', 'class':'form-control'}))
    nickname = forms.CharField(max_length=30, label='名前', required=False,
        widget=forms.TextInput(
        attrs={'placeholder':'名前', 'class':'form-control'}))
    introduction = forms.CharField(max_length=1000, label='自己紹介', required=False,
        widget=forms.Textarea(
        attrs={'placeholder':'自己紹介', 'class':'form-control'}))
    profile_image = forms.ImageField(required=False, initial='common/default.png')


        # class Meta:
        #     model = MyUser
        #     fields = ('email', 'userid', 'nickname', 'password1', 'password2', 'introduction', 'profile_image')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['introduction'].required = False  # 必須フィールドではないことを明示


    def clean(self):
        cleaned_data = super().clean()

        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        userid = cleaned_data.get('userid')

        # メールアドレスのバリデーション
        if not email:
            raise forms.ValidationError("メールアドレスは必須です。")
        if MyUser.objects.filter(email=email).exists():
            raise forms.ValidationError("こちらのメールアドレスは既に登録済みです.")

        # パスワードのバリデーション
        if not password1:
            raise forms.ValidationError("パスワードは必須です。")
        if not password2:
            raise forms.ValidationError("確認用パスワードも入力してください。")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        password_validation.validate_password(password2)

        # ユーザーIDのバリデーション
        if not userid:
            raise forms.ValidationError("ユーザーIDは必須です。")
        if MyUser.objects.filter(userid=userid).exists():
            raise forms.ValidationError('こちらのユーザーIDはすでに使用されています。')

        # デフォルトのバリデーションエラーが発生したら以下のメッセージを返す
        if self.errors:
            self.add_error(None, "入力内容に問題があります。")

        return cleaned_data

    # # バリデーション
    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if not email:
    #         raise forms.ValidationError("メールアドレスは必須です。")
    #     if MyUser.objects.filter(email=email).exists():
    #         raise forms.ValidationError("こちらのメールアドレスは既に登録済みです。")
    #     return email

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("パスワードが一致しません。")
    #     password_validation.validate_password(password2)
    #     return password2

    # def clean_userid(self):
    #     userid = self.cleaned_data.get('userid')
    #     if MyUser.objects.filter(userid=userid).exists():
    #         raise forms.ValidationError('こちらのユーザーIDはすでに使用されています。')
    #     return userid

    # def save(self, commit=True):
    #     # Save the provided password in hashed format
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data["password1"])
    #     if commit:
    #         user.save()
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