from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from captcha.fields import CaptchaField
from game_info_part.models import Article


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-input'}))

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}))

    password2 = forms.CharField(
        label='Повтор пароля',
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}))

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(
            attrs={'class': 'form-input'}))

    captcha = CaptchaField()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(
            attrs={'class': 'form-input'}))

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(
            attrs={'class': 'form-input'}))


class AddArticleForm(forms.ModelForm):
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_game'].empty_label = "Игра не выбрана"

    class Meta:
        model = Article
        fields = ['name_game', 'title', 'contains', 'preview_picture', 'is_published']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-input'}),
            'contains': forms.Textarea(
                attrs={'cols': 70, 'rows': 8}),
        }


class ChangeRating(forms.Form):
    CHOICES = [tuple([str(i), i]) for i in range(1, 11)]
    rating = forms.ChoiceField(label="Изменить рейтинг", choices=CHOICES)
