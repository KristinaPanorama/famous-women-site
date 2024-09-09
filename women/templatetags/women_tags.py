from django import template
from django.db.models import Count

from ..models import Category, TagPost
from ..utils import menu


register = template.Library()


@register.simple_tag
def get_menu():
    return menu


@register.inclusion_tag('women/cat_list.html', name='categories')
def get_categories(cat_selected=0):
    cats = Category.objects.annotate(total=Count('posts')).filter(total__gt=0)
    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('women/tag_list.html', name='tag_list')
def get_tag_list():
    return {'tags': TagPost.objects.annotate(total=Count('tags')).filter(total__gt=0)}

