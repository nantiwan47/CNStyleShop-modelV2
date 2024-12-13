from django.urls import path
from django_browser_reload.urls import app_name
from .views import  *

urlpatterns = [
 path('add/', product_create, name="add"),
 path('dashboard/', dashboard, name='dashboard'),

]