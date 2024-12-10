from django.urls import path
from accounts.views import *

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),  # ชื่อ URL สำหรับหน้า login
    path('home/', home, name='home'),
    path('dashboard/', dashboard, name='dashboard'),

]