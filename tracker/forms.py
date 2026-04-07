from django import forms


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