__all__ = ()

from hata import Embed, ZEROUSER, DiscordException, ERROR_CODES, DATETIME_FORMAT_CODE, elapsed_time, GUILDS
from hata.ext.slash import InteractionResponse, Row

from .constants import BUTTON_SNIPE_CLOSE, BUTTON_SNIPE_DM


async def get_emoji_info(event, emoji):
    if emoji.is_unicode_emoji():
        embed = Embed(
            f'Emoji details',
        ).add_field(
            'Name',
            (
                f'```\n'
                f'{emoji.name}\n'
                f'```'
            ),
            inline = True,
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
        url = emoji.url
        
        embed = Embed(
            f'Emoji details',
            url = url,
        ).add_image(
            url,
        ).add_field(
            'Name',
            (
                f'```\n'
                f'{emoji.name}\n'
                f'```'
            ),
            inline = True,
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
    
    if event.guild_id:
        components = Row(BUTTON_SNIPE_CLOSE, BUTTON_SNIPE_DM)
    else:
        components = Row(BUTTON_SNIPE_CLOSE)
    
    return InteractionResponse(
        embed = embed,
        components = components
    )
