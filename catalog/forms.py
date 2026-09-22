from typing import Any, Dict, List

from django import forms
from django.core.exceptions import ValidationError

from catalog.models import Product

# Критерий №4: Список запрещенных слов
FORBIDDEN_WORDS: List[str] = [
    "казино",
    "биржа",
    "обман",
    "криптовалюта",
    "дешево",
    "полиция",
    "крипта",
    "бесплатно",
    "радар",
]


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields: List[str] = ["name", "description", "image", "category", "price"]
        widgets: Dict[str, Any] = {
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Задание 3: Автоматическая стилизация всех полей под Bootstrap."""
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})

    def _validate_forbidden_words(self, value: str | None) -> str | None:
        """Вспомогательный метод регистронезависимой проверки слов."""
        if value:
            value_lower = value.lower()
            for word in FORBIDDEN_WORDS:
                if word in value_lower:
                    raise ValidationError(
                        f"В тексте обнаружено запрещенное слово: '{word}'."
                    )
        return value

    def clean_name(self) -> str | None:
        """Валидация названия продукта на запрещенные слова (Задание 1)."""
        name = self.cleaned_data.get("name")
        return self._validate_forbidden_words(name)

    def clean_description(self) -> str | None:
        """Валидация описания продукта на запрещенные слова (Задание 1)."""
        description = self.cleaned_data.get("description")
        return self._validate_forbidden_words(description)

    def clean_price(self) -> int | None:
        """Задание 2: Кастомная валидация цены (запрет отрицательных чисел)."""
        price = self.cleaned_data.get("price")
        if price is not None and price < 0:
            raise ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def clean_image(self) -> Any:
        """Дополнительное задание: Валидация формата и размера картинки."""
        image = self.cleaned_data.get("image")
        if image:
            # Ограничение 5 МБ (5 * 1024 * 1024 байт)
            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError("Размер файла не должен превышать 5 МБ.")

            # Проверяем формат файла
            valid_types = ["image/jpeg", "image/png"]
            if hasattr(image, "content_type") and image.content_type not in valid_types:
                raise ValidationError(
                    "Допускаются только изображения в формате JPEG или PNG."
                )
        return image
