from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Users, Product, Category, Order

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone_number']
    search_fields = ['name', 'email']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'quantity']
    list_filter = ['category']
    search_fields = ['name']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'users', 'order_amount', 'order_status', 'registration_date']
    list_filter = ['order_status', 'payment_method', 'shipping_method']
    search_fields = ['order_number', 'users__name']
    filter_horizontal = ['product']