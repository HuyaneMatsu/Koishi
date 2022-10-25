__all__ = ()

import re

from hata import Client, DiscordException, ERROR_CODES, Embed, parse_custom_emojis_ordered
from hata.ext.slash import abort

from .constants import (
    CUSTOM_ID_SNIPE_SELECT_EMOJI, CUSTOM_ID_SNIPE_SELECT_REACTION, CUSTOM_ID_SNIPE_SELECT_STICKER, NAME_BY_SNIPE_TYPE,
    SNIPE_TYPE_EMOJI, SNIPE_TYPE_REACTION, SNIPE_TYPE_STICKER
)
from .lister_helpers import (
    add_embed_author, create_initial_response, create_initial_response_parts, create_select_response,
    embed_builder_emoji, embed_builder_reaction, embed_builder_sticker, select_option_parser_emoji,
    select_option_parser_sticker
)


DELETED_EMOJI_RP = re.compile(
    '(?:data\.)?components\[\d+\]\.components\[\d+\]\.options\[(\d+)\]\.emoji\.id\.BUTTON_COMPONENT_INVALID_EMOJI.*'
)


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def snipe_emojis(client, event, target):
    emojis = parse_custom_emojis_ordered(target.content)
    if not emojis:
        abort('The message has no emojis.')
    
    
    await _respond_with_emojis(client, event, target, emojis, SNIPE_TYPE_EMOJI)



@SLASH_CLIENT.interactions(is_global=True, target='message')
async def snipe_reactions(client, event, target):
    reactions = target.reactions
    if (reactions is None) or (not reactions):
        abort('The message has no reactions.')
    
    emojis = [*reactions.keys()]
    
    await _respond_with_emojis(client, event, target, emojis, SNIPE_TYPE_REACTION)


async def _respond_with_emojis(client, event, target, emojis, snipe_type):
    await client.interaction_application_command_acknowledge(event, wait = False)
    
    while True:
        embed, components = create_initial_response_parts(event, target, emojis, snipe_type)
        
        try:
            await client.interaction_response_message_edit(event, embed = embed, components = components)
        except DiscordException as err:
            if err.code != ERROR_CODES.invalid_form_body:
                raise
            
            errors = err.errors
            
            emoji_indexes_to_remove = []
            
            for error in errors:
                matched = DELETED_EMOJI_RP.fullmatch(error)
                if matched is None:
                    break
                
                emoji_indexes_to_remove.append(int(matched.group(1)))
                continue
            
            if (not emoji_indexes_to_remove) or (len(errors) != len(emoji_indexes_to_remove)):
                raise

        else:
            break
        
        emoji_indexes_to_remove.sort(reverse = True)
        
        for index in emoji_indexes_to_remove:
            del emojis[index]
        
        if not emojis:
            type_name = NAME_BY_SNIPE_TYPE[snipe_type]
            embed = Embed(None, f'*No alive {type_name}s where sniped.*')
            add_embed_author(embed, event, target.url, type_name)
            
            await client.interaction_response_message_edit(event, embed=embed)
            
            return


@SLASH_CLIENT.interactions(is_global=True, target='message')
async def snipe_stickers(event, target):
    stickers = target.stickers
    if (stickers is None):
        abort('The message has no stickers.')
    
    stickers = [*stickers]
    
    return create_initial_response(event, target, stickers, SNIPE_TYPE_STICKER)



@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_SELECT_EMOJI)
async def select_emoji(client, event):
    return await create_select_response(client, event, select_option_parser_emoji, embed_builder_emoji)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_SELECT_REACTION)
async def select_reaction(client, event):
    return await create_select_response(client, event, select_option_parser_emoji, embed_builder_reaction)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_SELECT_STICKER)
async def select_stickers(client, event):
    return await create_select_response(client, event, select_option_parser_sticker, embed_builder_sticker)
