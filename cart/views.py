from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from .models import CartItem, Cart
from products.models import Product
from products.views import _get_category_context


def get_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        cart = request.session.get('cart', {})
    return cart


def get_cart_items(request):
    """Returns a list of cart items and total for template context."""
    if request.user.is_authenticated:
        cart = get_cart(request)
        items = []
        total = 0
        for item in CartItem.objects.select_related('product','cart','product__category').filter(cart=cart):
            item.subtotal = item.product.price * item.quantity
            items.append(item)
            total += item.subtotal
        return items, total
    else:
        cart = request.session.get('cart', {})
        items = []
        total = 0
        for product in Product.objects.select_related('category').filter(id__in=cart.keys()):
            quantity = cart.get(str(product.id), 0)
            subtotal = product.price * quantity
            item = {'product': product, 'quantity': quantity, 'subtotal': subtotal}
            items.append(item)
            total += subtotal
        return items, total


@require_POST
def add_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        cart = request.session.get('cart', {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        request.session['cart'] = cart
    return redirect('cart:cart_details')


def cart_details(request):
    cart_items, total = get_cart_items(request)
    context = _get_category_context(request)
    return render(request, 'cart/cart_details.html', {**context, 'cart_items': cart_items, 'total': total})


@require_POST
def remove_from_cart(request, product_id):
    if request.user.is_authenticated:
        cart = get_cart(request)
        CartItem.objects.select_related('product','cart','product__category').filter(cart=cart, product_id=product_id).delete()
    else:
        cart = request.session.get('cart', {})
        cart.pop(str(product_id), None)
        request.session['cart'] = cart
    return redirect('cart:cart_details')


@require_POST
def update_cart(request, product_id):
    quantity = max(1, int(request.POST.get('quantity', 1)))
    if request.user.is_authenticated:
        cart = get_cart(request)
        CartItem.objects.select_related('product','cart','product__category').filter(cart=cart, product_id=product_id).update(quantity=quantity)
    else:
        cart = request.session.get('cart', {})
        if str(product_id) in cart:
            cart[str(product_id)] = quantity
            request.session['cart'] = cart
    return redirect('cart:cart_details')