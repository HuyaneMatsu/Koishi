__all__ = ('COMMAND', )

import warnings

from ....bot_utils.constants import GUILD__SUPPORT
from ....bots import SLASH_CLIENT

from .info import *



COMMAND = SLASH_CLIENT.interactions(
    None,
    name = 'relationship',
    description = 'Wanna marry?',
    guild = GUILD__SUPPORT,
)


for sub_module in (
    info
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
