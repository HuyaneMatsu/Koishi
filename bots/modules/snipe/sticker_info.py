__all__ = ()

from hata import StickerFormat, Embed, DATETIME_FORMAT_CODE, elapsed_time, StickerType, ZEROUSER, GUILDS


def get_sticker_info(event, sticker):
    sticker_url = sticker.url_as(size=4096)
    embed = Embed('Sticker details',url=sticker_url)
    
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker_url)
    
    # Row 1 | name | id | animated
    embed.add_field(
        'Name',
        (
            f'```\n'
            f'{sticker.name}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Identifier',
        (
            f'```\n'
            f'{sticker.id}\n'
            f'```'
        ),
        inline = True,
    )
    
    if sticker_format is StickerFormat.apng:
        is_sticker_animated = True
    elif sticker_format is StickerFormat.lottie:
        is_sticker_animated = True
    else:
        is_sticker_animated = False
    
    embed.add_field(
        'Animated',
        (
            f'```\n'
            f'{"true" if is_sticker_animated else "false"}\n'
            f'```'
        ),
        inline = True,
    )
    
    # Row 2 | created_at
    
    created_at = sticker.created_at
    
    embed.add_field(
        'Created at',
        (
            f'```\n'
            f'{created_at:{DATETIME_FORMAT_CODE}} | {elapsed_time(created_at)} ago\n'
            f'```'
        ),
    )
    
    
    # Row 3 | description
    
    description = sticker.description
    if description is None:
        description = 'N / A'
    
    embed.add_field(
        'Description',
        (
            f'```\n'
            f'{description}\n'
            f'```'
        ),
    )
    
    # Row 4 | type | format
    
    sticker_type = sticker.type
    
    embed.add_field(
        'Type',
        (
            f'```\n'
            f'{sticker_type.name}\n'
            f'```'
        ),
        inline = True,
    ).add_field(
        'Format',
        (
            f'```\n'
            f'{sticker_format.name}\n'
            f'```'
        ),
        inline = True,
    )
    
    # Row 5 | tags
    
    tags = sticker.tags
    if tags is None:
        tags_listed = 'N / A'
    
    else:
        tags_listed = ', '.join(sorted(tags))
    
    embed.add_field(
        'Tags',
        (
            f'```\n'
            f'{tags_listed}\n'
            f'```'
        ),
    )
    
    if sticker_type is StickerType.standard:
        
        # Row 6 | pack id | sort value
        
        embed.add_field(
            'Pack id',
            (
                f'```\n'
                f'{sticker.pack_id}\n'
                f'```'
            ),
            inline = True,
        ).add_field(
            'Sort value',
            (
                f'```\n'
                f'{sticker.sort_value}\n'
                f'```'
            ),
            inline = True,
        )
    
    elif sticker_type is StickerType.guild:
        
        # Row 6 | creator | guild
        
        user = sticker.user
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
        
        
        guild_id = sticker.guild_id
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
    
    return embed
