__all__ = ('STATS_COMMAND',)

from . import show


import warnings

from hata import Client


SLASH_CLIENT: Client

STATS_COMMAND = SLASH_CLIENT.interactions(
    None,
    name = 'stats',
    description = 'wanna know you waifu stats?',
    is_global = True,
)


for sub_module in (
    show,
):
    sub_module_attributes = sub_module.__all__
    sub_module_attribute_count = len(sub_module_attributes)
    
    if sub_module_attribute_count == 0:
        warnings.warn(f'`sub_module.__spec__.name` has no elements in it\'s `__all__`.')
        
    elif sub_module_attribute_count == 1:
        command = getattr(sub_module, sub_module_attributes[0])
        STATS_COMMAND.interactions(command)
    
    else:
        category = STATS_COMMAND.interactions(None, **getattr(sub_module, sub_module_attributes[0]))
        
        for sub_module_attribute_name in sub_module_attributes[1:]:
            command = getattr(sub_module, sub_module_attribute_name)
            category.interactions(command)
