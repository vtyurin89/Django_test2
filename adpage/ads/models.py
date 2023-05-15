from django.contrib.auth.models import AbstractUser
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from django.conf import settings

from ads.utils import get_timestamp_path


# Create your models here.


class AdditionalImage(models.Model):
    ad = models.ForeignKey('Ad', on_delete=models.CASCADE, verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path, verbose_name='Изображение')

    class Meta:
        verbose_name_plural = 'Дополнительные иллюстрации'
        verbose_name = 'Дополнительная иллюстрация'



class Ad(models.Model):
    title = models.CharField(max_length=255, verbose_name='Товар')
    slug = models.SlugField(max_length=260, unique=True, db_index=True, verbose_name='Slug-значение')
    content = models.TextField(blank=True, verbose_name='Описание')
    price = models.FloatField(blank=True, verbose_name='Цена')
    time_published = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, null=True, verbose_name='Категория')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    author = models.ForeignKey('AdUser', on_delete=models.CASCADE, verbose_name='Автор')
    image = models.ImageField(blank=True, upload_to=get_timestamp_path, verbose_name='Изображение')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_ad', kwargs={'ad_slug': self.slug})


    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)


    def correct_price(self):
        return "{:,.2f} ₽".format(self.price)

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-time_published']


class Category(models.Model):
    title = models.CharField(max_length=100, db_index=True, verbose_name='Название')
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name='URL')
    super_category = models.ForeignKey('SuperCategory', blank=True, null=True, on_delete=models.PROTECT, verbose_name='Родительская категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'


class AdUser(AbstractUser):
    is_active = models.BooleanField(default=True, db_index=True, verbose_name='Активация пройдена?')

    def delete(self, *args, **kwargs):
        for ad in self.ad_set.all():
            ad.delete()
        super().delete(*args, **kwargs)

    class Meta(AbstractUser.Meta):
        pass


class SuperCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(Category):
    objects = SuperCategoryManager()

    def __str__(self):
        return self.title

    class Meta:
        proxy = True
        verbose_name = 'Родительская категория'
        verbose_name_plural = 'Родительские категории'


class SubCategoryManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubCategory(Category):
    objects = SubCategoryManager()

    def __str__(self):
        return '%s - %s' % (self.super_category.title, self.title)

    class Meta:
        proxy = True
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'