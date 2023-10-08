from hata import Client
from hata.ext.plugin_loader import require

# This will fail
require(Koishi = Client)


from .command import *
from .constants import *
from .shared_logic import *

from .helpers import *


__all__ = (
    *command.__all__,
    *constants.__all__,
    *shared_logic.__all__,
    
    *helpers.__all__,
)
