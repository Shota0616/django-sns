from django import forms


from app.models import Tweet, Comment


class TweetForm(forms.ModelForm):
    text = forms.CharField(max_length=300,
        widget=forms.Textarea(
        attrs={'class':'form-control'}))

    class Meta:
        model = Tweet
        fields = ['text']

    # # djangoデフォルトのバリデーションメッセージを表示したくないので、required = False
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.required = False

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('何も入力されていません。')
        return text

# ユーザー編集フォーム
class TweetEditForm(forms.ModelForm):
    text = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Tweet
        fields = ['text']

    # # djangoデフォルトのバリデーションメッセージを表示したくないので、required = False
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for field in self.fields.values():
    #         field.required = False

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == "":
            raise forms.ValidationError('入力してください。')
        return text

class CommentForm(forms.ModelForm):
    text = forms.CharField(max_length=300, widget=forms.Textarea(attrs={'class':'form-control'}))

    class Meta:
        model = Comment
        fields = ['text']

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if text == "":
            raise forms.ValidationError('入力してください。')
        return text