from django.test import TestCase
from .models import Category, Product


class CategoryModelTest(TestCase):
    def test_create_category(self):
        category = Category.objects.create(name="Test Category")
        self.assertEqual(category.name, "Test Category")

    def test_str(self):
        category = Category.objects.create(name="Category")
        self.assertEqual(str(category), category.name)


class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Tech")

    def test_create_product(self):
        product = Product.objects.create(
            category=self.category,
            name="Phone",
            price=100
        )
        self.assertEqual(product.name, "Phone")
        self.assertEqual(product.category, self.category)

    def test_str(self):
        product = Product.objects.create(
            category=self.category,
            name="Laptop",
            price=200
        )
        self.assertEqual(str(product), product.name)