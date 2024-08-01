# В этом файле будут храниться пользовательские шаблонные теги:
from django import template

from goods.models import Categories


register = template.Library() # Регистрация шаблонного тега который ниже с помощью декоратора:
@register.simple_tag()
def tag_categories(): # Фукция которая возвращает "Категории" на странице, по этому имени в шаблоне вернется 'Categories.objects.all()'
    return Categories.objects.all()