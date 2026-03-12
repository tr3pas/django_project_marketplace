
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

def _get_category_context(request):
	categories = Category.objects.all()
	return {'categories': categories}


# Головна
def home(request):
	categories = Category.objects.all()
	return render(request, 'product/home.html', {'categories': categories})

# Список продуктів
def product_list(request, category_id=None):
	if category_id:
		products = Product.objects.select_related('category',).filter(category_id=category_id)
		category = get_object_or_404(Category, id=category_id)
	else:
		products = Product.objects.select_related('category').all()
		category = None
	context = _get_category_context(request)
	return render(request, 'product/product_list.html', {**context, 'products': products, 'category': category})

# Деталі продукту
def product_details(request, product_id):
	product = get_object_or_404(Product, id=product_id)
	context = _get_category_context(request)
	return render(request, 'product/product_details.html', {**context, 'product': product})
