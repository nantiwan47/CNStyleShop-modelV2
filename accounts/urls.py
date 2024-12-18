from django.urls import path
from accounts.views import *


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('admin-logout/', AdminLogoutView.as_view(), name='admin-logout'),
]