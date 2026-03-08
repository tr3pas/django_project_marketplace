
from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart_details, name='cart_details'),
	path('add/<int:product_id>/', views.add_cart, name='add_cart'),
	path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
	path('update/<int:product_id>/', views.update_cart, name='update_cart'),
]
