from django.test import TestCase
from products.models import Category, Product
from .models import Cart, CartItem
from django.contrib.auth import get_user_model

User = get_user_model()


class CartTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="cartuser", email="cartuser@test.com", password="12345678"
        )
        self.category = Category.objects.create(name="Shoes")
        self.product = Product.objects.create(
            category=self.category, name="Sneakers", price=1000
        )
        self.cart = Cart.objects.create(user=self.user)

    def test_add_item(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        self.assertEqual(item.quantity, 2)

    def test_total(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=3)

        items = CartItem.objects.filter(cart=self.cart)
        total = sum(i.product.price * i.quantity for i in items)

        self.assertEqual(total, 3000)
