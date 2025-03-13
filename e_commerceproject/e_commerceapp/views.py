
from e_commerceapp.models import Contact,Product
from django.contrib import messages
from math import ceil
import qrcode
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.conf import settings
from .models import Order
import json
import os


# Create your views here.
def index(request):
    allProds = []
    catprods = Product.objects.values('category', 'id')
    print(catprods)
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds}
    return render(request, "index.html", params)


def contact(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        desc=request.POST.get("desc")
        pnumber=request.POST.get("pnumber")
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"we will get back to you soon")
    return render(request,"contact.html",)    


def about(request):
    return render(request,"about.html") 




def checkout(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')
        items_json = request.POST.get('itemsJson')
        total_amount = request.POST.get('amt')

        # Save order
        order = Order(
            name=name,
            email=email,
            address1=address1,
            address2=address2,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            items_json=items_json,
            total_amount=total_amount
        )
        order.save()

        # Generate QR Code
        qr_data = f"Pay Rs. {total_amount} to UPI 6309195703@upi for Order ID: {order.id}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)

        # Save the QR Code image
        qr_dir = os.path.join(settings.MEDIA_ROOT, 'qr_codes')
        if not os.path.exists(qr_dir):
            os.makedirs(qr_dir)  # Ensure directory exists
        qr_path = os.path.join(qr_dir, f'order_{order.id}.png')
        img = qr.make_image(fill="black", back_color="white")
        img.save(qr_path)

        # Save QR Code path to model
        order.qr_code = f'qr_codes/order_{order.id}.png'
        order.save()
        return render(request, 'thankyou.html', {'order': order})

    return render(request, 'checkout.html')
