from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)
from .models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
