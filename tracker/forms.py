from django import forms
from .models import (
    Product
)

class ProductFilterForm(forms.Form):
    store = forms.ChoiceField(
        choices=[
            ("", "Select a store"),
            ("coles", "Coles"),
            ("woolworths", "Woolworths"),
            ("chemist_warehouse", "Chemist Warehouse"),
        ],
        required=False,
        widget=forms.Select(attrs={
            "class": "form-select select2",
            "data-placeholder": "Select a store",
        })
    )

    category = forms.ChoiceField(
        choices=[
            ("", "Select a category"),
            ("supplements", "Supplements"),
            ("skincare", "Skincare"),
            ("groceries", "Groceries"),
        ],
        required=False,
        widget=forms.Select(attrs={
            "class": "form-select select2",
            "data-placeholder": "Select a category",
        })
    )

    product_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search product name",
        })
    )

from django import forms
from .models import Category, Product


class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="Select a category",
        widget=forms.Select(attrs={
            "class": "form-select select2",
            "data-placeholder": "Select a category",
        })
    )

    class Meta:
        model = Product
        fields = ["brand", "name", "weight_grams", "category", "barcode", "is_active"]
        widgets = {
            "brand": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Blackmores",
            }),
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Vitamin C 1000mg",
            }),
            "weight_grams": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. 500",
                "step": "0.01",
                "min": "0",
            }),
            "barcode": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Optional barcode",
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "form-check-input",
            }),
        }

    def clean_brand(self):
        return self.cleaned_data.get("brand", "").strip().title()

    def clean_name(self):
        return self.cleaned_data.get("name", "").strip()

    def clean_weight_grams(self):
        weight = self.cleaned_data.get("weight_grams")

        if weight is not None and weight <= 0:
            raise forms.ValidationError("Weight must be greater than 0.")

        return weight

    def clean_barcode(self):
        return self.cleaned_data.get("barcode", "").strip()
