import requests
import telegram
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction
from django.forms import ValidationError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.conf import settings
from carts.models import Cart
from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem

# Инициализация Telegram-бота
bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)

class CreateOrderView(LoginRequiredMixin, FormView):
    template_name = 'orders/create_order.html'
    form_class = CreateOrderForm
    success_url = reverse_lazy('users:profile')

    def get_initial(self):
        initial = super().get_initial()
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        return initial

    def form_valid(self, form):
        try:
            with transaction.atomic():
                user = self.request.user
                cart_items = Cart.objects.filter(user=user)

                if cart_items.exists():
                    # Создать заказ
                    order = Order.objects.create(
                        user=user,
                        phone_number=form.cleaned_data['phone_number'],
                        requires_delivery=form.cleaned_data['requires_delivery'],
                        delivery_address=form.cleaned_data['delivery_address'] if form.cleaned_data['requires_delivery'] else '',
                        payment_on_get=form.cleaned_data['payment_on_get'],
                    )

                    # Инициализация списка для товаров
                    items = []
                    total_price = 0  # Инициализация общей суммы

                    # Создать заказанные товары
                    for cart_item in cart_items:
                        product = cart_item.product
                        name = cart_item.product.name
                        price = cart_item.product.sell_price()
                        quantity = cart_item.quantity

                        if product.quantity < quantity:
                            raise ValidationError(f'Недостаточное количество товара {name} на складе. В наличии - {product.quantity}')

                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            name=name,
                            price=price,
                            quantity=quantity,
                        )
                        product.quantity -= quantity
                        product.save()

                        items.append(f"{name} ({quantity} шт.)")
                        total_price += price * quantity  # Добавление стоимости товара к общей сумме

                    # Очистить корзину пользователя после создания заказа
                    cart_items.delete()

                    # Форматирование дополнительных данных заказа
                    requires_delivery = form.cleaned_data['requires_delivery'] == '1'  # Преобразование в логическое значение
                    delivery_method = "Нужна доставка" if requires_delivery else "Самовывоз"
                    payment_method = "Оплата картой" if form.cleaned_data['payment_on_get'] == '0' else "Наличными/картой при получении"
                    delivery_address = form.cleaned_data['delivery_address'] if requires_delivery else "Не указан"
                    phone_number = form.cleaned_data['phone_number']

                    # Создание сообщения для Telegram
                    message = (
                        f"Новый заказ от {user.username}!\n\n"
                        f"Телефон: {phone_number}\n"
                        f"Товары:\n" + "\n".join(items) + f"\n\n"
                        f"Общая сумма: {total_price} руб.\n"
                        f"Способ доставки: {delivery_method}\n"
                        f"Адрес доставки: {delivery_address}\n"
                        f"Способ оплаты: {payment_method}"
                    )

                    # Отправка сообщения в Telegram
                    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
                    payload = {'chat_id': settings.TELEGRAM_CHAT_ID, 'text': message}
                    response = requests.post(url, data=payload)

                    if response.status_code != 200:
                        raise Exception(f"Ошибка при отправке сообщения в Telegram: {response.text}")

                    # Отправка изображений товаров в Telegram
                    for cart_item in OrderItem.objects.filter(order=order):
                        product = cart_item.product
                        if product.image:  # Проверка на наличие изображения
                            with open(product.image.path, 'rb') as image_file:
                                photo_url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendPhoto"
                                photo_payload = {'chat_id': settings.TELEGRAM_CHAT_ID}
                                photo_files = {'photo': image_file}
                                photo_response = requests.post(photo_url, data=photo_payload, files=photo_files)

                            if photo_response.status_code != 200:
                                raise Exception(f"Ошибка при отправке изображения в Telegram: {photo_response.text}")

                    messages.success(self.request, 'Заказ оформлен!')
                    return redirect('user:profile')

        except ValidationError as e:
            messages.error(self.request, str(e))
            return redirect('orders:create_order')

    def form_invalid(self, form):
        messages.error(self.request, 'Заполните все обязательные поля!')
        return redirect('orders:create_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Оформление заказа'
        context['order'] = True
        return context




# @login_required
# def create_order(request):
#     if request.method == 'POST':
#         form = CreateOrderForm(data=request.POST)
#         if form.is_valid():
#             try:
#                 with transaction.atomic():
#                     user = request.user
#                     cart_items = Cart.objects.filter(user=user)
#
#                     if cart_items.exists():
#                         # Создать заказ
#                         order = Order.objects.create(
#                             user=user,
#                             phone_number=form.cleaned_data['phone_number'],
#                             requires_delivery=form.cleaned_data['requires_delivery'],
#                             delivery_address=form.cleaned_data['delivery_address'],
#                             payment_on_get=form.cleaned_data['payment_on_get'],
#                         )
#                         # Создать заказанные товары
#                         for cart_item in cart_items:
#                             product=cart_item.product
#                             name=cart_item.product.name
#                             price=cart_item.product.sell_price()
#                             quantity=cart_item.quantity
#
#
#                             if product.quantity < quantity:
#                                 raise ValidationError(f'Недостаточное количество товара {name} на складе\
#                                                        В наличии - {product.quantity}')
#
#                             OrderItem.objects.create(
#                                 order=order,
#                                 product=product,
#                                 name=name,
#                                 price=price,
#                                 quantity=quantity,
#                             )
#                             product.quantity -= quantity
#                             product.save()
#
#                         # Очистить корзину пользователя после создания заказа
#                         cart_items.delete()
#
#                         messages.success(request, 'Заказ оформлен!')
#                         return redirect('user:profile')
#             except ValidationError as e:
#                 messages.success(request, str(e))
#                 return redirect('orders:create_order')
#     else:
#         initial = {
#             'first_name': request.user.first_name,
#             'last_name': request.user.last_name,
#             }
#
#         form = CreateOrderForm(initial=initial)
#
#     context = {
#         'title': 'Home - Оформление заказа',
#         'form': form,
#         'order': True,
#     }
#     return render(request, 'orders/create_order.html', context=context)


# Предыдущая версия:
# class CreateOrderView(LoginRequiredMixin, FormView):
#     template_name = 'orders/create_order.html'
#     form_class = CreateOrderForm
#     success_url = reverse_lazy('users:profile')
#
#     def get_initial(self):
#         initial = super().get_initial()
#         initial['first_name'] = self.request.user.first_name
#         initial['last_name'] = self.request.user.last_name
#         return initial
#
#     def form_valid(self, form):
#         try:
#             with transaction.atomic():
#                 user = self.request.user
#                 cart_items = Cart.objects.filter(user=user)
#
#                 if cart_items.exists():
#                     # Создать заказ
#                     order = Order.objects.create(
#                         user=user,
#                         phone_number=form.cleaned_data['phone_number'],
#                         requires_delivery=form.cleaned_data['requires_delivery'],
#                         delivery_address=form.cleaned_data['delivery_address'],
#                         payment_on_get=form.cleaned_data['payment_on_get'],
#                     )
#                     # Создать заказанные товары
#                     for cart_item in cart_items:
#                         product = cart_item.product
#                         name = cart_item.product.name
#                         price = cart_item.product.sell_price()
#                         quantity = cart_item.quantity
#
#                         if product.quantity < quantity:
#                             raise ValidationError(f'Недостаточное количество товара {name} на складе\
#                                                        В наличии - {product.quantity}')
#
#                         OrderItem.objects.create(
#                             order=order,
#                             product=product,
#                             name=name,
#                             price=price,
#                             quantity=quantity,
#                         )
#                         product.quantity -= quantity
#                         product.save()
#
#                     # Очистить корзину пользователя после создания заказа
#                     cart_items.delete()
#
#                     messages.success(self.request, 'Заказ оформлен!')
#                     return redirect('user:profile')
#         except ValidationError as e:
#             messages.success(self.request, str(e))
#             return redirect('orders:create_order')
#
#     def form_invalid(self, form):
#         messages.error(self.request, 'Заполните все обязательные поля!')
#         return redirect('orders:create_order')
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Оформление заказа'
#         context['order'] = True
#         return context
#