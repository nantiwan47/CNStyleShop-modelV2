from django.contrib import admin
from products.models import Product, ProductOption, ProductColor

# ProductColor Inline (ยังคงแสดงในหน้า Product)
class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('color', 'image')

# Product Admin (แสดงเฉพาะ ProductColorInline)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorInline]
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'created_at')

# ProductOption Admin (แยกหน้าจัดการของตัวเอง)
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'price')
    list_filter = ('product', 'color', 'size')
    search_fields = ('product__name', 'size', 'color')
    autocomplete_fields = ['product', 'color']  # ช่วยเลือกสินค้าและสีได้ง่าย

# ProductColor Admin (ถ้าต้องการแสดงในหน้าแยกด้วย)
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color')
    list_filter = ('product',)
    search_fields = ('product__name', 'color')

# Register Models
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
