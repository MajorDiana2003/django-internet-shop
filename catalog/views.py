from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, View

from .forms import ProductForm
from .models import ContactInfo, Product


class ProductListView(ListView):
    """CBV для главной страницы со списком товаров и пагинацией"""

    model = Product
    template_name = "index.html"
    context_object_name = "page_obj"  # сохраняем имя переменной для шаблона
    paginate_by = 3

    def get_queryset(self) -> Any:
        """Получаем отсортированный список всех доступных товаров"""
        queryset = super().get_queryset().order_by("-created_at")

        # Сохраняем логику вывода в консоль из прошлых заданий
        print("\n--- ПОСЛЕДНИЕ ТОВАРЫ В КОНСОЛИ (CBV) ---")
        for prod in queryset[:5]:
            print(prod)
        print("-----------------------------------------\n")

        return queryset


class ContactsView(View):
    """CBV для страницы контактов с обработкой GET и POST методов"""

    def get(self, request: HttpRequest) -> HttpResponse:
        contact_data: ContactInfo | None = ContactInfo.objects.first()
        if not contact_data:
            contact_data = ContactInfo.objects.create(
                phone="+7 (999) 000-00-00",
                email="info@my-django-shop.ru",
                address="г. Шахты, ул. Программистов, д. 1",
            )
        return render(request, "contacts.html", {"contact": contact_data})

    def post(self, request: HttpRequest) -> HttpResponse:
        name: str | None = request.POST.get("name")
        phone: str | None = request.POST.get("phone")
        message: str | None = request.POST.get("message")

        print("\n" + "=" * 40)
        print(" ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (CBV) ")
        print(f"Имя: {name} | Телефон: {phone}")
        print(f"Сообщение: {message}")
        print("=" * 40 + "\n")

        return self.get(request)


class ProductDetailView(DetailView):
    """CBV для детальной страницы отдельного товара"""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(CreateView):
    """CBV для создания нового товара через валидируемую форму"""

    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")
