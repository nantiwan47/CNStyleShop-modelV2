from django.contrib import admin
from .models import Product, ProductOption, ProductImage
from django.utils.html import mark_safe


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # จำนวนแถวที่เพิ่มขึ้นใหม่ได้ในฟอร์ม
    fields = ['image', 'preview_image']
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No image"


class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1  # จำนวนแถวที่เพิ่มขึ้นใหม่ได้ในฟอร์ม
    fields = ['color', 'size', 'price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'cover_image_preview', 'created_at', 'updated_at']
    search_fields = ['name', 'category']
    list_filter = ['category']
    # inlines = [ProductOptionInline, ProductImageInline]  # รวมตัวเลือกสินค้าและรูปภาพสินค้าในหน้าเดียวกัน

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return mark_safe(f'<img src="{obj.cover_image.url}" width="100" />')
        return "No image"

    cover_image_preview.short_description = 'Cover Image Preview'


@admin.register(ProductOption)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ['product', 'color', 'size', 'price']
    search_fields = ['product__name', 'color', 'size']


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'image_preview']
    search_fields = ['product__name']

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100" />')
        return "No image"

    image_preview.short_description = 'Image Preview'
