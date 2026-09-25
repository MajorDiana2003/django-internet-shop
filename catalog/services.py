from django.core.cache import cache
from catalog.models import Product


def get_products_by_category(category_id):
    """Низкоуровневое кеширование списка продуктов по категории (Задание 3, 4)"""
    # Формируем ключ строго по критерию: category_{id}
    key = f'category_{category_id}'

    # Пытаемся достать список продуктов из Redis
    products_list = cache.get(key)

    # Если в Redis ничего нет, идем в базу данных PostgreSQL/SQLite
    if products_list is None:
        # Берем только опубликованные товары для этой категории
        products_list = list(Product.objects.filter(category_id=category_id, is_published=True))

        # Записываем полученный список в Redis с TTL (время жизни кеша) на 300 секунд (5 минут)
        cache.set(key, products_list, timeout=300)

    return products_list
