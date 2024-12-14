# from django.http import JsonResponse
# from .models import Product, ProductColor, ProductOption

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm
from .models import *
from django.db.models import Min, Max
from django.core.paginator import Paginator


# def create_product_view(request):
#     if request.method == 'POST':
#         # ข้อมูลสินค้า
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         category = request.POST.get('category')
#         cover_image = request.FILES.get('cover_image')
#
#         print(name, description, category, cover_image)
#
#         # บันทึก Product
#         product = Product.objects.create(
#             name=name,
#             description=description,
#             category=category,
#             image=cover_image
#         )
#
#         # ข้อมูลสีสินค้า
#         colors = request.POST.getlist('colors[]')
#         color_images = request.FILES.getlist('color_images[]')
#         print(colors, color_images)
#
#         for color, color_image in zip(colors, color_images):
#             product_color = ProductColor.objects.create(
#                 product=product,
#                 color=color,
#                 image=color_image
#             )
#
#         # ข้อมูลตัวเลือกสินค้า (ไซส์)
#         size_colors = request.POST.getlist('size_colors[]')
#         sizes = request.POST.getlist('sizes[]')
#         prices = request.POST.getlist('prices[]')
#
#         print(size_colors, sizes, prices)
#
#         for size_color, size, price in zip(size_colors, sizes, prices):
#             product_color = ProductColor.objects.filter(product=product, color=size_color).first()
#             ProductOption.objects.create(
#                 product=product,
#                 color=product_color,
#                 size=size,
#                 price=price
#             )
#
#         return JsonResponse({'message': 'Product created successfully!'})
#
#     return render(request, 'products/product_create.html')

def product_list(request):
    # รับค่าคำค้นหาจาก URL
    query = request.GET.get('search', '')  # กรณีที่ไม่มีคำค้นหาจะเป็นค่าว่าง

    # ดึงข้อมูลสินค้าทั้งหมดพร้อมราคาต่ำสุดและสูงสุด และกรองตามคำค้นหา
    products = Product.objects.annotate(
        min_price=Min('options__price'),
        max_price=Max('options__price'),
    ).filter(name__icontains=query)

    # แบ่งเพจ - 10 รายการต่อหน้า
    paginator = Paginator(products, 10)  # แบ่งสินค้าทีละ 10 รายการ
    page_number = request.GET.get('page')  # รับหมายเลขหน้าจาก query string
    page_obj = paginator.get_page(page_number)  # สร้าง object ของหน้าที่กำลังดู

    # นับจำนวนสินค้าทั้งหมด
    total_products = Product.objects.count()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'total_products': total_products,
        'query': query})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        # บันทึก Product
        if form.is_valid():
            product = form.save()
            return redirect('product_list')
        else:
            messages.error(request, "มีข้อผิดพลาดในการบันทึกสินค้า")
    else:
        form = ProductForm()
    return render(request, 'products/product_create.html', {'form': form})

def dashboard(request):
    return render(request, 'products/dashboard.html')

