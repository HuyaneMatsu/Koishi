__all__ = ()

from hata import (
    DiscordException, ERROR_CODES, Emoji, GUILDS, STICKERS, SoundboardSound, Sticker, ZEROUSER,
    create_partial_soundboard_sound_from_id
)

from ...bot_utils.user_getter import _get_client

from .constants import CACHE_EMOJI, CACHE_EMOJI_SIZE_MAX, CACHE_STICKER, CACHE_STICKER_SIZE_MAX


async def update_emoji_details(emoji):
    """
    Tries to update the emoji's details. If it is already in cache, does nothing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji's to update.
    """
    if not emoji.is_custom_emoji():
        return
    
    if emoji.id in CACHE_EMOJI:
        CACHE_EMOJI.move_to_end(emoji.id)
        return
    
    await request_emoji_details(emoji)
    
    if len(CACHE_EMOJI) == CACHE_EMOJI_SIZE_MAX:
        del CACHE_EMOJI[next(iter(CACHE_EMOJI))]
    
    CACHE_EMOJI[emoji.id] = emoji


async def request_emoji_details(emoji):
    """
    Requests the emoji's details.
    
    This function is a coroutine.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji's to update.
    """
    if (emoji.user is not ZEROUSER):
        return
    
    guild = emoji.guild
    if (guild is None):
        return
    
    for client in guild.iter_clients():
        try:
            await client.emoji_get_guild(emoji, force_update = True)
        except DiscordException as err:
            if err.code not in (
                ERROR_CODES.missing_access, # Client removed.
            ):
                raise
        break


async def update_soundboard_sound_details(soundboard_sound):
    """
    Tries to update the soundboard sound's details. If the sound is already in cache does nothing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    soundboard_sound : ``SoundboardSound``
        The soundboard sound to update.
    """
    guild = soundboard_sound.guild
    if (guild is None):
        return
    
    for client in guild.iter_clients():
        await client.request_soundboard_sounds([guild.id])
        break


async def request_soundboard_sounds_of(guild):
    """
    Requests the soundboard sounds of the given guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild : ``Guild``
        Guild to request its soundboard sounds of.
    """
    for client in guild.iter_clients():
        await client.request_soundboard_sounds([guild.id])
        break


async def get_soundboard_sound(guild_id, sound_id):
    """
    Gets the soundboard sound described by `guild_id` and `sound_id`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    guild_id : `int`
        The soundboard sound's guild's identifier.
    
    sound_id : `int`
        The soundboard sound's identifier.
    
    Returns
    -------
    sound : ``SoundboardSound``
    """
    if (not guild_id) or (not sound_id):
        return None
    
    try:
        guild = GUILDS[guild_id]
    except KeyError:
        return None
    
    await request_soundboard_sounds_of(guild)
    sound = create_partial_soundboard_sound_from_id(sound_id, guild_id)
    
    return sound


async def get_sticker(sticker_id):
    """
    Tries to get a sticker from cache. If not found requests it.
    
    This function is a coroutine.
    
    Parameters
    ----------
    sticker_id : `int`
        The sticker's identifier.
    
    Returns
    -------
    sticker : ``None | Sticker``
    """
    try:
        sticker = CACHE_STICKER[sticker_id]
    except KeyError:
        sticker = await request_sticker(sticker_id)
        if sticker is None:
            return None
        
        if len(CACHE_STICKER) == CACHE_STICKER_SIZE_MAX:
            del CACHE_STICKER[next(iter(CACHE_STICKER))]
        
        CACHE_STICKER[sticker_id] = sticker
    
    else:
        CACHE_STICKER.move_to_end(sticker_id)
    
    return sticker


async def request_sticker(sticker_id):
    """
    Requests the sticker.
    
    This function is a coroutine.
    
    Parameters
    ----------
    sticker_id : `int`
        The sticker's identifier.
    
    Returns
    -------
    sticker : ``None | Sticker``
    """
    sticker = STICKERS.get(sticker_id, None)
    
    if (sticker is not None):
        guild = sticker.guild
        if (guild is not None):
            for client in guild.iter_clients():
                try:
                    sticker = await client.sticker_get_guild(sticker, force_update = True)
                except ConnectionError:
                    return
                
                except DiscordException as exception:
                    # sticker deleted -> return `None`.
                    if exception.code == ERROR_CODES.unknown_sticker: 
                        return None
                    
                    # client removed -> move to global request
                    if exception.code == ERROR_CODES.missing_access: 
                        break
                    
                    raise
                
                else:
                    return sticker
                break
    
    # Try to request the sticker globally.
    client = _get_client()
    try:
        sticker = await client.sticker_get(sticker_id, force_update = True)
    except ConnectionError:
        return
    
    except DiscordException as exception:
        # sticker deleted -> return `None`.
        if exception.code == ERROR_CODES.unknown_sticker: 
            return None
        
        raise
    
    return sticker


async def update_entity_details(entity):
    """
    Updates the entity's details.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entity : ``Emoji | Sticker | SoundboardSound``
        Entity to update.
    """
    entity_type = type(entity)
    if entity_type is Emoji:
        await update_emoji_details(entity)
    
    elif entity_type is Sticker:
        await get_sticker(entity.id)
    
    elif entity_type is SoundboardSound:
        await update_soundboard_sound_details(entity)
