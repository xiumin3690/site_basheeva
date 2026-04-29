from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .cart import Cart
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Product, Category, Order, Users
from .forms import ProductForm, CategoryForm, OrderForm, UserForm

# Home page
def index(request):
    products = Product.objects.all()[:8]
    categories = Category.objects.all()
    return render(request, 'olga/index.html', {
        'products': products,
        'categories': categories
    })

# Product Views
class ProductListView(ListView):
    model = Product
    template_name = 'olga/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Фильтр по категории
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Поиск по названию
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(name__icontains=search_query)
        
        # Сортировка
        sort_by = self.request.GET.get('sort')
        if sort_by == 'price_asc':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_desc':
            queryset = queryset.order_by('-price')
        elif sort_by == 'name_asc':
            queryset = queryset.order_by('name')
        else:
            queryset = queryset.order_by('name')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['title'] = 'Все товары'
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'olga/product_detail.html'
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id)[:4]
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'olga/product_form.html'
    success_url = reverse_lazy('olga:product_list')
    login_url = '/login/'
    
    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно добавлен!')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'olga/product_form.html'
    login_url = '/login/'
    
    def get_success_url(self):
        return reverse_lazy('olga:product_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Товар успешно обновлён!')
        return super().form_valid(form)

# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'olga/category_list.html'
    context_object_name = 'categories'

class CategoryDetailView(DetailView):
    model = Category
    template_name = 'olga/category_detail.html'
    context_object_name = 'category'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = self.object.products.all()
        return context

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'olga/category_form.html'
    success_url = reverse_lazy('olga:category_list')
    login_url = '/login/'


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'olga/category_form.html'
    success_url = reverse_lazy('olga:category_list')
    login_url = '/login/'


# Order Views
class OrderListView(ListView):
    model = Order
    template_name = 'olga/order_list.html'
    context_object_name = 'orders'
    ordering = ['-registration_date']

class OrderDetailView(DetailView):
    model = Order
    template_name = 'olga/order_detail.html'
    context_object_name = 'order'

class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'olga/order_form.html'
    success_url = reverse_lazy('olga:order_list')
    login_url = '/login/'


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderForm
    template_name = 'olga/order_form.html'
    success_url = reverse_lazy('olga:order_list')
    login_url = '/login/'

# User Views
class UserListView(ListView):
    model = Users
    template_name = 'olga/user_list.html'
    context_object_name = 'users'

class UserDetailView(DetailView):
    model = Users
    template_name = 'olga/user_detail.html'
    context_object_name = 'user'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['orders'] = self.object.orders.all()
        return context

class UserCreateView(LoginRequiredMixin, CreateView):
    model = Users
    form_class = UserForm
    template_name = 'olga/user_form.html'
    success_url = reverse_lazy('olga:user_list')
    login_url = '/login/'

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = Users
    form_class = UserForm
    template_name = 'olga/user_form.html'
    success_url = reverse_lazy('olga:user_list')
    login_url = '/login/'

# ==================== АВТОРИЗАЦИЯ ====================

def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'olga/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'olga/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'olga/register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        Users.objects.create(name=username, email=email, address='', phone_number=0)
        
        messages.success(request, 'Регистрация прошла успешно! Теперь вы можете войти.')
        return redirect('olga:login')
    
    return render(request, 'olga/register.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(email=email)
            user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
            user = None
        if user is not None:
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('olga:index')
        else:
            messages.error(request, 'Неверный email или пароль')
    return render(request, 'olga/login.html')

def user_logout(request):
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('olga:index')

# ==================== КОРЗИНА ====================

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'olga/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product, quantity=1)
    messages.success(request, f'Товар "{product.name}" добавлен в корзину')
    return redirect('olga:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f'Товар "{product.name}" удалён из корзины')
    return redirect('olga:cart_detail')

@login_required(login_url='/login/')
def checkout(request):
    cart = Cart(request)
    if request.method == 'POST':
        try:
            user_profile = Users.objects.get(email=request.user.email)
        except Users.DoesNotExist:
            user_profile = Users.objects.create(
                name=request.user.username,
                email=request.user.email,
                address=request.POST.get('delivery_address', ''),
                phone_number=0
            )
        
        order_number = Order.objects.count() + 1
        order = Order.objects.create(
            users=user_profile,
            order_number=order_number,
            order_amount=cart.get_total_price(),
            order_status='pending',
            payment_method=request.POST.get('payment_method'),
            shipping_method=request.POST.get('shipping_method'),
            delivery_address=request.POST.get('delivery_address')
        )
        
        for item in cart:
            product = item['product']
            order.product.add(product)
        
        cart.clear()
        messages.success(request, f'Заказ №{order_number} оформлен!')
        return redirect('olga:order_detail', pk=order.pk)
    
    return render(request, 'olga/checkout.html', {'cart': cart})

# ==================== ЛИЧНЫЙ КАБИНЕТ ====================

@login_required(login_url='/login/')
def profile(request):
    try:
        user_profile = Users.objects.get(email=request.user.email)
        orders = user_profile.orders.all()
    except Users.DoesNotExist:
        orders = []
    return render(request, 'olga/profile.html', {'orders': orders})