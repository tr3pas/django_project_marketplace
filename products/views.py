
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from .models import Category, Product

# Категорії
class CategoryListView(ListView):
	model = Category
	template_name = 'project/category_list.html'
	context_object_name = 'categories'

class CategoryDetailView(DetailView):
	model = Category
	template_name = 'project/category.html'
	context_object_name = 'category'


# Головна
def home(request):
	categories = Category.objects.all()
	return render(request, 'project/home.html', {'categories': categories})

# Список продуктів
def product_list(request, category_id=None):
	if category_id:
		products = Product.objects.filter(category_id=category_id)
		category = get_object_or_404(Category, id=category_id)
	else:
		products = Product.objects.all()
		category = None
	categories = Category.objects.all()
	return render(request, 'project/product_list.html', {'products': products, 'category': category, 'categories': categories})

# Деталі продукту
def product_details(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	categories = Category.objects.all()
	return render(request, 'project/product_details.html', {'product': product, 'categories': categories})
