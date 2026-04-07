from django.shortcuts import render
from .forms import ProductFilterForm


def home(request):
    form = ProductFilterForm(request.GET or None)

    context = {
        "form": form,
    }
    return render(request, "home.html", context)
