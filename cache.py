from collections import defaultdict
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

cache_store = defaultdict(dict)


def cache_using(store: str):
    """ Decorator to select which cache decorator to use """
    return {
        "redis": redis_cache_by_first_arg,
        "memory": memory_cache_by_first_arg,
    }[store.lower()]


def memory_cache_by_first_arg(fn):
    """ Simple decorator to cache function result in-memory """
    function_name = fn.__name__

    def decorated(*args, **kwargs):
        if len(args) == 0:
            return fn(*args, **kwargs)

        cache_key = args[0]
        if cache_store[function_name].get(cache_key, None):
            return r.get(cache_key)
        else:
            result = fn(*args, **kwargs)
            r.set(cache_key, result)
            return result
    return decorated


def redis_cache_by_first_arg(fn):
    """ Simple decorator to cache function result using redis """
    function_name = fn.__name__

    def decorated(*args, **kwargs):
        if len(args) == 0:
            return fn(*args, **kwargs)

        cache_key = f"{function_name}|{args[0]}"
        if r.get(cache_key):
            return r.get(cache_key)
        else:
            result = fn(*args, **kwargs)
            r.set(cache_key, result)
            return result
    return decorated
