from django.urls import path

from blog import views
from blog.apps import BlogConfig

app_name = BlogConfig.name

urlpatterns = [
    # Список статей
    path("", views.BlogListView.as_view(), name="list"),
    # Создание статьи
    path("create/", views.BlogCreateView.as_view(), name="create"),
    # Просмотр статьи по её slug
    path("<slug:slug>/", views.BlogDetailView.as_view(), name="detail"),
    # Редактирование статьи по её slug
    path("<slug:slug>/update/", views.BlogUpdateView.as_view(), name="update"),
    # Удаление статьи по её slug
    path("<slug:slug>/delete/", views.BlogDeleteView.as_view(), name="delete"),
]
