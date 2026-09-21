from typing import Any

from django.db import models
from pytils.translit import slugify


class BlogPost(models.Model):
    title: models.CharField = models.CharField(max_length=200, verbose_name="Заголовок")
    slug: models.SlugField = models.SlugField(max_length=250, verbose_name="Slug", blank=True, null=True)
    content: models.TextField = models.TextField(verbose_name="Содержимое")
    preview: models.ImageField = models.ImageField(
        upload_to="blog/", verbose_name="Превью (изображение)", blank=True, null=True
    )
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    is_published: models.BooleanField = models.BooleanField(default=True, verbose_name="Признак публикации")
    views_count: models.IntegerField = models.IntegerField(default=0, verbose_name="Количество просмотров")

    class Meta:
        verbose_name = "Блоговая запись"
        verbose_name_plural = "Блоговые записи"

    def __str__(self) -> str:
        return str(self.title)

    def save(self, *args: Any, **kwargs: Any) -> None:
        """Автоматическая генерация slug при сохранении статьи"""
        if not self.slug and self.title:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
