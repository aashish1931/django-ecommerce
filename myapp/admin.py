from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Register)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Contact)