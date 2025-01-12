__all__ = ()

from collections import OrderedDict

from scarletio import WeakValueDictionary


RELATIONSHIP_REQUEST_CACHE = WeakValueDictionary()

RELATIONSHIP_REQUEST_CACHE_LISTING = OrderedDict()
RELATIONSHIP_REQUEST_CACHE_LISTING_SIZE_MAX = 100


RELATIONSHIP_CACHE = WeakValueDictionary()

RELATIONSHIP_CACHE_LISTING = OrderedDict()
RELATIONSHIP_CACHE_LISTING_SIZE_MAX = 100


ACTION_NAME_UNKNOWN = 'pudding'
