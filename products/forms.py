from django import forms
from django.forms import inlineformset_factory
from .models import Product, ProductColor, ProductOption

# ฟอร์มสำหรับ Product
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'cover_image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none',
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none',
                'rows': 4
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none'
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'w-full border-gray-300 rounded-lg shadow-sm focus:ring focus:ring-blue-200 focus:outline-none'
            }),
        }

# # ฟอร์มสำหรับ ProductColor
# class ProductColorForm(forms.ModelForm):
#     class Meta:
#         model = ProductColor
#         fields = ['color', 'image']
#         widgets = {
#             'color': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'สี'}),
#             'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }
#         labels = {
#             'color': 'สี',
#             'image': 'รูปภาพตัวอย่างสี',
#         }
#
# # ฟอร์มสำหรับ ProductOption
# class ProductOptionForm(forms.ModelForm):
#     class Meta:
#         model = ProductOption
#         fields = ['color', 'size', 'price']
#         widgets = {
#             'color': forms.Select(attrs={'class': 'form-select'}),
#             'size': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'ขนาด'}),
#             'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'ราคา'}),
#         }
#         labels = {
#             'color': 'สี',
#             'size': 'ขนาด',
#             'price': 'ราคา',
#         }
#

