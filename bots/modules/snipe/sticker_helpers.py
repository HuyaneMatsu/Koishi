__all__ = ()

from hata import DiscordException, ERROR_CODES, STICKERS


async def get_sticker(client, sticker_id):
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
        coroutine = client.sticker_get(sticker_id, force_update=True)
    else:
        coroutine = client.sticker_guild_get(sticker, force_update=True)
    
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
