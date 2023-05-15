from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm, \
    PasswordChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import *


class AddPostForm(forms.ModelForm):
   def __init__(self, *args, **kwargs):
       self.author_id = kwargs.pop('user_id', None)
       super(AddPostForm, self).__init__(*args, **kwargs)

   cat = forms.ModelChoiceField(queryset=Category.objects.filter(super_category__isnull=False), label='Категория',
                                widget=forms.Select(attrs={'class': 'form-select'}))
   captcha = CaptchaField(label='Код с картинки')

   class Meta:
       model = Ad
       fields = ['title', 'content', 'price', 'cat', 'image']
       widgets = {'title': forms.TextInput(attrs={'class': 'form-control'}),
                  'content': forms.Textarea(attrs={'class': 'form-control'}),
                  'price': forms.TextInput(attrs={'class': 'form-control'}),
                  'image': forms.FileInput(attrs={'class': 'form-control'})
}

   def clean_title(self):
       title = self.cleaned_data['title']
       if len(title) > 200:
           raise ValidationError('Максимальная длина названия - 200 символов')
       return title

   def save(self, commit=True, **kwargs):
       my_form_object = super(AddPostForm, self).save(commit=False)
       new_title = my_form_object.title.translate(
           str.maketrans(
               "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
               "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"))
       new_slug = slugify(new_title)
       check_ad = Ad.objects.filter(slug=new_slug)
       if check_ad.exists():
           my_form_object.slug = f"{new_slug}_{check_ad.count() + 1}"
       else:
           my_form_object.slug = new_slug
       my_form_object.author_id = self.author_id
       if commit:
           my_form_object.save()
       return my_form_object


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))
    captcha = CaptchaField(label='Код с картинки')

    def clean(self):
        super().clean()
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 and password2 and password1 != password2:
            errors = {'password2': ValidationError('Введённые пароли не совпадают', code='password_mismatch')}
            raise ValidationError(errors)

    class Meta:
        model = AdUser
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))


class AskPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email',
                             widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'E-mail'}))


class DoPasswordResetForm(SetPasswordForm):
    new_password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Новый пароль'}))
    new_password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'}))



class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Сообщение',
                              widget=forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-control',
                                                           'placeholder': 'О чём вы хотели бы нам сообщить?'}))
    captcha = CaptchaField(label='Код с картинки')


class ChangeUserDataForm(forms.ModelForm):
    email = forms.EmailField(required=True, label='E-mail', widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label='Фамилия', max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = AdUser
        fields = ('email', 'first_name', 'last_name')


class ProfileChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label='Старый пароль', max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label='Новый пароль', max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label='Повторите пароль', max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class SubCategoryForm(forms.ModelForm):
    super_category = forms.ModelChoiceField(queryset=SuperCategory.objects.all(), empty_label=None, label='Родительская категория', required=True)

    class Meta:
        model = SubCategory
        fields = '__all__'

