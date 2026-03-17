from django.test import TestCase
from django.contrib.auth import get_user_model
from products.models import Category, Product
from .models import Order, OrderItem

User = get_user_model()


class OrderTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="buyer",
            email="buyer@test.com",
            password="12345678",
        )
        self.category = Category.objects.create(name="Clothes")
        self.product = Product.objects.create(
            category=self.category,
            name="T-shirt",
            price=50,
            description= "Comfortable cotton t-shirt",
            color="Red",
            size="M",
        )
        self.order = Order.objects.create(user=self.user, total_price=self.product.price)

    def test_create_order(self):
        self.assertEqual(self.order.user, self.user)

    def test_add_item(self):
        item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            product_price=self.product.price  # 👈 ВАЖНО
        )
        self.assertEqual(item.quantity, 2)