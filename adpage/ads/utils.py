from django.db.models import Count
from .models import *

menu = [{'title':"Главная страница", 'url_name': 'index', 'menu_pos': 1},
        {'title':"Добавить объявление", 'url_name': 'new', 'menu_pos': 2},
        {'title':"О сайте", 'url_name': 'about', 'menu_pos': 3},]

profile_sidebar = [{'title': "Мои объявления", 'url_name': 'profile_myads', 'sidebar_pos': 1},
                   {'title': "Редактировать профиль", 'url_name': 'profile_edit', 'sidebar_pos': 2},
                   {'title': "Настройки безопасности", 'url_name': 'profile_change_password', 'sidebar_pos': 3},
]

class DataMixin:
    #pagination
    paginate_by = 12

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('ad'))
        context['menu'] = menu
        context['profile_sidebar'] = profile_sidebar
        context['cats'] = cats
        return context

