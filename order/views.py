from django.shortcuts import render

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required


from cart.models import CartItem, Cart
from .models import Order, OrderItem
from products.models import Product
from account.models import Address
from .forms import CheckoutForm
from django.contrib import messages
from products.views import _get_category_context


def _get_cart_items(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.select_related('user').get(user=request.user)
            return [{"products": item.product, "quantity": item.quantity, "db_item": item}
                        for item in cart.items.select_related('product').all()]
        except Cart.DoesNotExist:
            return []
    
    else:                   
        cart = request.session.get('cart', {})
        if not cart:
            return []
        products = Product.objects.select_related('category').filter(id__in=cart.keys())
        return [{"products": product, "quantity": cart.get(str(product.id), 0), "db_item": None} 
                for product in products]

def _cart_clear(request):
    if request.user.is_authenticated:
        CartItem.objects.select_related('cart','product',).filter(cart__user=request.user).delete()
    else:
        request.session['cart'] = {}


def checkout(request):
    cart_items = _get_cart_items(request)
    if not cart_items:
        messages.error(request, 'Ваш кошик порожній. Додайте товари перед оформленням замовлення.')
        return redirect('cart:cart_details')
    
    initial = {}
    total_price = sum(item['products'].price * item['quantity'] for item in cart_items)

    if request.user.is_authenticated:
        try:
            name = f"{request.user.first_name} {request.user.last_name}"
            initial['shipping_name'] = name.strip() or request.user.username
            address = Address.objects.select_related('user').filter(user=request.user).first()
            if address:
                initial.update({
                    'shipping_city': address.city,
                    'shipping_street': address.street,
                    'shipping_zip_code': address.zip_code,
                    'shipping_country': address.country,
                })
        except Exception:
            pass
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST, initial=initial)
        if form.is_valid():
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                shipping_name=form.cleaned_data['shipping_name'],
                shipping_city=form.cleaned_data['shipping_city'],
                shipping_street=form.cleaned_data['shipping_street'],
                shipping_zip_code=form.cleaned_data['shipping_zip_code'],
                comment=form.cleaned_data.get('comment', ''),
                total_price=total_price,
                status='new'
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['products'],
                    product_name=item['products'].name,
                    product_price=item['products'].price,
                    quantity=item['quantity']
                )
            _cart_clear(request)
            return redirect('order:confirmation', order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)
    context = _get_category_context(request)
    return render(request, 'order/checkout.html', {**context, 'form': form, 'cart_items': cart_items, 'total_price': total_price})


def confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    context = _get_category_context(request)
    return render(request, 'order/confirmation.html', {**context, 'order': order})

@login_required
def history(request):
    orders = Order.objects.select_related('user').filter(user=request.user)
    context = _get_category_context(request)
    return render(request, 'order/history.html', {**context, 'orders': orders})
