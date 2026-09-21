from django.db import models


class Category(models.Model):
    name: models.CharField = models.CharField(max_length=100, verbose_name="Наименование")
    description: models.TextField = models.TextField(verbose_name="Описание", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self) -> str:
        return str(self.name)


class Product(models.Model):
    name: models.CharField = models.CharField(max_length=150, verbose_name="Наименование")
    description: models.TextField = models.TextField(verbose_name="Описание", blank=True, null=True)
    image: models.ImageField = models.ImageField(upload_to="products/", verbose_name="Изображение", blank=True, null=True)
    category: models.ForeignKey = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price: models.IntegerField = models.IntegerField(verbose_name="Цена за покупку")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата последнего изменения")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self) -> str:
        return str(self.name)


class ContactInfo(models.Model):
    phone: models.CharField = models.CharField(max_length=50, verbose_name="Телефон")
    email: models.EmailField = models.EmailField(verbose_name="Email")
    address: models.TextField = models.TextField(verbose_name="Адрес")

    class Meta:
        verbose_name = "Контактная информация"
        verbose_name_plural = "Контактная информация"

    def __str__(self) -> str:
        return f"Контакты: {self.phone}"


