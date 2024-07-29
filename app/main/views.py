from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    context = {
        'title': 'Home - Главная',
        'content':"Магазин цветов FLOWERS",

    }

    return render(request, 'main/index.html', context)

def about(request):
    return HttpResponse("About page")