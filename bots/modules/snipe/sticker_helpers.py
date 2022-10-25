__all__ = ()

from collections import OrderedDict

from hata import DiscordException, ERROR_CODES, STICKERS


STICKER_CACHE = OrderedDict()
STICKER_CACHE_MAX_SIZE = 128


async def get_sticker(client, sticker_id):
    try:
        sticker = STICKER_CACHE[sticker_id]
    except KeyError:
        sticker = await request_sticker(client, sticker_id)
        
        if len(STICKER_CACHE) == 1000:
            del STICKER_CACHE[next(iter(STICKER_CACHE))]
        
        STICKER_CACHE[STICKER_CACHE_MAX_SIZE] = sticker
    
    else:
        STICKER_CACHE.move_to_end(sticker_id)
    
    return sticker


async def request_sticker(client, sticker_id):
    sticker = STICKERS.get(sticker_id, None)
    
    if (sticker is None):
        request_global = True
    else:
        guild = sticker.guild
        if guild is None:
            request_global = True
        else:
            if (guild in client.guilds):
                request_global = False
            else:
                request_global = True
    
    if request_global:
        coroutine = client.sticker_get(sticker_id, force_update = True)
    else:
        coroutine = client.sticker_guild_get(sticker, force_update = True)
    
    try:
        sticker = await coroutine
    except BaseException as err:
        if isinstance(err, ConnectionError):
            return
        
        if isinstance(err, DiscordException):
            if err.code == ERROR_CODES.unknown_sticker:
                return None
        
        raise
    
    return sticker
