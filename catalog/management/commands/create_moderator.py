from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создает группу Модератор продуктов с необходимыми правами'

    def handle(self, *args, **options):
        # Создаем или находим группу
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        # Получаем контент-тип нашей модели продукта
        content_type = ContentType.objects.get_for_model(Product)

        # Ищем два нужных разрешения по их кодам
        perm_unpublish = Permission.objects.get(codename='can_unpublish_product', content_type=content_type)
        perm_delete = Permission.objects.get(codename='delete_product', content_type=content_type)

        # Добавляем права в группу
        group.permissions.add(perm_unpublish, perm_delete)

        self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана и настроена!'))
