from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.core.mail import send_mail
from django.conf import settings
from users.forms import UserRegisterForm, UserLoginForm


class RegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        send_mail(
            subject="Успешная регистрация!",
            message=f"Добро пожаловать! Ваш логин: {user.email}",
            from_email='noreply@shop.ru',
            recipient_list=[user.email],
            fail_silently=True,
        )
        return super().form_valid(form)


class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'

