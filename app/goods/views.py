# from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, ListView

from .models import Products, Review
from .utils import q_search
from .forms import ReviewForm


class CatalogView(ListView):
    model = Products
    # queryset = Products.objects.all().order_by("-id")
    template_name = "goods/catalog.html"
    context_object_name = "goods"
    paginate_by = 3
    allow_empty = False
    # чтоб удобно передать в методы
    slug_url_kwarg = "category_slug"

    def get_queryset(self):
        category_slug = self.kwargs.get(self.slug_url_kwarg)
        on_sale = self.request.GET.get("on_sale")
        order_by = self.request.GET.get("order_by")
        query = self.request.GET.get("q")

        if category_slug == "all":
            goods = super().get_queryset()
        elif query:
            goods = q_search(query)
        else:
            goods = super().get_queryset().filter(category__slug=category_slug)
            if not goods.exists():
                raise Http404()

        if on_sale:
            goods = goods.filter(discount__gt=0)

        if order_by and order_by != "default":
            goods = goods.order_by(order_by)

        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home - Каталог"
        context["slug_url"] = self.kwargs.get(self.slug_url_kwarg)
        context["rating_range"] = range(1, 6)  # Добавляем диапазон в контекст
        return context


class ProductView(DetailView):
    model = Products
    template_name = "goods/product.html"
    context_object_name = "product"
    slug_field = 'slug'
    slug_url_kwarg = "product_slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ReviewForm()
        context['reviews'] = self.object.reviews.all()
        context['rating_range'] = range(1, 6)  # Передача диапазона 1-5 в контекст
        return context

    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        product = self.get_object()

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user  # Привязываем отзыв к текущему пользователю
            review.save()
            return redirect(product.get_absolute_url())

        return self.get(request, *args, **kwargs)

# class ProductView(DetailView):
#     # model = Products      # В этом случае будет выборка всех карт товаров, а нам нужно конкретную.
#     # slug_field = "slug"
#     template_name = "goods/product.html"
#     slug_url_kwarg = "product_slug"    # Значение ключ, получить значение по конвертору 'urls.py:
#     context_object_name = "product"
#
#     def get_object(self, queryset=None):
#         product = Products.objects.get(slug=self.kwargs.get(self.slug_url_kwarg))
#         return product
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["title"] = self.object.name
#         context["range"] = range(1, 6)
#         return context


# ПРЕДЫДУЩАЯ ВЕРСИЯ:

# def catalog(request, category_slug=None):
#
#     page = request.GET.get('page', 1)
#     on_sale = request.GET.get('on_sale', None)
#     order_by = request.GET.get('order_by', None)
#     query = request.GET.get('q', None)
#
#     if category_slug == 'all':
#         goods = Products.objects.all()
#     elif query:
#         goods = q_search(query)
#     else:
#         goods = Products.objects.filter(category__slug=category_slug)
#         if not goods.exists():
#             raise Http404()
#
#     if on_sale:
#         goods = goods.filter(discount__gt=0)
#
#     if order_by and order_by != "default":
#         goods = goods.order_by(order_by)
#
#     paginator = Paginator(goods,3)
#     current_page = paginator.page(int(page))
#
#     context = {
#         "title": "Home - Каталог",
#         "goods": current_page,
#         "slug_url": category_slug
#     }
#     return render(request, 'goods/catalog.html', context)



# def product(request, product_slug):
#     product = Products.objects.get(slug=product_slug)
#
#     context = {'product': product}
#
#     return render(request, "goods/product.html", context)