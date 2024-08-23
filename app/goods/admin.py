# Register your models here.

from django.contrib import admin
from .models import Categories, Products, Review

#admin.site.register(Categories)
#admin.site.register(Products)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # 'prepopulated_fields' - поля которые будут заполняться автоматически:

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # 'prepopulated_fields' - поля которые будут заполняться автоматически:
    list_display = ['name', 'quantity','price', 'discount', 'rating']
    list_editable = ['discount', 'price', 'quantity']
    search_fields = ['name', 'description']
    list_filter = ['discount', 'quantity', 'category']
    fields = [
        "name",
        "category",
        "slug",
        "description",
        "image",
        ("price", "discount"),
        "quantity",
        "rating",  # Добавлено поле rating в форму редактирования
    ]

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'rating', 'created_at']
    search_fields = ['product__name', 'user__username']

