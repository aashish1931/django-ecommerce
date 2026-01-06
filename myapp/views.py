from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def register(request):
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        password=request.POST['password']

        Register.objects.create(name=name,email=email,password=password)
        return redirect('login')
    return render(request,'register.html')

def login(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        user=Register.objects.get(email=email,password=password)
        if user:
            request.session['user_id']=user.id
            return redirect('home')
    return render(request,'login.html')

def home(request):
    products=Product.objects.all()
    return render(request,'home.html',{'products':products})

def products(request):
    products=Product.objects.all()
    return render(request,'products.html',{'products':products})

def add_to_cart(request,product_id):
    user=Register.objects.get(id=request.session['user_id'])
    product=Product.objects.get(id=product_id)

    cart,created=Cart.objects.get_or_create(user=user,product=product)
    if not created:
        cart.quantity+=1
        cart.save()
    return redirect('cart')

def increase_qty(request,cart_id):
    cart=Cart.objects.get(id=cart_id)
    cart.quantity+=1
    cart.save()
    return redirect('cart')

def decrease_qty(request,cart_id):
    cart=Cart.objects.get(id=cart_id)
    if cart.quantity>1:
        cart.quantity-=1
        cart.save()
    else:
        cart.delete()
    return redirect('cart')

def remove_item(request,cart_id):
    cart=Cart.objects.get(id=cart_id)
    cart.delete()
    return redirect('cart')

def cart(request):
    user=Register.objects.get(id=request.session['user_id'])
    cart_items=Cart.objects.filter(user=user)
    total_amount= sum(item.total_price for item in cart_items)
    return render(request,'cart.html',{'cart_items':cart_items,'total':total_amount})

import razorpay
from django.conf import settings
def checkout(request):
    user=Register.objects.get(id=request.session['user_id'])
    cart_items=Cart.objects.filter(user=user)
    total_amount=sum(item.total_price for item in cart_items)

    if request.method=='POST':

        payment_method=request.POST['payment_method']

        if payment_method=='COD':
            order=Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_method="COD",
            status="Order Placed"
         )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete()
            return redirect('order_success')
        
        else:
            order=Order.objects.create(
            user=user,
            total_amount=total_amount,
            payment_method="ONLINE",
            status="Order Placed"
         )
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart_items.delete()
            return redirect('order_success')
        
        if payment_method=='ONLINE':
            client=razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            razorpay_order=client.order.create({'amount':total_amount*100,'currency':'INR','payment_capture':'1'})

            return render(request,'checkout.html',{
                total_amount:total_amount,
                'razorpay_key_id':settings.RAZORPAY_KEY_ID,
                'razorpay_order_id':razorpay_order['id']
            })
            return redirect('order_success')

    return render(request,'checkout.html',{
        'cart_items':cart_items,
        'total_amount':total_amount
    })


def order_success(request):
    return render(request,'order_success.html')

# View (views.py)

def contact_us(request):
    if request.method == 'POST':
        Contact.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            subject=request.POST['subject'],
            message=request.POST['message']
        )
        return render(request, 'contact_success.html')

    return render(request, 'contact.html')

    
def logout(request):
    request.session.flush()#clear session data
    return redirect('login')

def about(request):
    return render(request, 'about.html')