from django import forms
from .models import Product, Category, Order, Users

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'quantity', 'description', 'image']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название товара'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Цена в рублях'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество на складе'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите описание товара'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название категории'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Введите описание категории'}),
        
        }

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['users', 'order_number', 'order_amount', 'order_status', 
                 'payment_method', 'shipping_method', 'delivery_address', 'product']
        widgets = {
            'users': forms.Select(attrs={'class': 'form-control'}),
            'order_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Номер заказа'}),
            'order_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Сумма заказа'}),
            'order_status': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('pending','Ожидает обработки'),
                ('processing','В обработке'),
                ('shipped','Отправлен'),
                ('delivered','Доставлен'),
                ('cancelled','Отменён'),
            ]),
            'payment_method': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('card', 'Банковская карта онлайн'),
                ('cash','Наличными при получении'),
                ('card_on_delivery','Картой при получении'),
            ]),
            'shipping_method': forms.Select(attrs={'class': 'form-control'}, choices=[
                ('courier','Курьером'),
                ('pickup', 'Самовывоз'),
                ('post','Почтой'),
            ]),
            'delivery_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Адрес доставки'}),
            'product': forms.SelectMultiple(attrs={'class': 'form-control', 'size': 5}),
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['name', 'address', 'email', 'phone_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ФИО'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Введите адрес доставки'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '+7 (999) 123-45-67'}),
        }