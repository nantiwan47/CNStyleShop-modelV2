from django.urls import path
from accounts.views import *


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', AdminLogoutView.as_view(), name='admin_logout'),

]