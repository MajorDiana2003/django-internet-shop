from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from typing import Union

from .models import Product, ContactInfo
from .forms import ProductForm

# Тип возвращаемого значения для редиректа или обычного ответа
ResponseResult = Union[HttpResponse, HttpResponse]


def home(request: HttpRequest) -> HttpResponse:
    """Контроллер для главной страницы — выводит все товары с пагинацией"""
    # Сортируем товары
    products_list = Product.objects.all().order_by('-created_at')

    # Выводим последние 5 товаров в консоль
    print("\n--- ПОСЛЕДНИЕ ТОВАРЫ В КОНСОЛИ ---")
    for prod in products_list[:5]:
        print(prod)
    print("-----------------------------------\n")

    # Настраиваем пагинацию: выводим ровно по 3 товара на одну страницу
    paginator = Paginator(products_list, 3)
    page_number: str | None = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})


def contacts(request: HttpRequest) -> HttpResponse:
    """Контроллер для страницы контактов"""
    if request.method == 'POST':
        name: str | None = request.POST.get('name')
        phone: str | None = request.POST.get('phone')
        message: str | None = request.POST.get('message')

        print("\n" + "=" * 40)
        print(" ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (DJANGO) ")
        print(f"Имя: {name} | Телефон: {phone}")
        print(f"Сообщение: {message}")
        print("=" * 40 + "\n")

    contact_data: ContactInfo | None = ContactInfo.objects.first()
    if not contact_data:
        contact_data = ContactInfo.objects.create(
            phone="+7 (999) 000-00-00",
            email="info@my-django-shop.ru",
            address="г. Шахты, ул. Программистов, д. 1"
        )

    return render(request, 'contacts.html', {'contact': contact_data})


def product_detail(request: HttpRequest, pk: int) -> HttpResponse:
    """Задание 1: Контроллер для детальной страницы товара"""
    product: Product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def product_create(request: HttpRequest) -> ResponseResult:
    """Дополнительное задание №1: Контроллер для создания товара через форму"""
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()

    return render(request, 'product_form.html', {'form': form})






