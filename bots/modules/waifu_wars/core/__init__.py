from .constants import *
from .waifu_type import *

__all__ = (
    *constants.__all__,
    *waifu_type.__all__,
)

from hata import bind,  ClientUserBase


bind(ClientUserBase, waifu_type.WaifuType, 'waifu_stats', weak=True, weak_cache_size=1000)
