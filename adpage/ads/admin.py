from django.contrib import admin

# Register your models here.
from .models import *


class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'time_published', 'cat', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_published', 'cat')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}



admin.site.register(Ad, AdAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AdUser)

admin.site.site_header = 'Панель администратора'
admin.site.site_title = 'Панель администратора'