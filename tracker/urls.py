from django.urls import path
from .views import home
from .views import home, product_list, new_product

urlpatterns = [
    path('', home, name='home'),
    path("products/", product_list, name="product_list"),
    path("products/new/", new_product, name="new_product"),
]