from django.core.cache import cache
from functools import wraps

class CacheService:
    @staticmethod
    def cache_decorator(timeout=3600 * 24):
        def decorator(func):
            @wraps(func)
            def wrapper(self, request, *args, **kwargs):
                print(request)
                cache_key = f"{self.__class__.__name__}-{request.user.client.city}-{func.__name__}"
                result = cache.get(cache_key)
                if result is None:
                    result = func(self, request, *args, **kwargs)
                    cache.set(cache_key, result, timeout=timeout)
                return result
            return wrapper
        return decorator

    @staticmethod
    def invalidate_cache(client_city, resource_name):
        cache_key = f"{resource_name}-{client_city}"
        cache.delete(cache_key)
