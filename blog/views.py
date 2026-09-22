from typing import Any

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .models import BlogPost


class BlogListView(ListView):
    """Список всех опубликованных блоговых записей"""

    model = BlogPost
    template_name = "blog/blog_list.html"
    context_object_name = "posts"

    def get_queryset(self) -> Any:
        """По ТЗ выводим только те статьи, которые имеют признак публикации True"""
        return super().get_queryset().filter(is_published=True).order_by("-created_at")


class BlogDetailView(DetailView):
    """Детальный просмотр статьи с автоматическим счетчиком просмотров"""

    model = BlogPost
    template_name = "blog/blog_detail.html"
    context_object_name = "post"

    def get_object(self, queryset: Any = None) -> Any:
        """Переопределяем метод для фиксации просмотров при каждом открытии"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogCreateView(CreateView):
    """Создание новой статьи в блоге"""

    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_form.html"
    success_url = reverse_lazy("blog:list")  # После создания возвращаем к списку


class BlogUpdateView(UpdateView):
    """Редактирование существующей статьи"""

    model = BlogPost
    fields = ("title", "content", "preview", "is_published")
    template_name = "blog/blog_form.html"

    def get_success_url(self) -> str:
        """По ТЗ после успешного редактирования перенаправляем на DetailView этой статьи"""
        return reverse("blog:detail", kwargs={"slug": self.object.slug})


class BlogDeleteView(DeleteView):
    """Удаление статьи из блога"""

    model = BlogPost
    template_name = "blog/blog_confirm_delete.html"
    success_url = reverse_lazy("blog:list")
