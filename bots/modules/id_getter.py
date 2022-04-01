from hata import Client, parse_emoji
from hata.ext.slash import abort


SLASH_CLIENT: Client

ID_GETTER_COMMANDS = SLASH_CLIENT.interactions(
    None,
    name = 'id',
    description = 'Shows the id of the selected entity',
    is_global = True,
)


@ID_GETTER_COMMANDS.interactions
async def user_(client, event,
    user: ('user', 'Who\'s id do you want to see?') = None,
):
    """Returns your or the selected user's identifier."""
    if user is None:
        user = event.user
    
    return str(user.id)


@ID_GETTER_COMMANDS.interactions
async def channel_(client, event,
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
async def role_(client, event,
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
async def sticker_(client, event,
    sticker_name: ('sticker', 'Select a sticker', 'sticker'),
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
async def emoji_(client, event,
    emoji_name: ('sticker', 'Select a sticker', 'emoji_name'),
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
            return None
        
        emoji_names = []
        count = 0
        for emoji in guild.emojis.values():
            emoji_names.append(emoji)
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
            return None
    
    guild = event.guild
    if guild is None:
        return None
    
    start = emoji_name.startswith(':')
    length = len(emoji)
    end = length - emoji_name.endswith(':')
    stripped_emoji_name = emoji_name[start:end]
    
    if end != length:
        emoji = guild.get_emoji_like(stripped_emoji_name)
        if emoji.name == stripped_emoji_name:
            return [emoji_name]
        
        else:
            return None
    
    emojis = guild.get_emojis_like(stripped_emoji_name)
    emoji_names = sorted(emoji.name for emoji in emojis)
    if start:
        emoji_names = [':' + emoji_name for emoji_name in emoji_names]
    
    return emoji_names
