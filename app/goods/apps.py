from django.apps import AppConfig


class GoodsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'goods'
    verbose_name = 'Товары' # Вместо 'goods' будет отображаться в 'admin-penal'- "Товары" на русском языке.
