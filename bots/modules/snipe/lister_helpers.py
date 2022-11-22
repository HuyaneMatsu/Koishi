__all__ = ()

from hata import Embed, parse_emoji
from hata.ext.slash import InteractionResponse, Option, Row, Select

from .constants import (
    BUTTON_SNIPE_ADD_DISABLED, BUTTON_SNIPE_ADD_EMOJI, BUTTON_SNIPE_ADD_STICKER, BUTTON_SNIPE_CLOSE, BUTTON_SNIPE_DM,
    BUTTON_SNIPE_INFO_EMOJI, BUTTON_SNIPE_INFO_STICKER, CUSTOM_ID_SNIPE_SELECT_EMOJI, CUSTOM_ID_SNIPE_SELECT_STICKER,
    SNIPE_TYPE_EMOJI, SNIPE_TYPE_STICKER
)
from .sticker_helpers import get_sticker


def embed_builder_emoji(event, emoji, message_url):
    return build_embed(event, emoji, message_url, 'emoji')

def embed_builder_reaction(event, emoji, message_url):
    return build_embed(event, emoji, message_url, 'reaction')
    
def embed_builder_sticker(event, sticker, message_url):
    return build_embed(event, sticker, message_url, 'sticker')


def option_builder_emoji(emoji):
    return Option(emoji.as_emoji, emoji.name, emoji)


def option_builder_sticker(sticker):
    return Option(sticker.id, sticker.name)


def build_embed(event, entity, message_url, type_name):
    entity_url = entity.url
    if entity_url is None:
        title = None
    
    else:
        title = 'Click to open'
    
    embed = create_base_embed(entity, title)
    
    guild = entity.guild
    if (guild is None):
        footer_text = 'Unknown guild'
        footer_icon_url = None
    else:
        footer_text = f'from {guild.name}'
        footer_icon_url = guild.icon_url
    
    embed.add_footer(
        footer_text,
        footer_icon_url,
    )
    
    add_embed_author(embed, event, type_name, message_url)
    
    return embed


def create_base_embed(entity, title):
    if entity is None:
        entity_url = None
    else:
        entity_url = entity.url
    
    embed = Embed(
        title,
        color = (entity.id >> 22) & 0xffffff,
        url = entity_url,
    ).add_field(
        'Name',
        f'```\n{entity.name}\n```',
        inline = True,
    ).add_field(
        'ID',
        f'```\n{entity.id}\n```',
        inline = True,
    )
    
    if entity_url is not None:
        embed.add_image(entity_url)
    
    return embed


def add_embed_author(embed, event, type_name, message_url):
    user = event.user
    
    embed.add_author(
        f'{user.name_at(event.guild_id)}\'s sniped {type_name}s!',
        user.avatar_url,
        message_url,
    )


def create_initial_response(event, target, entities, snipe_type):
    embed, components = create_initial_response_parts(event, target, entities, snipe_type)
    return InteractionResponse(embed = embed, components = components)


def create_initial_response_parts(event, target, entities, snipe_type):
    if target is None:
        target_url = None
    else:
        target_url = target.url
    
    
    if snipe_type == SNIPE_TYPE_STICKER:
        button_info = BUTTON_SNIPE_INFO_STICKER
        button_add = BUTTON_SNIPE_ADD_STICKER
        option_builder = option_builder_sticker
        select_custom_id = CUSTOM_ID_SNIPE_SELECT_STICKER
        embed_builder = embed_builder_sticker
    
    else:
        button_info = BUTTON_SNIPE_INFO_EMOJI
        button_add = BUTTON_SNIPE_ADD_EMOJI
        option_builder = option_builder_emoji
        
        if snipe_type == SNIPE_TYPE_EMOJI:
            select_custom_id = CUSTOM_ID_SNIPE_SELECT_EMOJI
            embed_builder = embed_builder_emoji
        
        else:
            select_custom_id = CUSTOM_ID_SNIPE_SELECT_STICKER
            embed_builder = embed_builder_sticker
    
    entity = entities[0]
    embed = embed_builder(event, entity, target_url)
    
    
    if event.guild_id == entity.guild_id:
        button_add = BUTTON_SNIPE_ADD_DISABLED
    
    
    if len(entities) == 1:
        components = Row(
            button_info,
            BUTTON_SNIPE_DM,
            button_add,
            BUTTON_SNIPE_CLOSE,
        )
    
    else:
        del entities[25:]
        
        components = [
            Select(
                [option_builder(entity) for entity in entities],
                custom_id = select_custom_id,
                placeholder = 'Select an emoji!',
            ),
            Row(
                button_info,
                BUTTON_SNIPE_DM,
                button_add,
                BUTTON_SNIPE_CLOSE,
            )
        ]
    
    return embed, components


async def select_option_parser_emoji(client, event):
    selected_emojis = event.values
    if (selected_emojis is None):
        return None
    
    selected_emoji = selected_emojis[0]
    return parse_emoji(selected_emoji)


async def select_option_parser_sticker(client, event):
    selected_stickers = event.values
    if (selected_stickers is None):
        return None
    
    selected_sticker = selected_stickers[0]
    try:
        selected_sticker_id = int(selected_sticker)
    except ValueError:
        return None
    
    return await get_sticker(client, selected_sticker_id)


async def create_select_response(client, event, select_option_parser, embed_builder):
    # Check permission
    if event.user is not event.message.interaction.user:
        return
    
    entity = await select_option_parser(client, event)
    if entity is None:
        return
    
    # get message.url
    embed = event.message.embed
    if embed is None:
        message_url = None
    else:
        embed_author = embed.author
        if embed_author is None:
            message_url = None
        else:
            message_url = embed_author.url
    
    return embed_builder(event, entity, message_url)
