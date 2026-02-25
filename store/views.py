from django.shortcuts import render, get_object_or_404
from .models import CartItem, Order, OrderItem, Product
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from django.shortcuts import redirect


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, id=pk)

    if request.method == "POST":
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')

    return render(request, 'product_detail.html', {'product': product})
@login_required
def cart_view(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.total_price() for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})
@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.total_price() for item in items)

    return render(request, 'cart.html', {
        'items': items,
        'total': total
    })
@login_required
def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


@login_required
def remove_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart')
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect('cart')

    order = Order.objects.create(user=request.user)

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    items.delete()  # clear cart

    return redirect('order_success')
@login_required
def order_success(request):
    return render(request, 'order_success.html')
from django.shortcuts import redirect

@login_required
def increase_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):
    item = CartItem.objects.get(id=item_id)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


@login_required
def remove_item(request, item_id):
    item = CartItem.objects.get(id=item_id)
    item.delete()
    return redirect('cart')
@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)
    items = CartItem.objects.filter(cart=cart)

    if not items:
        return redirect('cart')

    order = Order.objects.create(user=request.user)

    for item in items:
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

    items.delete()  # clear cart

    return redirect('order_success')
@login_required
def order_success(request):
    return render(request, 'order_success.html')
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'order_history.html', {'orders': orders})