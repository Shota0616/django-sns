from django import forms
from django.contrib.auth import password_validation

from allauth.account.forms import SignupForm

from user.utils import generate_unique_id
from user.models import User


# ユーザー編集フォーム
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
    profile_image = forms.ImageField(required=False)

    # djangoデフォルトのバリデーションメッセージを表示したくないので、required = False
    def __init__(self, *args, **kwargs):
        # instance引数を取得し、存在しなければNoneをデフォルト値とする
        self.instance = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    # バリデーション
    def clean_userid(self):
        userid = self.cleaned_data.get('userid')
        if not userid:
            raise forms.ValidationError("ユーザーIDは必須です。")
    # 自身のIDと入力されたIDが同一でなく、入力されたIDが既に存在する場合にエラーを出す
        if self.instance.userid != userid and User.objects.filter(userid__iexact=userid).exists():
            raise forms.ValidationError('こちらのユーザーIDはすでに使用されています。')
        return userid

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if not nickname:
            raise forms.ValidationError('名前は必須です。')
        return nickname

    def save(self, user_data):
        user_data.userid = self.cleaned_data['userid']
        user_data.nickname = self.cleaned_data['nickname']
        user_data.introduction = self.cleaned_data['introduction']
        if 'profile_image' in self.files:
            user_data.profile_image = self.cleaned_data['profile_image']
        user_data.save()
        return user_data


# ユーザー登録フォーム
class MyCustomSignupForm(SignupForm):
    email = forms.EmailField(
        max_length=255,
        error_messages={'invalid': '有効なメールアドレスを入力してください。'},
        label='メールアドレス',
        widget=forms.TextInput(attrs={'type':'email', 'name':'login', "autocomplete":"email", 'placeholder':'メールアドレス', 'class':'form-control'})
    )
    password1 = forms.CharField(
        max_length=128,
        label='パスワード',
        widget=forms.PasswordInput(attrs={'placeholder':'パスワード', 'class':'form-control'})
    )
    password2 = forms.CharField(
        max_length=128,
        label='パスワード確認',
        widget=forms.PasswordInput(attrs={'placeholder':'パスワード確認', 'class':'form-control'})
    )
    userid = forms.CharField(
        initial=generate_unique_id,
        max_length=15,
        label='ユーザーID',
        widget=forms.TextInput(attrs={'placeholder':'ユーザーID', 'class':'form-control'})
    )
    nickname = forms.CharField(
        max_length=30,
        label='名前',
        widget=forms.TextInput(attrs={'placeholder':'名前', 'class':'form-control'})
    )
    introduction = forms.CharField(
        max_length=1000,
        label='自己紹介',
        widget=forms.Textarea(attrs={'placeholder':'自己紹介', 'class':'form-control'})
    )
    profile_image = forms.ImageField(
        label='プロフィール画像',
    )

    # djangoデフォルトのバリデーションメッセージを表示したくないので、required = False
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    # バリデーション
    def clean_userid(self):
        userid = self.cleaned_data.get('userid')
        if not userid:
            raise forms.ValidationError("ユーザーIDは必須です。")
        if User.objects.filter(userid__iexact=userid).exists():
            raise forms.ValidationError('こちらのユーザーIDはすでに使用されています。')
        return userid

    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if not nickname:
            raise forms.ValidationError('名前は必須です。')
        return nickname

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("メールアドレスは必須です。")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("こちらのメールアドレスは既に登録済みです.")
        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if not password1:
            raise forms.ValidationError("パスワードは必須です。")
        password_validation.validate_password(password1)
        return password1

    def clean(self):
        cleaned_data = super().clean()

        password1 = cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if not password2:
            raise forms.ValidationError("確認用パスワードも入力してください。")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("パスワードが一致しません。")
        # パスワードのdjango側のバリデーションチェック
        password_validation.validate_password(password1, password2)

        return cleaned_data

    def save(self, request):
        user = super().save(request)

        user.userid = self.cleaned_data['userid']
        user.nickname = self.cleaned_data['nickname']
        user.introduction = self.cleaned_data['introduction']
        if 'profile_image' not in self.files:
            user.profile_image = 'common/default.png'
        else:
            user.profile_image = self.cleaned_data['profile_image']
        user.save()

        return user
