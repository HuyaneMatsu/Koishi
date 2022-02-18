from hata import Embed, Client, parse_emoji, elapsed_time, DATETIME_FORMAT_CODE, ZEROUSER,  GUILDS
from hata.ext.slash import abort

from bot_utils.constants import GUILD__SUPPORT

SLASH_CLIENT: Client

@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT)
async def emoji_info_preview(
    client,
    event,
    raw_emoji: ('str', 'The emoji, or it\'s name.', 'emoji'),
):
    """Shows details about the given emoji."""
    
    # Use goto
    while True:
        emoji = parse_emoji(raw_emoji)
        if (emoji is not None):
            break
        
        # Try resolve emoji from guild's.
        guild = event.guild
        if (guild is not None):
            emoji = guild.get_emoji_like(raw_emoji)
            if (emoji is not None):
                break
        
        abort('Could not resolve emoji')
        # Use return or the linter derps out
        return
    
    
    if emoji.is_unicode_emoji():
        embed = Embed(
            f'Unicode Emoji: {emoji.name}',
        ).add_field(
            'Internal identifier',
            (
                f'```\n'
                f'{emoji.id}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Unicode',
            (
                f'```\n'
                f'{emoji.unicode}\n'
                f'```'
            ),
            inline = True,
        )
    
    else:
        guild = emoji.guild
        
        # If the emoji's creator is unknown, try to request it.
        if (emoji.user is ZEROUSER) and (guild is not None) and (guild in client.guilds):
            await client.emoji_get(emoji)
        
        url = emoji.url
        
        embed = Embed(
            f'Custom emoji: {emoji.name}',
            url = url,
        ).add_image(
            url,
        ).add_field(
            'Identifier',
            (
                f'```\n'
                f'{emoji.id}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Animated',
            (
                f'```\n'
                f'{"true" if emoji.animated else "false"}\n'
                f'```'
            ),
            inline = True,
        )
        
        created_at = emoji.created_at
        
        embed.add_field(
            'Created at',
            (
                f'```\n'
                f'{created_at:{DATETIME_FORMAT_CODE}} | {elapsed_time(created_at)} ago\n'
                f'```'
            ),
        )
        
        user = emoji.user
        if user is ZEROUSER:
            creator_name = 'unknown'
        else:
            creator_name = f'{user.full_name}\n{user.id}'
        
        embed.add_field(
            'Creator',
            (
                f'```\n'
                f'{creator_name}\n'
                f'```'
            ),
            inline = True,
        )
        
        guild_id = emoji.guild_id
        if guild_id == 0:
            guild_name = 'unknown'
        
        else:
            guild = GUILDS.get(guild_id, None)
            if guild is None:
                guild_name = str(guild_id)
            
            else:
                guild_name = f'{guild.name}\n{guild_id}'
        
        embed.add_field(
            'Guild',
            (
                f'```\n'
                f'{guild_name}\n'
                f'```'
            ),
            inline = True,
        )
        
        roles = emoji.roles
        if roles is None:
            roles_description = 'N/A'
        
        else:
            roles_description_parts = []
            
            limit = len(roles)
            if limit > 10:
                truncated_count = limit - 10
                limit = 10
            else:
                truncated_count = 0
            
            index = 0
            while True:
                role = roles[index]
                roles_description_parts.append(role.name)
                
                index += 1
                if index == limit:
                    break
                
                roles_description_parts.append('\n')
                continue
            
            if truncated_count:
                roles_description_parts.append('\n\n... ')
                roles_description_parts.append(str(truncated_count))
                roles_description_parts.append(' truncated...')
            
            roles_description = ''.join(roles_description_parts)
            roles_description_parts = None
        
        
        embed.add_field(
            'Roles',
            (
                f'```\n'
                f'{roles_description}\n'
                f'```'
            ),
        )
        
        embed.add_field(
            'Available',
            (
                f'```\n'
                f'{"true" if emoji.available else "false"}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Managed',
            (
                f'```\n'
                f'{"true" if emoji.managed else "false"}\n'
                f'```'
            ),
            inline = True,
        )
    
    
    return embed
