from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'product_price', 'quantity', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'shipping_name', 'status', 'total_price', 'created_at','shipping_city', 'shipping_zip_code')
    list_filter = ('status', 'created_at')
    search_fields = ('shipping_name', 'shipping_city', 'shipping_street')
    inlines = [OrderItemInline, ]
    readonly_fields = ('total_price', 'created_at', 'updated_at')