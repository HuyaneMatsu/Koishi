__all__ = ()

from hata import Embed, parse_emoji
from hata.ext.slash import Select, Option, InteractionResponse, Row

from .constants import BUTTON_SNIPE_DM
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
        url = None
    
    else:
        title =  'Click to open'
        url = entity_url
    
    embed = Embed(
        title,
        color = (entity.id >> 22) & 0xffffff,
        url = url,
    ).add_field(
        'Name',
        f'```\n{entity.name}\n```',
        inline = True,
    ).add_field(
        'ID',
        f'```\n{entity.id}\n```',
        inline = True,
    )
    
    
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
    
    
    if entity_url is not None:
        embed.add_image(entity_url)
    
    
    user = event.user
    embed.add_author(
        f'{user.name_at(event.guild_id)}\'s sniped {type_name}s!',
        user.avatar_url,
        message_url,
    )
    
    return embed


def create_initial_response(event, target, entities, embed_builder, option_builder, custom_id, button_info):
    if target is None:
        target_url = None
    else:
        target_url = target.url
    
    embed = embed_builder(event, entities[0], target_url)
    
    
    if len(entities) == 1:
        components = Row(
            button_info,
            BUTTON_SNIPE_DM,
        )
    
    else:
        del entities[25:]
        
        components = [
            Select(
                [option_builder(entity) for entity in entities],
                custom_id = custom_id,
                placeholder = 'Select an emoji!',
            ),
            Row(
                BUTTON_SNIPE_DM,
                button_info,
            )
        ]
    
    return InteractionResponse(embed=embed, components=components)


async def select_option_parser_emoji(client, event):
    selected_emojis = event.interaction.options
    if (selected_emojis is None):
        return None
    
    selected_emoji = selected_emojis[0]
    return parse_emoji(selected_emoji)


async def select_option_parser_sticker(client, event):
    selected_stickers = event.interaction.options
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
