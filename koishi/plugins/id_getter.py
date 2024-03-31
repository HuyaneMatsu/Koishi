__all__ = ()

from hata import DATETIME_FORMAT_CODE, elapsed_time, id_to_datetime, now_as_id, parse_emoji
from hata.ext.slash import abort

from ..bots import FEATURE_CLIENTS


ID_GETTER_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    name = 'id',
    description = 'Shows the id of the selected entity',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)


@ID_GETTER_COMMANDS.interactions
async def user_(
    client,
    event,
    user: ('user', 'Who\'s id do you want to see?') = None,
):
    """Returns your or the selected user's identifier."""
    if user is None:
        user = event.user
    
    return str(user.id)


@ID_GETTER_COMMANDS.interactions
async def channel_(
    client,
    event,
    channel: ('channel', 'Which channel\'s id do you want to see?') = None,
):
    """Returns this or the selected channel's identifier."""
    if channel is None:
        channel = event.channel
    
    return str(channel.id)


@ID_GETTER_COMMANDS.interactions
async def guild_(client, event):
    """Returns the guild's identifier."""
    guild = event.guild
    if guild is None:
        abort('guild only')
    
    return str(guild.id)


@ID_GETTER_COMMANDS.interactions
async def role_(
    client,
    event,
    role: ('role', 'Which role\'s id do you want to see?') = None,
):
    """Returns this or the guild\'s default role's identifier."""
    guild = event.guild
    if guild is None:
        abort('guild only')
    
    if role is None:
        # Hax
        role_id = guild.id
    else:
        role_id = role.id
    
    return str(role_id)


@ID_GETTER_COMMANDS.interactions
async def sticker_(
    client,
    event,
    sticker_name: (str, 'Select a sticker', 'sticker'),
):
    guild = event.guild
    if guild is None:
        abort('guild only')
    
    sticker = guild.get_sticker_like(sticker_name)
    if sticker is None:
        abort('Unknown sticker')
    
    return str(sticker.id)


@sticker_.autocomplete('sticker')
async def autocomplete_sticker(client, event, value):
    guild = event.guild
    if guild is None:
        return
    
    if value is None:
        return sorted(
            sticker.name for sticker in guild.stickers.values()
        )
    
    return sorted(sticker.name for sticker in guild.get_stickers_like(value))



@ID_GETTER_COMMANDS.interactions
async def emoji_(
    client,
    event,
    emoji_name: (str, 'Select an emoji', 'emoji'),
):
    while True:
        emoji = parse_emoji(emoji_name)
        if emoji is not None:
            if not emoji.is_custom_emoji():
                abort('Not custom emoji')
            
            break
        
        guild = event.guild
        if guild is not None:
            start = emoji_name.startswith(':')
            end = len(emoji_name) - emoji_name.endswith(':')
            
            if end > start:
                emoji_name = emoji_name[start:end]
                emoji = guild.get_emoji_like(emoji_name)
                if emoji is not None:
                    break
        
        abort('Unknown emoji')
        return
    
    
    
    return str(emoji.id)


@emoji_.autocomplete('emoji')
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


@ID_GETTER_COMMANDS.interactions
async def now():
    """Returns the current time as discord snowflake."""
    return str(now_as_id())


@ID_GETTER_COMMANDS.interactions
async def to_time(
    snowflake: ('int', 'Id please!'),
):
    """Converts the given Discord snowflake to time."""
    time = id_to_datetime(snowflake)
    return f'{time:{DATETIME_FORMAT_CODE}}\n{elapsed_time(time)} ago'
