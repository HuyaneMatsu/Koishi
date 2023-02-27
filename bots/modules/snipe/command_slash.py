__all__ = ()

from hata import Client, is_id, parse_emoji
from hata.ext.slash import abort

from .cache_sticker import get_sticker
from .choice import CHOICE_TYPE_EMOJI, CHOICE_TYPE_STICKER, Choice
from .response_builder import build_initial_response


SLASH_CLIENT: Client


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
    
    abort('Could not resolve emoji')


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
        
        abort(f'Unknown or deleted sticker: {sticker_name_or_id}')
    
    guild = event.guild
    if (guild is not None):
        stickers = guild.get_stickers_like(sticker_name_or_id)
        if stickers:
            return stickers
    
    # Users can pass long strings as well. For this case limit the length of the returned value.
    if len(sticker_name_or_id) > 100:
        sticker_name_or_id = sticker_name_or_id[:100]
    
    return abort(f'Cannot find sticker in local scope: {sticker_name_or_id}.')
    

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
    show_for_invoking_user_only : `bool` = `True`, Optional
        Whether the message should show up only for the invoking user.
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    
    Returns
    -------
    interaction_response : ``InteractionResponse``
    """
    emojis = try_resolve_emojis(event, emoji_name)
    choices = [Choice(CHOICE_TYPE_EMOJI, emoji) for emoji in emojis]
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
    show_for_invoking_user_only : `bool` = `True`, Optional
        Whether the message should show up only for the invoking user.
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    
    Returns
    -------
    interaction_response : ``InteractionResponse``
    """
    stickers = await try_resolve_stickers(client, event, sticker_name_or_id)
    choices = [Choice(CHOICE_TYPE_STICKER, sticker) for sticker in stickers]
    return await build_initial_response(client, event, None, choices, not reveal, detailed)


@snipe_sticker.autocomplete('sticker')
async def snipe_sticker_autocomplete_sticker_name_or_id(event, value):
    """
    Tries to autocomplete the sticker by its name.
    
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
    guild = event.guild
    if guild is None:
        return None
    
    if value is None:
       stickers = sorted(guild.stickers.values())
    else:
        stickers = guild.get_stickers_like(value)
    
    return [sticker.name for sticker in stickers]
