from django.urls import path
from .views import  *

urlpatterns = [
 path('create-product/', create_product, name="create-product"),
 path('dashboard/', dashboard, name='dashboard'),

]