__all__ = ()

from hata import create_partial_soundboard_sound_from_id


async def update_soundboard_sound_details(client, soundboard_sound):
    """
    Tries to update the soundboard sound's details. If the sound is already in cache does nothing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the soundboard sound with if required.
    soundboard_sound : ``SoundboardSound``
        The soundboard sound to update.
    """
    guild_id = soundboard_sound.guild_id
    if guild_id:
        await client.request_soundboard_sounds([guild_id])


async def get_soundboard_sound(client, guild_id, sound_id):
    """
    Gets the soundboard sound described by `guild_id` and `sound_id`.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to request the soundboard sound as required.
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
    
    sound = create_partial_soundboard_sound_from_id(sound_id, guild_id)
    await client.request_soundboard_sounds([guild_id])
    return sound
