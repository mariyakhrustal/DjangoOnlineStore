from django.contrib.auth.forms import UserCreationForm
from django import forms

from users.models import User


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone", "avatar", "country"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs.update({
            'class': 'form-control',  # Добавление CSS-класса для стилизации поля
            'placeholder': 'Введите email'  # Текст подсказки внутри поля
        })

        self.fields['phone'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Введите номер телефона'
        })

        self.fields['avatar'].widget.attrs.update({
            'class': 'form-control',
        })

        self.fields['country'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Выберите страну'
        })
