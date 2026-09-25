from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    username = None

    # Делаем электронную почту
    email = models.EmailField(unique=True, verbose_name="Электронная почта")


    avatar = models.ImageField(upload_to="users/avatars/", blank=True, null=True, verbose_name="Аватар")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Номер телефона")
    country = models.CharField(max_length=50, blank=True, null=True, verbose_name="Страна")
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',
        blank=True,
        verbose_name='Группы'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',
        blank=True,
        verbose_name='Права доступа'
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

