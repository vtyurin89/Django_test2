from django.db.models import Count
from .models import *

menu = [{'title':"Главная страница", 'url_name': 'index', 'menu_pos': 1},
        {'title':"Добавить объявление", 'url_name': 'new', 'menu_pos': 2},
        {'title':"О сайте", 'url_name': 'about', 'menu_pos': 3},]

class DataMixin:
    #pagination
    paginate_by = 12

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('ad'))
        context['menu'] = menu
        context['cats'] = cats
        return context

