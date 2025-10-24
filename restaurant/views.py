from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import MenuItem, Order, OrderItem
from .decorators import admin_required

def home(request):
    return render(request, 'restaurant/home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'restaurant/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')
        
        # Try to authenticate with username first
        user = authenticate(request, username=username_or_email, password=password)
        
        # If that fails, try to find user by email and authenticate with username
        if user is None:
            try:
                from django.contrib.auth.models import User
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None
        
        if user is not None:
            login(request, user)
            # Check if user is admin based on email
            if user.email == 'admin@gmail.com':
                request.session['user_type'] = 'admin'
            else:
                request.session['user_type'] = 'user'
            return redirect('home')
        else:
            # If authentication failed, show error
            error_message = "Invalid credentials. For admin access, use: admin@gmail.com / admin"
            return render(request, 'restaurant/login.html', {'error': error_message})
    else:
        return render(request, 'restaurant/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def menu(request):
    items = MenuItem.objects.all()
    return render(request, 'restaurant/menu.html', {'items': items})

@login_required
def add_to_order(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    
    # Get the most recent order for the user, or create one if none exists
    order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    if not order:
        order = Order.objects.create(user=request.user)
    
    order_item, created = OrderItem.objects.get_or_create(order=order, menu_item=item)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('menu')

@login_required
def cart_view(request):
    # Current cart (latest order) - this is the active cart
    current_order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    
    # Previous completed orders (orders with items, excluding current)
    previous_orders = Order.objects.filter(
        user=request.user, 
        orderitem__isnull=False
    ).exclude(
        id=current_order.id if current_order else None
    ).distinct().order_by('-created_at')
    
    context = {
        'order': current_order,
        'previous_orders': previous_orders
    }
    
    return render(request, 'restaurant/cart.html', context)

@login_required
def order_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Calculate bill details
    order_items = order.orderitem_set.all()
    subtotal = sum(item.menu_item.price * item.quantity for item in order_items)
    
    # Basic billing calculations using Decimal for precision
    tax_rate = Decimal('0.18')  # 18% GST
    service_charge_rate = Decimal('0.10')  # 10% service charge
    
    service_charge = (subtotal * service_charge_rate).quantize(Decimal('0.01'))
    tax_amount = ((subtotal + service_charge) * tax_rate).quantize(Decimal('0.01'))
    total_amount = (subtotal + service_charge + tax_amount).quantize(Decimal('0.01'))
    
    context = {
        'order': order,
        'order_items': order_items,
        'subtotal': subtotal.quantize(Decimal('0.01')),
        'service_charge': service_charge,
        'tax_amount': tax_amount,
        'total_amount': total_amount,
        'tax_rate': float(tax_rate * 100),
        'service_charge_rate': float(service_charge_rate * 100),
    }
    
    return render(request, 'restaurant/order_bill.html', context)

@login_required
def submit_order(request):
    # Get the current (most recent) order
    order = Order.objects.filter(user=request.user).order_by('-created_at').first()
    if order and order.orderitem_set.exists():
        # Here you would typically integrate with a payment gateway
        # For this example, we'll just mark the order as "submitted"
        # by creating a new empty order for the user.
        Order.objects.create(user=request.user)
        return redirect('home')
    return redirect('cart')

@admin_required
@admin_required
def admin_orders(request):
    orders = Order.objects.all()
    unique_customers = orders.values_list('user', flat=True).distinct().count()
    context = {
        'orders': orders,
        'unique_customers': unique_customers,
    }
    return render(request, 'restaurant/admin_orders.html', context)

@admin_required
def admin_menu(request):
    items = MenuItem.objects.all()
    categories = MenuItem.objects.values_list('category', flat=True).distinct()
    category_count = categories.count()
    
    # Calculate price range
    if items:
        min_price = items.order_by('price').first().price
        max_price = items.order_by('-price').first().price
    else:
        min_price = max_price = 0
    
    context = {
        'items': items,
        'category_count': category_count,
        'min_price': min_price,
        'max_price': max_price,
    }
    return render(request, 'restaurant/admin_menu.html', context)

@admin_required
def add_menu_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        photo = request.FILES.get('photo')
        
        if name and description and price and category:
            MenuItem.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                photo=photo
            )
            return redirect('admin_menu')
    
    return render(request, 'restaurant/add_menu_item.html')

@admin_required
def edit_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        photo = request.FILES.get('photo')
        
        if name and description and price and category:
            item.name = name
            item.description = description
            item.price = price
            item.category = category
            if photo:
                item.photo = photo
            item.save()
            return redirect('admin_menu')
    
    return render(request, 'restaurant/edit_menu_item.html', {'item': item})

@admin_required
def delete_menu_item(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    item.delete()
    return redirect('admin_menu')

def debug_view(request):
    """Debug view to check user and session state"""
    from django.http import HttpResponse
    
    debug_info = {
        'user_authenticated': request.user.is_authenticated,
        'username': request.user.username if request.user.is_authenticated else 'Anonymous',
        'user_email': request.user.email if request.user.is_authenticated else 'No email',
        'session_user_type': request.session.get('user_type', 'Not set'),
        'session_data': dict(request.session),
        'is_superuser': request.user.is_superuser if request.user.is_authenticated else False,
        'admin_check': request.user.is_authenticated and request.session.get('user_type') == 'admin',
    }
    
    # Check for orders
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        debug_info['user_orders_count'] = orders.count()
        debug_info['user_orders'] = [f"Order {o.id} - {o.created_at}" for o in orders[:5]]
    
    html = "<h1>Debug Information</h1>"
    for key, value in debug_info.items():
        html += f"<p><strong>{key}:</strong> {value}</p>"
    
    html += f"<p><a href='/manage/menu/'>Admin Menu Link</a></p>"
    html += f"<p><a href='/manage/orders/'>Admin Orders Link</a></p>"
    html += f"<p><a href='/cart/'>My Orders</a></p>"
    html += f"<p><a href='/login/'>Login</a></p>"
    html += f"<p><a href='/'>Home</a></p>"
    
    return HttpResponse(html)
