from django.contrib import admin
from .models import Profile, Cart, Reviews, Order, OrderDetails

admin.site.register(Profile)
admin.site.register(Cart)
admin.site.register(Reviews)
admin.site.register(Order)
admin.site.register(OrderDetails)