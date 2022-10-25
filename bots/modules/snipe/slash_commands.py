__all__ = ()

from hata import Client, is_id, parse_emoji
from hata.ext.slash import abort

from .constants import SNIPE_TYPE_EMOJI, SNIPE_TYPE_STICKER
from .lister_helpers import create_initial_response
from .sticker_helpers import get_sticker


SLASH_CLIENT: Client


SNIPE_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'snipe',
    description = 'snipe emojis or stickers!',
    is_global = True,
)


def try_resolve_emoji(event, raw_emoji):
    emoji = parse_emoji(raw_emoji)
    if (emoji is not None):
        return emoji
    
    # Try resolve emoji from guild's.
    guild = event.guild
    if (guild is not None):
        emoji = guild.get_emoji_like(raw_emoji)
        if (emoji is not None):
            return emoji
    
    abort('Could not resolve emoji')
    # Use return or the linter derps out
    return


async def emoji_command(
    event,
    raw_emoji: ('str', 'The emoji, or it\'s name.', 'emoji'),
):
    """Shows details about the given emoji."""
    emoji = try_resolve_emoji(event, raw_emoji)
    return create_initial_response(event, None, [emoji], SNIPE_TYPE_EMOJI)

emoji_autocompleted = SNIPE_COMMANDS.interactions(emoji_command, name='emoji-autocompleted')
emoji_ = SNIPE_COMMANDS.interactions(emoji_command, name='emoji')

@emoji_autocompleted.autocomplete('emoji')
async def autocomplete_emoji(client, event, emoji_name):
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


@SNIPE_COMMANDS.interactions
async def sticker_(
    client,
    event,
    sticker_name_or_id: ('str', 'Sticker to show', 'sticker'),
):
    """Shows details about the given sticker."""
    
    if is_id(sticker_name_or_id):
        sticker = await get_sticker(client, int(sticker_name_or_id))
        if (sticker is None):
            return abort(f'Unknown or deleted sticker: {sticker_name_or_id}')
    
    else:
        guild = event.guild
        if (guild is None):
            sticker = None
        else:
            sticker = guild.get_sticker_like(sticker_name_or_id)
        
        if sticker is None:
            # Users can pass long strings as well. For this case limit the length of the returned value.
            if len(sticker_name_or_id) > 100:
                sticker_name_or_id = sticker_name_or_id[:100]
            
            return abort(f'Cannot find sticker in local scope: {sticker_name_or_id}')
        
    
    return create_initial_response(event, None, [sticker], SNIPE_TYPE_STICKER)


@sticker_.autocomplete('sticker')
async def auto_complete_sticker_name(event, value):
    guild = event.guild
    if guild is None:
        return None
    
    if value is None:
       stickers = sorted(guild.stickers.values())
    else:
        stickers = guild.get_stickers_like(value)
    
    return [sticker.name for sticker in stickers]
