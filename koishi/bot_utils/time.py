__all__ = ('unix_time_nano_seconds_get', 'unix_time_seconds_get')

from time import time

try:
    from time import time_ns as unix_time_nano_seconds_get
except ImportError:
    def unix_time_nano_seconds_get():
        return int(time() * 1000000000.0)


def unix_time_seconds_get():
    return int(time())
