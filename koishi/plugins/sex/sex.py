__all__ = ()

from random import random

from hata import Embed

from ...bots import FEATURE_CLIENTS

from .constants import SEX_IMAGES
from .lock import check_lock_and_limit_level


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def sex(event):
    """
    You horny? Try your luck!
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    embed : ``Embed``
    """
    value = random()
    if value > 0.150: # no sex
        level = 0
    
    elif value > 0.100: # maybe sex
        level = 1
    
    elif value > 0.060: # probably sex
        level = 2
    
    elif value > 0.035: # yes sex
        level = 3
    
    elif value > 0.020: # yes sex fast
        level = 4
    
    elif value > 0.010: # totally sex
        level = 5
    
    elif value > 0.002: # sex 2.0
        level = 6
    
    else: # yes sex (koishi)
        level = 7
    
    level = check_lock_and_limit_level(event, level)
    
    return Embed().add_image(SEX_IMAGES[level])
