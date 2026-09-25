from django.core.exceptions import PermissionDenied

from django.contrib.auth.mixins import LoginRequiredMixin

from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
    View,
)

from .forms import ProductForm
from .models import ContactInfo, Product
from catalog.services import get_products_by_category


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


class ProductDetailView(LoginRequiredMixin, DetailView):
    """CBV для детальной страницы отдельного товара"""

    model = Product
    template_name = "product_detail.html"
    context_object_name = "product"


class ProductCreateView(LoginRequiredMixin, CreateView):
    """CBV для создания нового товара через валидируемую форму"""

    model = Product
    form_class = ProductForm
    template_name = "product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """CBV для редактирования существующего товара."""

    model = Product
    form_class = ProductForm
    template_name = "product_form.html"

    def get_success_url(self) -> str:
        return reverse("catalog:product_detail", kwargs={"pk": self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner == request.user or request.user.has_perm('catalog.can_unpublish_product'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied



class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """CBV для удаления товара."""

    model = Product
    template_name = "product_confirm_delete.html"
    success_url = reverse_lazy("catalog:home")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.owner == request.user or request.user.has_perm('catalog.delete_product'):
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied


class CategoryProductsListView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        # Ловим ID категории, который пришел из URL-адреса
        category_id = self.kwargs.get('pk')

        return get_products_by_category(category_id)