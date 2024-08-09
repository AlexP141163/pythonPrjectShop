# Register your models here.

from django.contrib import admin
from .models import Categories, Products

#admin.site.register(Categories)
#admin.site.register(Products)

@admin.register(Categories)
class CategoriesAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # 'prepopulated_fields' - поля которые будут заполняться автоматически:

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)} # 'prepopulated_fields' - поля которые будут заполняться автоматически:
    list_display = ['name', 'quantity','price', 'discount']
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
    ]
