from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_products_by_category(category_id):
    if not CACHE_ENABLED:
        return list(Product.objects.filter(category_id=category_id, status="published"))
    products_key = f"products_list_{category_id}"
    products = cache.get(products_key)
    if products is not None:
        return products
    products = list(Product.objects.filter(category_id=category_id, status="published"))
    cache.set(products_key, products, timeout=300)
    return products


def get_all_cached_products():
    if not CACHE_ENABLED:
        return list(Product.objects.filter(status="published").order_by("-created_at"))
    products_key = "products_list_all"
    products = cache.get(products_key)
    if products is not None:
        return products
    products = list(Product.objects.filter(status="published").order_by("-created_at"))
    cache.set(products_key, products, timeout=40)
    return products
