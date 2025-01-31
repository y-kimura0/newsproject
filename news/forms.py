from django.forms import ModelForm
from .models import NewsPost
from django import forms

class NewsPostForm(ModelForm):
    class Meta:
        # モデルのクラス
        model = NewsPost
        # フォームで使用するモデルのフィールドを指定
        fields = ['category', 'title', 'comment', 'image1', 'image2']

class ContactForm(forms.Form):
    name = forms.CharField(label='お名前')
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='件名')
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = \
            'お名前(ユーザー名)を入力してください'
        self.fields['name'].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder'] = \
            'メールアドレスを入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control'

        self.fields['title'].widget.attrs['placeholder'] = \
            'タイトルを入力してください'
        self.fields['title'].widget.attrs['class'] = 'form-control'

        self.fields['message'].widget.attrs['placeholder'] = \
            'メッセージを入力してください'
        self.fields['message'].widget.attrs['class'] = ' form-control'

class DeleteRequestForm(forms.Form):
    name = forms.CharField(label='お名前')
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='件名', initial='削除申請', required=False, widget=forms.HiddenInput())
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'お名前(ユーザー名)を入力してください'
        self.fields['name'].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスを入力してください'
        self.fields['email'].widget.attrs['class'] = 'form-control'

        self.fields['message'].widget.attrs['placeholder'] = 'メッセージを入力してください'
        self.fields['message'].widget.attrs['class'] = ' form-control'

        # `title` をフォームで表示しないように設定
        self.fields['title'].initial = '削除申請'
        self.fields['title'].required = False  # `title` フィールドを必須ではなくする
