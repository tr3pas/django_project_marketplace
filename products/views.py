
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Category, Product
from .context_proccesor import _get_category_context
from django.core.cache import cache
from django_ratelimit.decorators import ratelimit

CATEGORY_CACHE_KEY = 'categories_cache'
CATEGORY_CACHE_TIL = 60 * 60  # 1 година в секундах

# Категорії
class CategoryListView(ListView):
	model = Category
	template_name = 'project/category_list.html'
	context_object_name = 'categories'

class CategoryDetailView(DetailView):
	model = Category
	template_name = 'project/category.html'
	context_object_name = 'category'

# Головна сторінка
@ratelimit(key='ip', rate='100/m', method='GET', block=True)
def home(request):
	categories = cache.get(CATEGORY_CACHE_KEY)
	if not categories:
		categories = list(Category.objects.all())
		cache.set(CATEGORY_CACHE_KEY, categories, CATEGORY_CACHE_TIL)
	return render(request, 'product/home.html', {'categories': categories})

# Список продуктів
@ratelimit(key='ip', rate='100/m', method='GET', block=True)
def product_list(request, slug=None):
	if slug:
		products = cache.get(f'products_category_{slug}')
		if not products:
			products = list(Product.objects.select_related('category',).filter(category__slug=slug))
			cache.set(f'products_category_{slug}', products, CATEGORY_CACHE_TIL)
	else:
		products = cache.get('products_all')
		if not products:
			products = list(Product.objects.select_related('category').all())
			cache.set('products_all', products, CATEGORY_CACHE_TIL)
	context = _get_category_context(request)
	return render(request, 'product/product_list.html', {**context, 'products': products})

# Деталі продукту
@ratelimit(key='ip', rate='100/m', method='GET', block=True)
def product_details(request, slug):
	product = cache.get(f'product_{slug}')
	if not product:
		product = get_object_or_404(Product, slug=slug)
		cache.set(f'product_{product.slug}', product, CATEGORY_CACHE_TIL)
	context = _get_category_context(request)
	return render(request, 'product/product_details.html', {**context, 'product': product})
