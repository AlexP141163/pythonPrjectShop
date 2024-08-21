import os
import csv
from datetime import datetime
from django.contrib import admin
from django.db.models import Sum
from django.http import HttpResponse
from django.conf import settings
from orders.models import Order, OrderItem


class OrderItemTabularAdmin(admin.TabularInline):
    model = OrderItem
    fields = "product", "name", "price", "quantity"
    search_fields = (
        "product",
        "name",
    )
    extra = 0


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = "order", "product", "name", "price", "quantity", "total_price"
    search_fields = (
        "order",
        "product",
        "name",
    )
    list_filter = (
        ("order__created_timestamp", admin.DateFieldListFilter),
    )
    actions = ['export_as_csv']

    def total_price(self, obj):
        return obj.price * obj.quantity

    total_price.short_description = 'Total Price'
    total_price.admin_order_field = 'total_price'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)
        try:
            qs = response.context_data['cl'].queryset
            total = qs.aggregate(Sum('price'))['price__sum'] or 0
            response.context_data['total_sum'] = total
        except (AttributeError, KeyError):
            pass
        return response

    def export_as_csv(self, request, queryset):
        # Генерация имени файла с текущей датой и временем
        filename = f"orders_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        # Путь к директории, где будет сохранен файл (например, папка 'exports' в корне проекта)
        export_dir = os.path.join(settings.BASE_DIR, 'exports')

        # Проверка существования директории, создание, если не существует
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)

        # Полный путь к файлу
        file_path = os.path.join(export_dir, filename)

        # Подсчеты для итоговых данных
        total_quantity = 0
        total_sum = 0

        # Создание CSV файла и запись данных
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Order ID', 'Product', 'Name', 'Price', 'Quantity', 'Total Price'])

            for order_item in queryset:
                quantity = order_item.quantity
                total_price = order_item.price * quantity

                writer.writerow([
                    order_item.order.id,
                    order_item.product,
                    order_item.name,
                    order_item.price,
                    quantity,
                    total_price,
                ])

                # Подсчет общей суммы и количества
                total_quantity += quantity
                total_sum += total_price

            # Добавление итоговых данных в конец файла
            writer.writerow([])
            writer.writerow(['', '', '', 'Total:', total_quantity, total_sum])

        # Подготовка файла для загрузки пользователем
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'

        with open(file_path, 'r', encoding='utf-8') as csvfile:
            response.write(csvfile.read())

        return response

class OrderTabulareAdmin(admin.TabularInline):
    model = Order
    fields = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    search_fields = (
        "requires_delivery",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    readonly_fields = ("created_timestamp",)
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
        "created_timestamp",
    )
    search_fields = (
        "id",
    )
    readonly_fields = ("created_timestamp",)
    list_filter = (
        "requires_delivery",
        "status",
        "payment_on_get",
        "is_paid",
    )
    inlines = (OrderItemTabularAdmin,)