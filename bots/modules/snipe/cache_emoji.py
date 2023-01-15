__all__ = ()

from collections import OrderedDict

from hata import DiscordException, ERROR_CODES, ZEROUSER


EMOJI_CACHE = OrderedDict()
EMOJI_CACHE_MAX_SIZE = 1000


async def update_emoji_details(client, emoji):
    """
    Tries to update the emoji's details. If it is already in cache, does nothing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the emoji with if required.
    emoji : ``Emoji``
        The emoji's to update.
    """
    if not emoji.is_custom_emoji():
        return
    
    if emoji.id in EMOJI_CACHE:
        EMOJI_CACHE.move_to_end(emoji.id)
        return
    
    await request_emoji_details(client, emoji)
    
    if len(EMOJI_CACHE) == EMOJI_CACHE_MAX_SIZE:
        del EMOJI_CACHE[next(iter(EMOJI_CACHE))]
    
    EMOJI_CACHE[emoji.id] = emoji


async def request_emoji_details(client, emoji):
    """
    Requests the emoji's details.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The emoji to request the emoji with.
    emoji : ``Emoji``
        The emoji's to update.
    """
    guild = emoji.guild
    if (emoji.user is ZEROUSER) and (guild is not None) and (guild in client.guilds):
        try:
            await client.emoji_get(emoji, force_update = True)
        except DiscordException as err:
            if err.code not in (
                ERROR_CODES.missing_access, # Client removed.
            ):
                raise
