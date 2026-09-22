from django.core.management import call_command
from django.core.management.base import BaseCommand

from catalog.models import Category, Product


class Command(BaseCommand):
    help = "Очищает базу данных и загружает данные из фикстуры"

    def handle(self, *args, **options):
        # 1. Предварительное удаление данных перед загрузкой (Пункт 5 критериев)
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.WARNING("База данных успешно очищена."))

        # 2. Использование существующей фикстуры в команде
        try:
            # Запускаем системную команду loaddata для нашего json-файла
            call_command("loaddata", "catalog_data.json")
            self.stdout.write(self.style.SUCCESS("🎉 Фикстуры загружены в БД корректно, связи выстроены!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Ошибка при загрузке фикстур: {e}"))
