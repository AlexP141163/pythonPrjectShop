from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Home - Главная',
        'content':"Магазин цветов FLOWERS",
    }

    return render(request, 'main/index.html', context)

def about(request):
    context = {
        'title': 'Home - О нас',
        'content': "О нас",
        'text_on_page': "В нашем магазине всегда самые свежие и красивые цветы. "
                        "Вы всегда можете подобрать в нашем магазине любые цветы, букеты, корзины цветов"
                        " на любой вкус. Мы очень стараемся, что бы удовлетворить Ваши желания. "
                        "Приходите в наш магазин и Вы останетесь очень довольны."
    }

    return render(request, 'main/about.html', context)
