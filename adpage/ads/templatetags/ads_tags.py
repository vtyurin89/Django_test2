from django import template

from ads.models import *

register = template.Library()


@register.simple_tag()
def get_categories():
    return Category.objects.all()