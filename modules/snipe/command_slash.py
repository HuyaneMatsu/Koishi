__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, is_id, parse_emoji, parse_message_jump_url
from hata.ext.slash import abort

from bots import SLASH_CLIENT

from .cache_sticker import get_sticker
from .choice import Choice
from .choice_type import ChoiceTypeEmoji, ChoiceTypeSoundboardSound, ChoiceTypeSticker
from .command_helpers_snipe_whole_message import respond_snipe_whole_message
from .response_builder import build_initial_response


SNIPE_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'snipe',
    description = 'snipe emojis or stickers!',
    is_global = True,
)


def try_resolve_emojis(event, emoji_name):
    """
    Tries to resolve emojis from a raw version.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    emoji_name : `str`
        The emoji's name.
    
    Returns
    -------
    emojis : `list` of ``Emoji``
    
    Notes
    -----
    Aborts the interaction if no emoji is found.
    """
    emoji = parse_emoji(emoji_name)
    if (emoji is not None):
        return [emoji]
    
    # Try resolve emoji from guild's.
    guild = event.guild
    if (guild is not None):
        emojis = guild.get_emojis_like(emoji_name)
        if emojis:
            return emojis
    
    return abort('Could not resolve emoji')


async def try_resolve_stickers(client, event, sticker_name_or_id):
    """
    Tries to resolve stickers from a raw version.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    sticker_name_or_id : `str`
        The sticker's name or its identifier.
    
    Returns
    -------
    stickers : `list` of ``Sticker``
    
    Notes
    -----
    Aborts the interaction if no sticker is found.
    """
    if is_id(sticker_name_or_id):
        sticker = await get_sticker(client, int(sticker_name_or_id))
        if (sticker is not None):
            return [sticker]
        
        return abort(f'Unknown or deleted sticker: {sticker_name_or_id}')
    
    guild = event.guild
    if (guild is not None):
        stickers = guild.get_stickers_like(sticker_name_or_id)
        if stickers:
            return stickers
    
    # Users can pass long strings as well. For this case limit the length of the returned value.
    if len(sticker_name_or_id) > 100:
        sticker_name_or_id = sticker_name_or_id[:100]
    
    return abort(f'Cannot find sticker in local scope: {sticker_name_or_id}.')


async def try_resolve_soundboard_sounds(client, event, soundboard_sound_name):
    """
    Tres to resolve the sound by its name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    soundboard_sound_name : `str`
        The sound's name.
    
    Returns
    -------
    soundboard_sounds : `list` of ``SoundboardSound``
    
    Notes
    -----
    Aborts the interaction if no soundboard sound is found.
    """
    guild = event.guild
    if guild is not None:
        await client.request_soundboard_sounds([guild])
        
        soundboard_sounds = guild.get_soundboard_sounds_like(soundboard_sound_name)
        if soundboard_sounds:
            return soundboard_sounds
    
    # Users can pass long strings as well. For this case limit the length of the returned value.
    if len(soundboard_sound_name) > 100:
        soundboard_sound_name = soundboard_sound_name[:100]
    
    return abort(f'Cannot find soundboard sound in local scope: {soundboard_sound_name}.')
        


async def snipe_emoji(
    client,
    event,
    emoji_name: (str, 'The emoji, or it\'s name.', 'emoji'),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Shows details about the given emoji.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    event : ``InteractionEvent``
        The received interaction event.
    emoji_name : `str`
        The emoji's name to resolve.
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    
    Returns
    -------
    interaction_response : ``InteractionResponse``
    """
    emojis = try_resolve_emojis(event, emoji_name)
    choices = [Choice(emoji, ChoiceTypeEmoji) for emoji in emojis]
    return await build_initial_response(client, event, None, choices, not reveal, detailed)


snipe_emoji_plain = SNIPE_COMMANDS.interactions(snipe_emoji, name = 'emoji')
snipe_emoji_autocompleted = SNIPE_COMMANDS.interactions(snipe_emoji, name = 'emoji-autocompleted')


@snipe_emoji_autocompleted.autocomplete('emoji')
async def snipe_emoji_autocomplete_emoji_name(event, emoji_name):
    """
    Tries to autocomplete the emoji by its name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    emoji_name : `None`, `str`
        The typed value.
    
    Returns
    -------
    suggestions : `None`, `list` of `str`
    """
    if emoji_name is None:
        guild = event.guild
        if guild is None:
            return
        
        emoji_names = []
        count = 0
        for emoji in guild.emojis.values():
            emoji_names.append(emoji.name)
            count += 1
            if count == 25:
                break
        
        emoji_names.sort()
        return emoji_names
    
    
    emoji = parse_emoji(emoji_name)
    if emoji is not None:
        if emoji.is_custom_emoji():
            return [emoji.as_emoji]
        else:
            return
    
    guild = event.guild
    if guild is None:
        return
    
    emojis = guild.get_emojis_like(emoji_name)
    return sorted(emoji.name for emoji in emojis)


@SNIPE_COMMANDS.interactions(name = 'soundboard-sound')
async def snipe_soundboard_sound(
    client,
    event,
    soundboard_sound_name: ('str', 'SoundboardSound to show', 'soundboard-sound'),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Shows details about the given soundboard sound.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    event : ``InteractionEvent``
        The received interaction event.
    soundboard_sound_name : `str`
        The soundboard sound's name.
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    
    Returns
    -------
    interaction_response : ``InteractionResponse``
    """
    soundboard_sounds = await try_resolve_soundboard_sounds(client, event, soundboard_sound_name)
    choices = [Choice(soundboard_sound, ChoiceTypeSoundboardSound) for soundboard_sound in soundboard_sounds]
    return await build_initial_response(client, event, None, choices, not reveal, detailed)


@snipe_soundboard_sound.autocomplete('soundboard_sound')
async def snipe_soundboard_sound_autocomplete_soundboard_sound_name(client, event, soundboard_sound_name):
    """
    Tries to autocomplete the soundboard sound by its name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    event : ``InteractionEvent``
        The received interaction event.
    soundboard_sound_name : `None`, `str`
        The typed value.
    
    Returns
    -------
    suggestions : `None`, `list` of `str`
    """
    guild = event.guild
    if guild is None:
        return None
    
    await client.request_soundboard_sounds([guild])
        
    if soundboard_sound_name is None:
       soundboard_sounds = sorted(guild.iter_soundboard_sounds())
    else:
        soundboard_sounds = guild.get_soundboard_sounds_like(soundboard_sound_name)
    
    return [soundboard_sound.name for soundboard_sound in soundboard_sounds]


@SNIPE_COMMANDS.interactions(name = 'sticker')
async def snipe_sticker(
    client,
    event,
    sticker_name_or_id: ('str', 'Sticker to show', 'sticker'),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Shows details about the given sticker.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    event : ``InteractionEvent``
        The received interaction event.
    sticker_name_or_id : `str`
        The sticker's identifier or name to resolve.
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    
    Returns
    -------
    interaction_response : ``InteractionResponse``
    """
    stickers = await try_resolve_stickers(client, event, sticker_name_or_id)
    choices = [Choice(sticker, ChoiceTypeSticker) for sticker in stickers]
    return await build_initial_response(client, event, None, choices, not reveal, detailed)


@snipe_sticker.autocomplete('sticker')
async def snipe_sticker_autocomplete_sticker_name_or_id(event, sticker_name):
    """
    Tries to autocomplete the sticker by its name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    sticker_name : `None`, `str`
        The typed value.
    
    Returns
    -------
    suggestions : `None`, `list` of `str`
    """
    guild = event.guild
    if guild is None:
        return None
    
    if sticker_name is None:
       stickers = sorted(guild.stickers.values())
    else:
        stickers = guild.get_stickers_like(sticker_name)
    
    return [sticker.name for sticker in stickers]


@SNIPE_COMMANDS.interactions(name = 'message')
async def snipe_message_with_url(
    client,
    event,
    message_jump_url: ('str', 'Message\'s url.'),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Snipes the message defined by its url.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    event : ``InteractionEvent``
        The received interaction event.
    message_jump_url : `str`
        The message's url to resolve.
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    """
    guild_id, channel_id, message_id = parse_message_jump_url(message_jump_url)
    if not message_id:
        abort('The given message url is invalid.')
    
    # TODO: Maybe add pre-validation?
    
    try:
        message = await client.message_get((channel_id, message_id))
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code in (
            ERROR_CODES.unknown_channel, # message deleted
            ERROR_CODES.unknown_message, # channel deleted
        ):
            # The message is already deleted.
            return abort('The message has been already deleted.')
        
        # Client not in the guild
        if err.code == ERROR_CODES.missing_access: # client removed
            return abort('I am not in the guild.' if guild_id else 'I am not in the channel.')
        
        # No permissions?
        if err.code == ERROR_CODES.missing_permissions: # no permissions
            return abort('I lack permission to get that message.')
        
        raise
    
    return await respond_snipe_whole_message(client, event, message, not reveal, detailed)
