__all__ = ()

from random import random

from hata import Embed

from ...bots import SLASH_CLIENT

from .constants import SEX_IMAGES
from .lock import check_lock_and_limit_level


@SLASH_CLIENT.interactions(is_global = True)
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
    if value > 0.15:
        level = 0
    elif value > 0.10:
        level = 1
    elif value > 0.06:
        level = 2
    elif value > 0.03:
        level = 3
    elif value > 0.01:
        level = 4
    else:
        level = 5
    
    level = check_lock_and_limit_level(event, level)
    
    
    return Embed().add_image(SEX_IMAGES[level])
