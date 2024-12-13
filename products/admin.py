from django.contrib import admin
from products.models import Product, ProductOption, ProductColor

class ProductColorInline(admin.TabularInline):
    model = ProductColor
    extra = 1
    fields = ('color', 'image')

class ProductOptionInline(admin.TabularInline):
    model = ProductOption
    extra = 1
    fields = ['size', 'color', 'price']
    autocomplete_fields = ['color']  # ใช้ autocomplete เพื่อเลือกสีไดนามิก

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductColorInline, ProductOptionInline]
    list_display = ('name', 'category', 'created_at', 'updated_at')
    search_fields = ('name', 'category')
    list_filter = ('category', 'created_at')

# ProductColor Admin
class ProductColorAdmin(admin.ModelAdmin):
    list_display = ('product', 'color')
    list_filter = ('product',)
    search_fields = ('product__name', 'color')  # รองรับการค้นหาใน autocomplete

# ProductOption Admin
class ProductOptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'size', 'color', 'price')
    list_filter = ('product', 'color')
    search_fields = ('product__name', 'size', 'color')

# Register Models
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductOption, ProductOptionAdmin)
