# В этом файле будут храниться пользовательские шаблонные теги:
from django import template
from django.utils.http import urlencode
from ..models import Categories


register = template.Library() # Регистрация шаблонного тега который ниже с помощью декоратора:
@register.simple_tag()
def tag_categories(): # Фукция которая возвращает "Категории" на странице, по этому имени в шаблоне вернется 'Categories.objects.all()'
    return Categories.objects.all()

@register.simple_tag(takes_context=True)
def change_params(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(**kwargs)
    return urlencode(query)