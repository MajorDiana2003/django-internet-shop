from django.shortcuts import render


def home(request):
    """Контроллер для главной страницы — рендерит шаблон index.html"""
    return render(request, 'index.html')


def contacts(request):
    """Контроллер для страницы контактов — рендерит шаблон и обрабатывает форму"""
    if request.method == 'POST':
        # Забираем данные, которые пользователь ввёл в поля формы
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Печатаем полученные данные в терминал PyCharm
        print("\n==========================================")
        print("   ПОЛУЧЕНЫ ДАННЫЕ ИЗ ФОРМЫ (DJANGO)     ")
        print("==========================================")
        print(f"Имя: {name}")
        print(f"Телефон: {phone}")
        print(f"Сообщение: {message}")
        print("==========================================\n")

    return render(request, 'contacts.html')



