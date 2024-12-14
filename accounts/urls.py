from django.urls import path
from accounts.views import *


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('admin-login/', AdminLoginView.as_view(), name='admin_login'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('admin-logout/', AdminLogoutView.as_view(), name='admin-logout'),

]