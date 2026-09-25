from django import forms
from django.contrib.auth.forms import UserCreationForm
from users.models import User


class UserRegisterForm(UserCreationForm):
    # Добавляем поле подтверждения пароля
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        label="Подтвердите пароль",
        help_text="Введите пароль ещё раз для проверки"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        # Добавляем email и все 3 кастомных поля в форму регистрации
        fields = ('email', 'phone', 'avatar', 'country')

    def clean(self):
        """Метод для обработки потенциальных ошибок и проверки паролей"""
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        # Если пароли заполнены, но не совпадают — выдаем ошибку формы
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают.")

        return cleaned_data


class UserLoginForm(forms.Form):
    """Форма для входа по email"""
    email = forms.EmailField(label="Электронная почта")
    password = forms.CharField(widget=forms.PasswordInput(), label="Пароль")

