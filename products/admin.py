from django.contrib import admin
from products.models import Product, ProductOption

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1  # จำนวนแถวเริ่มต้นที่ให้แสดง เมื่อไม่มีตัวเลือกสินค้าใดๆ
    fields = ['size', 'color', 'price']  # ฟิลด์ที่แสดง

# กำหนดการแสดงผลสำหรับ Product
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductOptionInline]
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category')
    list_filter = ('category',)

# กำหนดการแสดงผลสำหรับ ProductOption (ถ้ามี)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'price')
    search_fields = ('product__name', 'size', 'color')

# ลงทะเบียนโมเดลใน Django admin
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)