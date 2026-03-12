from django.db import models
from django.contrib.auth.models import User

from products.models import Product

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новий'),
        ('processing', 'В обробці'),
        ('shipped', 'Відправлено'),
        ('completed', 'Завершено'),
        ('cancelled', 'Скасовано'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    shipping_name = models.CharField(max_length=100, verbose_name='Ім\'я отримувача')
    shipping_city = models.CharField(max_length=100, verbose_name='Місто')
    shipping_street = models.CharField(max_length=255, verbose_name='Вулиця')
    shipping_zip_code = models.CharField(max_length=20, verbose_name='Поштовий індекс')

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    comment = models.TextField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Замовлення'
        verbose_name_plural = 'Замовлення'
        ordering = ['-created_at']


    def __str__(self):
        return f'Замовлення #{self.id} від {self.created_at.strftime("%Y-%m-%d %H:%M:%S")}'
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    @property
    def total_price(self):
        return self.product_price * self.quantity

    class Meta:
        verbose_name = 'Товар замовлення'
        verbose_name_plural = 'Товари замовлення'
    
    def __str__(self):
        return f'{self.product_name} x {self.quantity} {self.total_price} (Замовлення #{self.order.id})'