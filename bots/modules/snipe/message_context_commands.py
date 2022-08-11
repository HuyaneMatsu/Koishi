__all__ = ()

import re

from hata import Client, DiscordException, ERROR_CODES, Embed, parse_custom_emojis_ordered
from hata.ext.slash import abort

from .constants import (
    BUTTON_SNIPE_EMOJI_INFO, BUTTON_SNIPE_STICKER_INFO, CUSTOM_ID_SNIPE_EMOJIS, CUSTOM_ID_SNIPE_REACTIONS,
    CUSTOM_ID_SNIPE_STICKERS
)
from .lister_helpers import (
    TYPE_NAME_BY_BUILDER, add_embed_author, create_initial_response, create_initial_response_parts,
    create_select_response, embed_builder_emoji, embed_builder_reaction, embed_builder_sticker, option_builder_emoji,
    option_builder_sticker, select_option_parser_emoji, select_option_parser_sticker
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
    
    
    await _respond_with_emojis(client, event, target, emojis, embed_builder_emoji, CUSTOM_ID_SNIPE_EMOJIS)



@SLASH_CLIENT.interactions(is_global=True, target='message')
async def snipe_reactions(client, event, target):
    reactions = target.reactions
    if (reactions is None) or (not reactions):
        abort('The message has no reactions.')
    
    emojis = [*reactions.keys()]
    
    await _respond_with_emojis(client, event, target, emojis, embed_builder_reaction, CUSTOM_ID_SNIPE_REACTIONS)


async def _respond_with_emojis(client, event, target, emojis, embed_builder, custom_id):
    await client.interaction_application_command_acknowledge(event, wait=False)
    
    while True:
        embed, components = create_initial_response_parts(
            event, target, emojis, embed_builder, option_builder_emoji, custom_id, BUTTON_SNIPE_EMOJI_INFO
        )
        
        try:
            await client.interaction_response_message_edit(event, embed=embed, components=components)
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
            
            if (not emoji_indexes_to_remove) or (len(errors) != emoji_indexes_to_remove):
                raise

        else:
            break
        
        emoji_indexes_to_remove.sort(reverse = True)
        
        for index in emoji_indexes_to_remove:
            del emojis[index]
        
        if not emojis:
            type_name = TYPE_NAME_BY_BUILDER[embed_builder]
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
