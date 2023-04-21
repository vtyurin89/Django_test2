from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *

class AddPostForm(forms.ModelForm):
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
   captcha = CaptchaField(label='Код с картинки')

   class Meta:
       model = Ad
       fields = ['title', 'slug', 'content', 'price', 'cat']
       widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                  'slug': forms.TextInput(attrs={'class': 'form-control'}),
                  'content': forms.Textarea(attrs={'class': 'form-control'}),
                  'price': forms.TextInput(attrs={'class': 'form-control'}),
                  'cat': forms.Select(attrs={'class': 'form-select'}),
}

   def clean_title(self):
       title = self.cleaned_data['title']
       if len(title) > 200:
           raise ValidationError('Максимальная длина названия - 200 символов')
       return title


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    captcha = CaptchaField(label='Код с картинки')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Сообщение', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-control', 'placeholder': 'О чём вы хотели бы нам сообщить?'}))
    captcha = CaptchaField(label='Код с картинки')