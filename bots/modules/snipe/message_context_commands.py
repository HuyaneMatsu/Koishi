__all__ = ()

from hata import Client, parse_custom_emojis_ordered
from hata.ext.slash import abort

SLASH_CLIENT: Client

from .constants import CUSTOM_ID_SNIPE_EMOJIS, CUSTOM_ID_SNIPE_REACTIONS, CUSTOM_ID_SNIPE_STICKERS, \
    BUTTON_SNIPE_EMOJI_INFO, BUTTON_SNIPE_STICKER_INFO
from .lister_helpers import create_initial_response, embed_builder_emoji, select_option_parser_emoji, \
    select_option_parser_sticker, option_builder_emoji, embed_builder_reaction, embed_builder_sticker, \
    option_builder_sticker, create_select_response


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def snipe_emojis(event, target):
    emojis = parse_custom_emojis_ordered(target.content)
    if not emojis:
        abort('The message has no emojis.')
    
    
    return create_initial_response(
        event, target, emojis, embed_builder_emoji, option_builder_emoji, CUSTOM_ID_SNIPE_EMOJIS,
        BUTTON_SNIPE_EMOJI_INFO
    )
    


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def snipe_reactions(event, target):
    reactions = target.reactions
    if (reactions is None) or (not reactions):
        abort('The message has no reactions.')
    
    emojis = [*reactions.keys()]
    
    return create_initial_response(
        event, target, emojis, embed_builder_reaction, option_builder_emoji, CUSTOM_ID_SNIPE_REACTIONS,
        BUTTON_SNIPE_EMOJI_INFO
    )


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def snipe_stickers(event, target):
    stickers = target.stickers
    if (stickers is None):
        abort('The message has no stickers.')
    
    stickers = [*stickers]
    
    return create_initial_response(
        event, target, stickers, embed_builder_sticker, option_builder_sticker, CUSTOM_ID_SNIPE_STICKERS,
        BUTTON_SNIPE_STICKER_INFO
    )



@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_SNIPE_EMOJIS)
async def select_emoji(client, event):
    return await create_select_response(client, event, select_option_parser_emoji, embed_builder_emoji)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_SNIPE_REACTIONS)
async def select_reaction(client, event):
    return await create_select_response(client, event, select_option_parser_emoji, embed_builder_reaction)


@SLASH_CLIENT.interactions(custom_id=CUSTOM_ID_SNIPE_STICKERS)
async def select_stickers(client, event):
    return await create_select_response(client, event, select_option_parser_sticker, embed_builder_sticker)
