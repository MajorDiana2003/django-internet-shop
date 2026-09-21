from django.contrib import admin

from .models import BlogPost


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    # Поля, которые будут отображаться в таблице списка статей
    list_display = ("id", "title", "slug", "is_published", "views_count", "created_at")
    # Поля, по которым можно фильтровать записи
    list_filter = ("is_published", "created_at")
    # Поля, по которым работает поиск
    search_fields = ("title", "content")
    # Автоматическое заполнение поля slug при вводе заголовка в админке
    prepopulated_fields = {"slug": ("title",)}
