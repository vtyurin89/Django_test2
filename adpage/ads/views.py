from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetCompleteView
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView

from .forms import *
from .models import *
from .utils import *


def page_not_found(request, exception):
    return HttpResponseNotFound("Страница не найдена")


class AdHomepage(DataMixin, ListView):
    model = Ad
    context_object_name = 'ads'
    template_name = 'ads/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Главная страница', in_menu=1)
        return context | c_def

    def get_queryset(self):
        return Ad.objects.filter(is_published=True).select_related('cat')


class AdNew(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'ads/new.html'
    success_url = reverse_lazy('index')
    login_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Добавить объявление', in_menu=2)
        return context | c_def


def help(request):
    context = {'menu': menu}
    return render(request, 'ads/help.html', context)


def search(request):
    if request.method == 'GET':
        searched = request.GET['search-bar']
        title = f'Результаты поиска: {str(searched)}'
        if searched:
            ads = Ad.objects.filter(title__icontains=searched)
            context = {'menu': menu, 'title': title, 'ads': ads}
            return render(request, 'ads/search.html', context)
        else:
            zero_query = True
            context = {'menu': menu, 'title': title, 'zero_query': zero_query}
            return render(request, 'ads/search.html', context)
    else:
        context = {'menu': menu, 'title': 'Результаты поиска:'}
        return render(request, 'ads/search.html', context)


def about(request):
    context = {'menu': menu, 'title': 'О сайте', 'in_menu': 3}
    return render(request, 'ads/about.html', context)


class AdShow(DataMixin, DetailView):
    model = Ad
    template_name = 'ads/show_ad.html'
    slug_url_kwarg = 'ad_slug'
    context_object_name = 'ad'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['ad'].title)
        context['ad_cat'] = context['ad'].cat
        return context | c_def


class AdCategory(DataMixin, ListView):
    model = Ad
    template_name = 'ads/category.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cat_obj = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title='Объявления в категории: ' + str(cat_obj.title))
        return context | c_def


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy('login')
    template_name = 'ads/register.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return context | c_def

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'ads/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return context | c_def

    def get_success_url(self):
        return reverse_lazy('index')


def logout_user(request):
    logout(request)
    return redirect('login')


class AskPasswordReset(PasswordResetView):
    form_class = AskPasswordResetForm
    subject_template_name = 'ads/email/reset_subject.txt'
    email_template_name = 'ads/email/reset_email_body.txt'
    template_name = 'ads/ask_password_reset.html'
    success_url = reverse_lazy('password_reset_email_sent')
    extra_context = {'menu': menu}


class AskPasswordResetDone(PasswordResetDoneView):
    template_name = 'ads/ask_password_reset_done.html'
    extra_context = {'menu': menu}


class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'ads/password_reset.html'
    form_class = DoPasswordResetForm
    post_reset_login = True
    success_url = reverse_lazy('password_reset_complete')
    extra_context = {'menu': menu}


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'ads/password_reset_complete.html'
    extra_context = {'menu': menu}


class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'ads/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return context | c_def

    def form_valid(self, form):
        return redirect('index')