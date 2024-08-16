from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView

from goods.models import Categories

class IndexView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - Главная'
        context['content'] = "Магазин цветов FLOWERS"
        return context

class AboutView(TemplateView):
    template_name = 'main/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home - О нас'
        context['content'] = "О нас"
        context['text_on_page'] = ("В нашем магазине всегда самые свежие и красивые цветы. "
                                   "Вы всегда можете подобрать в нашем магазине любые цветы, "
                                   "букеты, корзины цветов на любой вкус. Мы очень стараемся, "
                                   "что бы удовлетворить Ваши желания. Приходите в наш магазин и "
                                   "Вы останетесь очень довольны.")
        return context

# ПРЕДЫДУЩАЯ ВЕРСИЯ:

# def index(request):
#
#     context = {
#         'title': 'Home - Главная',
#         'content':"Магазин цветов FLOWERS",
#     }
#
#     return render(request, 'main/index.html', context)

# def about(request):
#     context = {
#         'title': 'Home - О нас',
#         'content': "О нас",
#         'text_on_page': "В нашем магазине всегда самые свежие и красивые цветы. "
#                         "Вы всегда можете подобрать в нашем магазине любые цветы, букеты, корзины цветов"
#                         " на любой вкус. Мы очень стараемся, что бы удовлетворить Ваши желания. "
#                         "Приходите в наш магазин и Вы останетесь очень довольны."
#     }
#
#     return render(request, 'main/about.html', context)
