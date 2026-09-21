from django.contrib import admin
from catalog.models import Category, Product, ContactInfo

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройка панели администратора для категорий"""
    list_display = ('id', 'name',)  # Выводим ID и название


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Настройка панели администратора для продуктов"""
    list_display = ('id', 'name', 'price', 'category',)  # Выводим ID, название, цену и категорию
    list_filter = ('category',)  # Добавляем фильтрацию по категории
    search_fields = ('name', 'description',)  # Добавляем поиск по названию и описанию


# Регистрируем модель контактов, чтобы её тоже можно было редактировать в админке
@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone', 'email', 'address',)

