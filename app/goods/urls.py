from django.urls import path
from .views import ProductView
from . import views

app_name = 'goods'

urlpatterns = [
    path('product/<slug:product_slug>/', ProductView.as_view(), name='product'),
    path('search/', views.CatalogView.as_view(), name='search'),
    path('<slug:category_slug>/', views.CatalogView.as_view(), name='index'),
    path('product/<slug:product_slug>/', views.ProductView.as_view(), name='product'),
]
