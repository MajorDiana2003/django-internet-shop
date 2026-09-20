from django.shortcuts import render
from catalog.models import Product, ContactInfo


def home(request):
    """Контроллер для главной страницы — выводит все товары из базы данных"""
    # Получаем все продукты из базы данных PostgreSQL
    products = Product.objects.all()

    # Дополнительное задание №1: Выводим последние 5 товаров в консоль
    print("\n--- ПОСЛЕДНИЕ ТОВАРЫ В КОНСОЛИ ---")
    for prod in products[:5]:
        print(prod)
    print("-----------------------------------\n")

    # Передаем продукты внутрь HTML-шаблона через контекст
    return render(request, 'index.html', {'products': products})


def contacts(request):
    """Контроллер для страницы контактов — обрабатывает форму и выводит контакты из БД"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        print("\n==========================================")
        print("   ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (DJANGO)     ")
        print("==========================================")
        print(f"Имя: {name}\nТелефон: {phone}\nСообщение: {message}")
        print("==========================================\n")

    # Дополнительное задание №2: Берем контактную информацию из базы данных
    contact_data = ContactInfo.objects.first()
    if not contact_data:
        # Если в базе ещё нет контактов, создадим автоматическую заглушку, чтобы сайт не падал
        contact_data = ContactInfo.objects.create(
            phone='+7 (999) 000-00-00',
            email='info@my-django-shop.ru',
            address='г. Шахты, ул. Программистов, д. 1'
        )

    return render(request, 'contacts.html', {'contact': contact_data})




