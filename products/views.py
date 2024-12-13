# from django.http import JsonResponse
# from .models import Product, ProductColor, ProductOption

from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm

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
#     return render(request, 'products/create_product.html')




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
    return render(request, 'products/create_product.html', {'form': form})

def dashboard(request):
    return render(request, 'products/dashboard.html')

