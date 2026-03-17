from .models import Category
from django.core.cache import cache

CATEGORY_CACHE_TIL = 60 * 30  # 30 хвилин в секундах


def _get_category_context(request):
    categories = cache.get("categories_cache")
    if not categories:
        categories = list(Category.objects.all())
        cache.set("categories_cache", categories, CATEGORY_CACHE_TIL)
    return {"categories": categories}
