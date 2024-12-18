from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib import messages
from .forms import UserRegisterForm
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
        if self.request.user.role == 'user':
            return reverse_lazy('home')

        # เพิ่มข้อความแจ้งเตือน
        messages.error(self.request, "กรุณาล็อกอินด้วยบัญชีผู้ใช้")
        return reverse_lazy('login')

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

class AdminLoginView(LoginView):
    template_name = 'accounts/admin_login.html'

    def get_success_url(self):
        # ตรวจสอบ role ของผู้ใช้
        if self.request.user.role == 'admin':
            return reverse_lazy('dashboard')

        # เพิ่มข้อความแจ้งเตือน
        messages.error(self.request, "กรุณาล็อกอินด้วยบัญชีแอดมิน")
        return reverse_lazy('admin_login')

class AdminLogoutView(LogoutView):
    next_page = reverse_lazy('admin_login')


