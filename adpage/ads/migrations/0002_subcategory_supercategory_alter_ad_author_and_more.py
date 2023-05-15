# Generated by Django 4.2 on 2023-05-12 10:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubCategory',
            fields=[
            ],
            options={
                'verbose_name': 'Подкатегория',
                'verbose_name_plural': 'Подкатегории',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ads.category',),
        ),
        migrations.CreateModel(
            name='SuperCategory',
            fields=[
            ],
            options={
                'verbose_name': 'Родительская категория',
                'verbose_name_plural': 'Родительские категории',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('ads.category',),
        ),
        migrations.AlterField(
            model_name='ad',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор'),
        ),
        migrations.AddField(
            model_name='category',
            name='super_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ads.supercategory', verbose_name='Родительская категория'),
        ),
    ]
