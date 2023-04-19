from django.db.models import Count
from .models import *

menu = [{'title':"Главная страница", 'url_name': 'index'},
        {'title':"Дать объявление", 'url_name': 'new'},
        {'title':"Помощь", 'url_name': 'help'},
        {'title':"О сайте", 'url_name': 'about'},]

class DataMixin:
    #pagination
    paginate_by = 10

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('ad'))
        context['menu'] = menu
        context['cats'] = cats
        return context

