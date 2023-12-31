__all__ = ()

from random import choice

from ...bots import FEATURE_CLIENTS

from .asset_listings.berigoo import BERIGOO_MEMES


@FEATURE_CLIENTS.interactions(is_global = True)
async def meme():
    """
    Shows a meme.
    
    This function is a coroutine.
    
    Returns
    -------
    url : `str`
    """
    return choice(BERIGOO_MEMES)
