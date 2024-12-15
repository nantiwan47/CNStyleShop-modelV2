from django.db.models import Min, Max
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from .models import Product, ProductOption, ProductImage
from django.http import JsonResponse

def dashboard(request):
    return render(request, 'products/dashboard.html')

def product_list(request):
    # รับค่าคำค้นหาจาก URL
    query = request.GET.get('search', '')  # กรณีที่ไม่มีคำค้นหาจะเป็นค่าว่าง

    # ดึงข้อมูลสินค้าทั้งหมดพร้อมราคาต่ำสุดและสูงสุด และกรองตามคำค้นหา
    products = Product.objects.annotate(
        min_price=Min('options__price'),
        max_price=Max('options__price'),
    ).filter(name__icontains=query)

    products = products.order_by('updated_at')

    # แบ่งเพจ - 10 รายการต่อหน้า
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # สร้าง object ของหน้าที่กำลังดู

    # นับจำนวนสินค้าทั้งหมด
    total_products = Product.objects.count()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'total_products': total_products,
        'query': query})

def product_create(request):
    if request.method == 'POST':
        # ดึงข้อมูลสินค้า
        name = request.POST.get('name')
        description = request.POST.get('description')
        category = request.POST.get('category')
        cover_image = request.FILES.get('cover_image')

        # บันทึกสินค้า
        product = Product.objects.create(
            name=name,
            description=description,
            category=category,
            cover_image=cover_image
        )

        # ดึงข้อมูลตัวเลือกสินค้า
        colors = request.POST.getlist('color')
        sizes = request.POST.getlist('size')
        prices = request.POST.getlist('price')

        for color, size, price in zip(colors, sizes, prices):
            if color and size and price:
                ProductOption.objects.create(
                    product=product,
                    color=color,
                    size=size,
                    price=price
                )

        # บันทึกรูปภาพเพิ่มเติม
        image_files = request.FILES.getlist('images')
        for image in image_files:
            ProductImage.objects.create(
                product=product,
                image=image
                )

        return redirect('product_list')

    return render(request, 'products/product_create.html')

def product_edit(request, product_id):
    # ดึงข้อมูลสินค้าที่ต้องการแก้ไข
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        # เริ่มกระบวนการจัดการข้อมูลแบบ Atomic
        try:
            with transaction.atomic():
                # ดึงข้อมูลจากฟอร์ม
                name = request.POST.get('name')
                description = request.POST.get('description')
                category = request.POST.get('category')
                cover_image = request.FILES.get('cover_image')

                # อัปเดตข้อมูลสินค้า
                product.name = name
                product.description = description
                product.category = category
                if cover_image:
                    product.cover_image = cover_image  # อัปเดตรูปภาพหากมีการอัปโหลดใหม่
                product.save()

                # ลบตัวเลือกสินค้าเก่าก่อนแล้วเพิ่มใหม่
                ProductOption.objects.filter(product=product).delete()

                colors = request.POST.getlist('color')
                sizes = request.POST.getlist('size')
                prices = request.POST.getlist('price')

                # ตรวจสอบความถูกต้องของข้อมูลตัวเลือก
                for color, size, price in zip(colors, sizes, prices):
                    if color and size and price:
                        ProductOption.objects.create(
                            product=product,
                            color=color,
                            size=size,
                            price=price
                        )

                # จัดการรูปภาพเพิ่มเติม
                delete_images = request.POST.getlist('delete_images')
                if delete_images:
                    ProductImage.objects.filter(id__in=delete_images, product=product).delete()

                # เพิ่มรูปภาพใหม่
                new_images = request.FILES.getlist('new_images')
                if new_images:
                    for image in new_images:
                        ProductImage.objects.create(product=product, image=image)

        except Exception as e:
            # หากเกิดข้อผิดพลาด ให้แสดงข้อความแจ้งเตือน
            return render(request, 'products/product_edit.html', {
                'product': product,
                'options': product.options.all(),
                'images': product.images.all(),
                'error': str(e),
            })

        return redirect('product_list')  # เปลี่ยน URL นี้ให้เหมาะสม

    # ดึงข้อมูลตัวเลือกสินค้าและรูปภาพเพิ่มเติมสำหรับการแสดงฟอร์ม
    options = product.options.all()
    images = product.images.all()

    context = {
        'product': product,
        'options': options,
        'images': images,
    }
    return render(request, 'products/product_edit.html', context)

def product_delete(request, product_id):
    # ดึงข้อมูลสินค้าที่ต้องการลบ
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        # ลบตัวเลือกสินค้าที่เกี่ยวข้อง
        ProductOption.objects.filter(product=product).delete()

        # ลบรูปภาพที่เกี่ยวข้อง
        ProductImage.objects.filter(product=product).delete()

        # ลบสินค้า
        product.delete()

        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'status': 'fail'}, status=400)



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
# def product_create(request):
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#
#         # บันทึก Product
#         if form.is_valid():
#             product = form.save()
#             return redirect('product_list')
#         else:
#             messages.error(request, "มีข้อผิดพลาดในการบันทึกสินค้า")
#     else:
#         form = ProductForm()
#     return render(request, 'products/product_create.html', {'form': form})

