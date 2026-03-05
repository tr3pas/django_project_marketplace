
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
	path('', views.home, name='home'),
	path('products/', views.product_list, name='product_list'),
	path('products/category/<int:category_id>/', views.product_list, name='product_list_by_category'),
	path('products/<int:product_id>/', views.product_details, name='product_details'),
]