__all__ = ('COMMAND', )

import warnings

from ....bot_utils.constants import GUILD__SUPPORT
from ....bots import FEATURE_CLIENTS

from .behavior import *
from .filter_add import *
from .filter_list import *
from .filter_remove import *
from .leave import *
from .move import *
from .pause import *
from .play import *
from .queue import *
from .remove import *
from .restart import *
from .resume import *
from .seek import *
from .skip import *
from .stop import *
from .volume import *



COMMAND = FEATURE_CLIENTS.interactions(
    None,
    name = 'voice',
    description = 'Voice commands',
    guild = GUILD__SUPPORT,
)


for sub_module in (
    behavior, filter_add, filter_list, filter_remove, leave, move, pause, play, queue, remove, restart, resume,
    seek, skip, stop, volume
):
    sub_module_attributes = sub_module.__all__
    sub_module_attribute_count = len(sub_module_attributes)
    
    if sub_module_attribute_count == 0:
        warnings.warn(f'`sub_module.__spec__.name` has no elements in it\'s `__all__`.')
        
    elif sub_module_attribute_count == 1:
        command = getattr(sub_module, sub_module_attributes[0])
        COMMAND.interactions(command)
    
    else:
        category = COMMAND.interactions(None, **getattr(sub_module, sub_module_attributes[0]))
        
        for sub_module_attribute_name in sub_module_attributes[1:]:
            command = getattr(sub_module, sub_module_attribute_name)
            category.interactions(command)
