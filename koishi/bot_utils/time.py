__all__ = ('get_unix_time_nano_seconds',)

try:
    from time import time_ns as get_unix_time_nano_seconds
except ImportError:
    from time import time
    
    def get_unix_time_nano_seconds():
        return int(time() * 1000000000.0)
