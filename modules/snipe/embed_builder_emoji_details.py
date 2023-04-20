__all__ = ()

from hata import DATETIME_FORMAT_CODE, Embed, GUILDS, ZEROUSER, elapsed_time

from .embed_builder_base import create_base_embed


def build_emoji_details(emoji, type_name):
    """
    Creates a detailed emoji embed.
    
    Parameters
    ----------
    sticker : ``Emoji``
        The emoji to create the embed for.
    type_name : `str`
        The name to call the emoji (capitalised).
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = create_base_embed(emoji, f'{type_name} details')
    
    if emoji.is_unicode_emoji():
        embed.add_field(
            'Unicode',
            (
                f'```\n'
                f'{emoji.unicode}\n'
                f'```'
            ),
            inline = True,
        )
    
    else:
        embed.add_field(
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
