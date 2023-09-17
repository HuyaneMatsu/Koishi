from .common_fields import *
from .waifu_stats import *

__all__ = (
    *common_fields.__all__,
    *waifu_stats.__all__,
)


from hata import bind,  ClientUserBase


bind(ClientUserBase, WaifuStats, 'waifu_stats', weak = True, weak_cache_size = 1000)
bind(ClientUserBase, CommonFields, 'common_fields', weak = True, weak_cache_size = 1000)
