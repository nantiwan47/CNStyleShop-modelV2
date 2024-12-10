from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import *
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from .models import *

class UserRegisterView(CreateView):
    model = UserProfile
    form_class = UserRegisterForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserLoginView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        # ตรวจสอบ role ของผู้ใช้
        if self.request.user.role == 'admin':
            return reverse_lazy('dashboard')  # เส้นทางสำหรับ admin
        return reverse_lazy('home')  # ไปที่หน้า home สำหรับ user

def dashboard(request):
    return render(request, 'dashboard.html')

def home(request):
    return render(request, 'home.html')



