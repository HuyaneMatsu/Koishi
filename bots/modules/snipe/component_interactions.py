__all__ = ()

import re

from hata import Client, ComponentType, DiscordException, ERROR_CODES, EMOJIS, Emoji, ZEROUSER

from .constants import CUSTOM_ID_SNIPE_DM, CUSTOM_ID_SNIPE_EMOJI_INFO, CUSTOM_ID_SNIPE_STICKER_INFO
from .emoji_info import get_emoji_info
from .sticker_helpers import get_sticker
from .sticker_info import get_sticker_info


MATCH_ID_IN_FIELD_VALUE = re.compile('[0-9]+')
MATCH_NAME_IN_FIELD_VALUE = re.compile('[0-9a-zA-Z_\-]+')

SLASH_CLIENT : Client


def without_dm_button(component):
    if component.type is ComponentType.row:
        return [*iter_without_dm_button(component)]
    
    return without_dm_button


def iter_without_dm_button(row):
    for component in row:
        if component.custom_id != CUSTOM_ID_SNIPE_DM:
            yield component


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_SNIPE_DM)
async def snipe_message_dm(client, event):
    await client.interaction_component_acknowledge(event, wait=False)
    
    message = event.message
    if message is None:
        return
    
    embed = message.embed
    if embed is None:
        # Rare Discord bug where not every message field is resolved correctly. :derp:
        # I dont even know what is going on.
        try:
            await client.message_get(message, force_update=True)
        except DiscordException as err:
            if err.code == ERROR_CODES.unknown_message: # Message deleted
                return
            
            raise
        
        embed = message.embed
        if embed is None:
            return
    
    components = message.components
    if (components is not None):
        components = [without_dm_button(component) for component in components]
    
    
    channel = await client.channel_private_create(event.user)
    
    try:
        await client.message_create(channel, embed=embed, components=components)
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user: # user has dm-s disabled:
            await client.interaction_followup_message_create(
                event, 'Could not deliver direct message.', show_for_invoking_user_only=True
            )
        
        else:
            raise

@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_SNIPE_EMOJI_INFO)
async def show_emoji_info(client, event):
    await client.interaction_component_acknowledge(event, wait=False)
    
    message = event.message
    if message is None:
        return
    
    embed = message.embed
    if embed is None:
        return
    
    fields = embed.fields
    if (fields is None) or len(fields) < 2:
        return
    
    field = fields[1]
    match = MATCH_ID_IN_FIELD_VALUE.search(field.value)
    if match is None:
        return
    
    emoji_id = int(match.group(0))
    
    emoji = EMOJIS.get(emoji_id, None)
    if emoji is None:
        
        url = embed.url
        if url is None:
            animated = False
        else:
            animated = url.endswith('.gif')
        
        field = fields[0]
        match = MATCH_NAME_IN_FIELD_VALUE.search(field.value)
        if match is None:
            name = ''
        else:
            name = match.group(0)
            
        emoji = Emoji._create_partial(int(emoji_id), name, animated)
    
    guild = emoji.guild
    if emoji.is_custom_emoji():
        if (emoji.user is ZEROUSER) and (guild is not None) and (guild in client.guilds) and (not emoji.managed):
            try:
                await client.emoji_get(emoji, force_update=True)
            except DiscordException as err:
                if err.code not in (
                    ERROR_CODES.missing_access, # Client removed.
                ):
                    raise
    
    response_embed = get_emoji_info(emoji)
    response_embed.author = embed.author
    response_embed.footer = embed.footer
    
    await client.interaction_followup_message_create(
        event,
        embed = response_embed,
        show_for_invoking_user_only = bool(event.guild_id),
    )


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_SNIPE_STICKER_INFO)
async def show_sticker_info(client, event):
    await client.interaction_component_acknowledge(event, wait=False)
    
    message = event.message
    if message is None:
        return
    
    embed = message.embed
    if embed is None:
        return
    
    fields = embed.fields
    if (fields is None) or len(fields) < 2:
        return
    
    field = fields[1]
    match = MATCH_ID_IN_FIELD_VALUE.search(field.value)
    if match is None:
        return
    
    sticker_id = int(match.group(0))
    
    sticker = await get_sticker(client, sticker_id)
    if sticker is None:
        return
    
    response_embed = get_sticker_info(event, sticker)
    response_embed.author = embed.author
    response_embed.footer = embed.footer
    
    await client.interaction_followup_message_create(
        event,
        embed = response_embed,
        show_for_invoking_user_only = bool(event.guild_id),
    )
