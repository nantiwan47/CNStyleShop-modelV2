from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class UserProfile(AbstractUser):
    # ลบฟิลด์ first_name และ last_name
    first_name = None
    last_name = None

    # เพิ่มฟิลด์ใหม่
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other'),], blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    phone_number = models.CharField(max_length=10, blank=True)
    address = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile', blank=True, default='profile/default_profile.jpg')
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('admin', 'Admin')], default='user')
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:  # ตรวจสอบว่าผู้ใช้เป็น superuser หรือไม่
            self.role = 'admin'
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} - ({self.role})"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"