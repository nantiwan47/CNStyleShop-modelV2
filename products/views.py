import os
from django.db.models import Min, Max
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.db import transaction
from .models import Product, ProductOption, ProductImage
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/account/admin-login')
def dashboard(request):
    return render(request, 'products/dashboard.html')

@login_required(login_url='/account/admin-login')
def product_list(request):
    # รับค่าคำค้นหาจาก URL
    query = request.GET.get('search', '').strip()  # กรณีที่ไม่มีคำค้นหาจะเป็นค่าว่าง และตัดช่องว่างหัวท้ายออก

    # ดึงข้อมูลสินค้าทั้งหมดพร้อมราคาต่ำสุดและสูงสุด และกรองตามคำค้นหา
    products = Product.objects.annotate(
        min_price=Min('options__price'),
        max_price=Max('options__price'),
    ).filter(name__icontains=query)

    products = products.order_by('-id')

    # แบ่งเพจ - 10 รายการต่อหน้า
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  # สร้าง object ของหน้าที่กำลังดู

    # นับจำนวนสินค้าทั้งหมด
    total_products = products.count()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'total_products': total_products,
        'query': query
    })

@login_required(login_url='/account/admin-login')
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

        # บันทึกตัวเลือกสินค้า
        for color, size, price in zip(colors, sizes, prices):
            if color and size and price:
                ProductOption.objects.create(
                    product=product,
                    color=color,
                    size=size,
                    price=price
                )

        # ดึงข้อมูลรูปภาพเพิ่มเติม
        image_files = request.FILES.getlist('images')

        # บันทึกรูปภาพเพิ่มเติม
        for image in image_files:
            ProductImage.objects.create(
                product=product,
                image=image
                )

        return redirect('product_list')

    return render(request, 'products/product_create.html')

@login_required(login_url='/account/admin-login')
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

                # เพิ่มรูปภาพใหม่
                new_images = request.FILES.getlist('new_images')
                if new_images:
                    for image in new_images:
                        ProductImage.objects.create(
                            product=product,
                            image=image
                        )

        except Exception as e:
            # หากเกิดข้อผิดพลาด ให้แสดงข้อความแจ้งเตือน
            return render(request, 'products/product_edit.html', {
                'product': product,
                'options': product.options.all(),
                'images': product.images.all(),
                'error': str(e),
            })

        return redirect('product_list')

    # ดึงข้อมูลตัวเลือกสินค้าและรูปภาพเพิ่มเติมสำหรับการแสดงฟอร์ม
    options = product.options.all()
    images = list(product.images.all())  # แปลง QuerySet เป็น List

    while len(images) < 4:
        images.append(None)

    context = {
        'product': product,
        'options': options,
        'images': images,
    }
    return render(request, 'products/product_edit.html', context)

def delete_image(request, image_id):
    if request.method == 'DELETE':
        # ตรวจสอบว่าเป็นคำขอจาก HTMX หรือไม่
        if request.headers.get('HX-Request'):
            # การลบภาพ
            image = get_object_or_404(ProductImage, id=image_id)

            image_file_path = image.image.path
            image.delete()  # ลบจากฐานข้อมูล

            # ลบไฟล์จากระบบไฟล์
            try:
                os.remove(image_file_path)
            except:
                pass  # ถ้าไม่สามารถลบไฟล์ได้ก็ไม่ต้องทำอะไร

            # เมื่อคำขอมาจาก HTMX ส่ง HTML ใหม่ที่แทนที่ content ของ #images_preview
            return HttpResponse('<span class="text-gray-400">รูปภาพ</span>')  # แสดงข้อความ placeholder

        else:
            # ถ้าไม่ใช่คำขอจาก HTMX ให้ส่งคำตอบอื่นๆ ตามปกติ
            return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required(login_url='/account/admin-login')
def product_delete(request, product_id):
    # ดึงข้อมูลสินค้าที่ต้องการลบ
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':

        # ลบรูปภาพหลักของสินค้า (cover_image)
        if product.cover_image:  # ตรวจสอบว่ามีรูปภาพหลักหรือไม่
            cover_image_path = product.cover_image.path  # พาธของไฟล์ภาพ
            if os.path.exists(cover_image_path):  # ตรวจสอบว่าไฟล์มีอยู่จริง
                os.remove(cover_image_path)  # ลบไฟล์ภาพหลัก

        # ลบตัวเลือกสินค้าที่เกี่ยวข้อง
        ProductOption.objects.filter(product=product).delete()

        # ลบรูปภาพที่เกี่ยวข้องจาก ProductImage
        product_images = ProductImage.objects.filter(product=product)
        for image in product_images:
            image_path = image.image.path  # พาธของไฟล์ภาพ
            if os.path.exists(image_path):  # ตรวจสอบว่าไฟล์มีอยู่จริง
                os.remove(image_path)  # ลบไฟล์ภาพ

        # ลบสินค้า
        product.delete()

        return JsonResponse({'status': 'success'}, status=200)

    return JsonResponse({'status': 'fail'}, status=400)

