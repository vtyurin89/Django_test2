from django.db import models
from django.urls import reverse


# Create your models here.
class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name='Товар')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='Slug-значение')
    content = models.TextField(blank=True, verbose_name='Описание')
    price = models.FloatField(blank=True, verbose_name='Цена')
    time_published = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_ad', kwargs={'ad_slug': self.slug})

    def correct_price(self):
        return "{:,.2f} ₽".format(self.price)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-time_published']


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'