from django.db import models

# Create your models here.
class Register(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    password=models.CharField(max_length=250)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField()
    price=models.IntegerField()
    image=models.ImageField(upload_to='products/', null=True,blank=True)

class Cart(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    @property
    def total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    user=models.ForeignKey(Register,on_delete=models.CASCADE)
    total_amount=models.IntegerField()
    payment_method=models.CharField(default="COD")
    status=models.CharField(default="Pending")
    created_at=models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.IntegerField()


class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=200)
    message=models.TextField()
"""
Razorpay Integration in Django
Last Updated : 20 Nov, 2025
Razorpay is a popular payment gateway in India that allows businesses to accept online payments via credit/debit cards, UPI, wallets, and net banking. Integrating Razorpay with Django enables secure and seamless payment processing for your web applications.

Project Setup with Razorpay in Django
Consider a project named 'dj_razorpay' having an app named 'payment', and create a Payment model to track transactions and apply migrations.

In payment/models.py:


from django.db import models

class Payment(models.Model):
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=50, default='Created')  # Created, Success, Failed
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.razorpay_order_id} - {self.status}"
Step 1: Get Razorpay Keys
Create an account on the Razorpay website by signing up with your email address and password. During registration, provide the required basic details such as your phone number. After the account is set up, complete the KYC verification by submitting your identity documents and business details.

Once verified, navigate to the Razorpay Dashboard to obtain the API Key ID and Key Secret, which are required for integration. For live transactions, you will also need to add your bank account details to enable settlements.

Note: After successful verification, you will see a similar user interface as below.



Inside the Razorpay settings screen, select 'Create a new key' to generate your API credentials. This will provide a Key ID and a Key Secret.

At this stage, payments operate in test mode, meaning no real transactions occur and only limited payment methods are available. To enable live transactions and unlock all payment options, complete the KYC verification process and add bank account details. The integration process remains identical for both test and live modes.



Add the 'Key Id' and 'Key Secret' to settings.py file.

RAZOR_KEY_ID = 'YOUR_KEY_ID'
RAZOR_KEY_SECRET = 'YOUR_KEY_SECRET'

Install razorpay's python package:

pip install razorpay

Razorpay Payment Flow
A Razorpay Order is created from the Django backend.
The Order ID and other required details are passed to the frontend.
The user clicks the payment button and completes the transaction using a preferred payment method.
Razorpay handles both payment success and failure scenarios.
In case of failure, Razorpay allows the user to retry the payment.
On successful payment, Razorpay sends a POST request to a callback URL on the Django server.
The server then verifies the payment signature to ensure authenticity and prevent tampering.
Once verified, the payment is captured, and a success page is rendered for the user.
"""
