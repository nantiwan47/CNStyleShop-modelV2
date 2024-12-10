from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# แบบฟอร์มสำหรับการลงทะเบียนผู้ใช้ใหม่
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
            'id': 'password1'
        }),
        help_text="รหัสผ่านควรมีความยาวอย่างน้อย 8 ตัวอักษร และห้ามเป็นตัวเลขล้วน"
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full border-gray-300 rounded-md shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm',
            'id': 'password2'
        })
    )

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password1', 'password2']

    # ฟังก์ชันสำหรับตรวจสอบอีเมล โดย .exists() ใช้ตรวจสอบว่า queryset มีข้อมูลหรือไม่ โดยไม่ดึงข้อมูลจากฐานข้อมูล
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

