from django.contrib import admin

# Register your models here.
from .models import *
from .forms import SubCategoryForm


class AdditionalImageInline(admin.TabularInline):
    model = AdditionalImage


class AdAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'time_published', 'cat', 'author', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_published', 'cat')
    inlines = (AdditionalImageInline, )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('super_category__title',)


class AdUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    fields = (('username', 'email'), ('first_name', 'last_name'),
              ('is_staff',), ('is_superuser',),
              'groups', 'user_permissions',
              ('last_login',), ('date_joined',))
    readonly_fields = ('last_login', 'date_joined')


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    prepopulated_fields = {'slug': ('title',)}


class SuperCategoryAdmin(admin.ModelAdmin):
    exclude = ('super_category',)
    inlines = (SubCategoryInline,)
    prepopulated_fields = {'slug': ('title',)}


class SubCategoryAdmin(admin.ModelAdmin):
    form = SubCategoryForm
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('super_category__title',)


admin.site.register(Ad, AdAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(AdUser, AdUserAdmin)
admin.site.register(SuperCategory, SuperCategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)

admin.site.site_header = 'Панель администратора'
admin.site.site_title = 'Панель администратора'