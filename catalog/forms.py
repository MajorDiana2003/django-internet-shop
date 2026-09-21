from django import forms
from typing import Any, List, Dict
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields: List[str] = ['name', 'description', 'image', 'category', 'price']

        widgets: Dict[str, Any] = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

