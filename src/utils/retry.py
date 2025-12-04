import time
import functools

def retry(max_retries=3, initial_delay=1.0, backoff=2.0, exceptions=(Exception,)):
    def deco(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            delay = initial_delay
            for attempt in range(1, max_retries+1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_retries:
                        raise
                    time.sleep(delay)
                    delay *= backoff
        return wrapper
    return deco
