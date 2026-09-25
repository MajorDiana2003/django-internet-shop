from django.urls import path
from django.contrib.auth.views import LogoutView
from users.apps import UsersConfig
from users.views import RegisterView, UserLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
]
