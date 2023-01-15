__all__ = ()

from collections import OrderedDict

from hata import DiscordException, ERROR_CODES, STICKERS


STICKER_CACHE = OrderedDict()
STICKER_CACHE_MAX_SIZE = 1000


async def get_sticker(client, sticker_id):
    """
    Tries to get a sticker from cache. If not found requests it.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the sticker with if required.
    sticker_id : `int`
        The sticker's identifier.
    
    Returns
    -------
    sticker : `None`, ``Sticker``
    """
    try:
        sticker = STICKER_CACHE[sticker_id]
    except KeyError:
        sticker = await request_sticker(client, sticker_id)
        if sticker is None:
            return None
        
        if len(STICKER_CACHE) == STICKER_CACHE_MAX_SIZE:
            del STICKER_CACHE[next(iter(STICKER_CACHE))]
        
        STICKER_CACHE[sticker_id] = sticker
    
    else:
        STICKER_CACHE.move_to_end(sticker_id)
    
    return sticker


async def request_sticker(client, sticker_id):
    """
    Requests the sticker.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the sticker with.
    sticker_id : `int`
        The sticker's identifier.
    
    Returns
    -------
    sticker : `None`, ``Sticker``
    """
    sticker = STICKERS.get(sticker_id, None)
    
    if (sticker is None):
        request_local = False
    else:
        guild = sticker.guild
        if guild is None:
            request_local = False
        else:
            if (guild in client.guilds):
                request_local = True
            else:
                request_local = False
    
    # Try to request the sticker first from it's guild.
    if request_local:
        try:
            sticker = await client.sticker_guild_get(sticker, force_update = True)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            elif isinstance(err, DiscordException):
                # sticker deleted -> return `None`.
                if err.code == ERROR_CODES.unknown_sticker: 
                    return None
                
                # client removed -> move to global request
                elif err.code == ERROR_CODES.missing_access: 
                    pass
                
                else:
                    raise
            else:
                raise
        
        else:
            return sticker
    
    # Try to request the sticker globally.
    try:
        sticker = await client.sticker_get(sticker_id, force_update = True)
    except BaseException as err:
        if isinstance(err, ConnectionError):
            return
        
        if isinstance(err, DiscordException):
            # sticker deleted -> return `None`.
            if err.code == ERROR_CODES.unknown_sticker: 
                return None
        
        raise
    
    return sticker
