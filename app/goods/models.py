from django.db import models

# Сздаем две таблицы: Categores и Products, by 'Class Meta: caterory and product (таблицы в базе должны быть
# в единственном числе, это достигается строкой 'Class Meta: db_table', если этого не делать то таблицы в базе
# назовутся по имени класса, а именно, в данном случае " categories and products)
class Categories(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')

    class Meta:
        db_table = 'category' # Имя таблицы в базе данных в единственном !!! числе:
        verbose_name = 'Категорию' # Имя будет отображаться в admin - панеле на русском языке в едиственном числе:
        verbose_name_plural = 'Категории'  # Имя будет отображаться в admin-панеле на русском языке во множественном числе:

    def __str__(self):
        return self.name # Возвращает правильное название созданной новой группы категории:


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='goods_images',blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=7, decimal_places=2, verbose_name='Цена')
    discount = models.DecimalField(default=0.00, max_digits=4, decimal_places=2, verbose_name='Скидка в %')
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    category = models.ForeignKey(to=Categories, on_delete=models.CASCADE, verbose_name='Категория')


    class Meta:
        db_table = 'product' # Имя таблицы в базе данных в единственном !!! числе:
        verbose_name = 'Продукт' # Имя будет отображаться в admin - панеле на русском языке в едиственном числе:
        verbose_name_plural = 'Продукты'  # Имя будет отображаться в admin-панеле на русском языке во множественном числе:

    def __str__(self):   # Возвращает правильное название созданной нового товара:
        return f'{self.name} Количество - {self.quantity}'

    def display_id(self):
        return f"{self.id:05}" # Возвращает 'id' товара и дописывает нули с начала, чтобы було 5 цыфрЖ

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price*self.discount/100, 2)

        return self.price