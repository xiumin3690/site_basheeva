from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="Name")
    description = models.TextField(verbose_name="Description")
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('olga:category_detail', args=[str(self.id)])

class Users(models.Model):
    name = models.CharField(max_length=100, verbose_name="Name")
    address = models.TextField(verbose_name="Address")
    email = models.EmailField(unique=True, verbose_name="Email")
    phone_number = models.IntegerField(verbose_name="Phone number")
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('olga:user_detail', args=[str(self.id)])

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Name")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Category"
    )
    quantity = models.IntegerField(verbose_name="Quantity")
    description = models.TextField(blank=True, verbose_name="Description")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Изображение")
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('olga:product_detail', args=[str(self.id)])

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает обработки'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_CHOICES = [
        ('card', 'Банковская карта онлайн'),
        ('cash', 'Наличными при получении'),
        ('card_on_delivery', 'Картой при получении'),
    ]
    
    SHIPPING_CHOICES = [
        ('courier', 'Курьер'),
        ('pickup', 'Самовывоз'),
        ('post', 'Почта'),
    ]
    
    users = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="User"
    )
    order_number = models.PositiveIntegerField(unique=True, verbose_name="Order number")
    order_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Order amount")
    order_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Order status"
    )
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Registration date")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, verbose_name="Payment method")
    shipping_method = models.CharField(max_length=50, choices=SHIPPING_CHOICES, verbose_name="Shipping method")
    delivery_address = models.TextField(verbose_name="Delivery address")
    product = models.ManyToManyField(
        Product,
        related_name='orders',
        verbose_name="Products"
    )
    
    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"Order #{self.order_number}"
    
    def get_absolute_url(self):
        return reverse('olga:order_detail', args=[str(self.id)])
