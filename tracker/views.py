from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import ProductForm
from .models import Product


def home(request):
    return render(request, "home.html")


def product_list(request):
    products = (
        Product.objects
        .select_related("category")
        .all()
        .order_by("brand", "name", "weight_grams")
    )

    context = {
        "products": products,
    }
    return render(request, "tracker/product_info.html", context)


def new_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f"Product '{product}' created successfully.")
            return redirect("product_list")
    else:
        form = ProductForm()

    context = {
        "form": form,
        "page_title": "New Product",
    }
    return render(request, "tracker/product_form.html", context)
