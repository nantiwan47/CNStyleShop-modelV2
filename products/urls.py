from django.urls import path
from .views import  *

urlpatterns = [
 path('dashboard/', dashboard, name='dashboard'),
 path('product-list', product_list, name="product_list"),
 path('product-create/', product_create, name="product_create"),
]