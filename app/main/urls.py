"""
URL configuration for app project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
#from django.views.decorators.cache import cache_page
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('delivery-payment/', views.DeliveryPaymentView.as_view(), name='delivery_payment'),
    path('contact-info/', views.ContactInfoView.as_view(), name='contact_info'),
]

# urlpatterns = [
#     path('', views.IndexView.as_view(), name='index'),
#     path('about/', cache_page(60)(views.AboutView.as_view()), name='about'),
# ]