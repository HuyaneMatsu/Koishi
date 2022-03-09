from hata import GUILDS, Embed, Client, DiscordException, StickerType, elapsed_time, BUILTIN_EMOJIS, ERROR_CODES, \
    DATETIME_FORMAT_CODE, StickerFormat, ZEROUSER, is_id
from hata.ext.slash import abort, InteractionResponse, Button


SLASH_CLIENT: Client

CLOSE_EMOJI = BUILTIN_EMOJIS['x']

CUSTOM_ID_STICKER_INFO_CLOSE = 'sticker_info.close'

BUTTON_STICKER_INFO_CLOSE = Button(
    emoji = CLOSE_EMOJI,
    custom_id = CUSTOM_ID_STICKER_INFO_CLOSE,
)


async def get_sticker(client, sticker, sticker_id):
    if (sticker is None):
        request_global = True
    else:
        guild = sticker.guild
        if guild is None:
            request_global = True
        else:
            if (guild in client.guilds):
                request_global = False
            else:
                request_global = True
    
    if request_global:
        coroutine = client.sticker_get(sticker_id, force_update=True)
    else:
        coroutine = client.sticker_guild_get(sticker, force_update=True)
    
    try:
        sticker = await coroutine
    except BaseException as err:
        if isinstance(err, ConnectionError):
            return
        
        if isinstance(err, DiscordException):
            if err.code == ERROR_CODES.unknown_sticker:
                abort(f'Unknown sticker: {sticker_id}')
        
        raise
    
    return sticker


def get_sticker_info(sticker):
    sticker_url = sticker.url_as(size=4096)
    embed = Embed(sticker.name, url=sticker_url)
    
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker_url)
    
    # Row 1 | id | animated
    embed.add_field(
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
        is_sticker_animated = True
    
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
    
    
    return InteractionResponse(embed=embed, components=BUTTON_STICKER_INFO_CLOSE)


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def sticker_(client, message):
    """Shows up the message's sticker."""
    sticker = message.sticker
    if sticker is None:
        abort('The message has no sticker.')
        
    sticker = await get_sticker(client, sticker, sticker.id)
    return get_sticker_info(sticker)


@SLASH_CLIENT.interactions(is_global=True)
async def sticker_info(
    client,
    event,
    sticker_name_or_id: ('str', 'Sticker to show', 'sticker'),
):
    if is_id(sticker_name_or_id):
        sticker = await get_sticker(client, None, sticker_name_or_id)
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
            
            abort(f'Cannot find sticker in local scope: {sticker_name_or_id}')
        
        sticker = await get_sticker(client, sticker, sticker.id)
    
    return get_sticker_info(sticker)


@sticker_info.autocomplete('sticker')
async def auto_complete_sticker_name(event, value):
    guild = event.guild
    if guild is None:
        return None
    
    if value is None:
       stickers = sorted(guild.stickers.values())
    else:
        stickers = guild.get_stickers_like(value)
    
    return [sticker.name for sticker in stickers]


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_STICKER_INFO_CLOSE)
async def close_emoji_info(client, event):
    if (event.user is event.message.interaction.user):
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)
