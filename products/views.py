import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm
from .models import Product, ProductColor, ProductOption
from django.db.models import Min, Max
from django.core.paginator import Paginator
from django.db import transaction


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

    # แบ่ง 10 รายการต่อหน้า
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')  # รับหมายเลขหน้าจาก query string
    page_obj = paginator.get_page(page_number)  # สร้าง object ของหน้าที่กำลังดู

    # นับจำนวนสินค้าทั้งหมด
    total_products = Product.objects.count()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'total_products': total_products,
        'query': query})

def create_product_color_and_options(product, color, size, price, image):
    # สร้าง ProductColor
    product_color = ProductColor.objects.create(
        product=product,
        color=color,
        image=image
    )
    # สร้าง ProductOption
    ProductOption.objects.create(
        product=product,
        color=product_color,
        size=size,
        price=price
    )

# def product_create(request):
#     if request.method == 'POST':
#         # ดึงข้อมูลจากฟอร์ม
#         name = request.POST.get('name')
#         description = request.POST.get('description')
#         category = request.POST.get('category')
#         cover_image = request.FILES.get('cover_image')
#
#         # ดึงข้อมูลจาก hidden input
#         products_data = json.loads(request.POST.get('products', '[]'))
#
#         # ใช้ Transaction สำหรับการบันทึกข้อมูล
#         with transaction.atomic():
#             # สร้าง Product
#             product = Product.objects.create(
#                 name=name,
#                 description=description,
#                 category=category,
#                 cover_image=cover_image
#             )
#
#             # สร้าง ProductColor และ ProductOption
#             for item in products_data:
#                 create_product_color_and_options(product, item)
#
#         return JsonResponse({'message': 'Product created successfully!'})
#
#     return render(request, 'products/product_create.html')

def product_create(request):
    if request.method == 'POST':
        # ดึงข้อมูลสินค้า
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        cover_image = request.FILES.get('cover_image')

        # สร้าง Product
        product = Product.objects.create(
            name=name,
            description=description,
            category=category,
            cover_image=cover_image
        )


        # รับข้อมูลจาก FormData
        products_data = json.loads(request.POST.get('products', '[]'))  # ข้อมูล JSON
        color_images = request.FILES.getlist('color_images[]')  # รับไฟล์ภาพ

                # บันทึกข้อมูล
        for i, item in enumerate(products_data):
                    color = item['color']
                    size = item['size']
                    price = item['price']
                    image = color_images[i]

                    # เรียกฟังก์ชสร้าง ProductColor และ ProductOption
                    create_product_color_and_options(product, color, size, price, image)
                    return JsonResponse({'message': 'Product created successfully!'})
        else:
            print('บันทึกไม่ได้')

    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # ใช้ form สำหรับข้อมูลสินค้า
        if form.is_valid():
            # ใช้ Transaction สำหรับการบันทึกข้อมูล
                # สร้าง Product
                product = form.save()

                # รับข้อมูลจาก FormData
                products_data = json.loads(request.POST.get('products', '[]'))  # ข้อมูล JSON
                color_images = request.FILES.getlist('color_images[]')  # รับไฟล์ภาพ

                # บันทึกข้อมูล
                for i, item in enumerate(products_data):
                    color = item['color']
                    size = item['size']
                    price = item['price']
                    image = color_images[i]

                    # เรียกฟังก์ชสร้าง ProductColor และ ProductOption
                    create_product_color_and_options(product, color, size, price, image)
                    return JsonResponse({'message': 'Product created successfully!'})
        else:
            print('บันทึกไม่ได้')

    else:
        form = ProductForm()

    return render(request, 'products/product_create.html', {'form': form})

def dashboard(request):
    return render(request, 'products/dashboard.html')


def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)  # ส่งข้อมูลจากฟอร์ม
        if form.is_valid():
            form.save()  # บันทึกข้อมูลลงในฐานข้อมูล
            return redirect('product_list')  # เปลี่ยนเส้นทางไปหน้ารายการสินค้า
    else:
        form = ProductForm()  # ถ้าไม่ใช่ POST ให้แสดงฟอร์มเปล่า

    return render(request, 'add_product.html', {'form': form})