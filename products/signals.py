from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Product, Category
from django.core.cache import cache
from .views import CATEGORY_CACHE_KEY


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_category_cache(sender, **kwargs):
    cache.delete(CATEGORY_CACHE_KEY)


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def clear_product_cache(sender, instance, **kwargs):
    cache.delete("products_all")
    cache.delete(f"products_category_{instance.category_id}")
    cache.delete(f"product_{instance.id}")
