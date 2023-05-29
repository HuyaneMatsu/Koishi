__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, Emoji
from hata.ext.slash import Form, TextInput, TextInputStyle

from bots import SLASH_CLIENT

from .action_helpers import (
    check_emoji_guild, check_emoji_type, check_sticker_guild, check_sticker_type_modify, process_reason
)
from .cache_sticker import get_sticker
from .component_translate_tables import REMOVE_DISABLE
from .constants import (
    CUSTOM_ID_SNIPE_REMOVE_EMOJI, CUSTOM_ID_SNIPE_REMOVE_STICKER, EMOJI_REMOVE_FORM_PATTERN,
    ROW_SNIPE_ACTION_RESPONSE, STICKER_REMOVE_FORM_PATTERN, create_emoji_remove_form_custom_id,
    create_sticker_remove_form_custom_id
)
from .embed_builder_base import create_base_embed
from .embed_parsers import get_emoji_from_event, get_entity_id_from_event
from .helpers import (
    check_has_manage_guild_expressions_permission, discard_entity_from_components, propagate_check_error_message,
    translate_components
)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_REMOVE_EMOJI)
async def snipe_interaction_remove_emoji(client, event):
    """
    Pops up an emoji remove confirmation form.
    
    This function is a coroutine.
    
    Returns
    -------
    form : `None`, ``InteractionForm``
    """
    if not await check_has_manage_guild_expressions_permission(client, event):
        return
    
    emoji = get_emoji_from_event(event)
    if (emoji is None):
        return
    
    if not await check_emoji_type(client, event, emoji):
        return
    
    if not await check_emoji_guild(client, event, emoji):
        return
    
    return Form(
        f'Remove emoji: {emoji.name}',
        [
            TextInput(
                'Reason',
                min_length = 0,
                max_length = 400,
                custom_id = 'reason',
                placeholder = 'Justification',
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = create_emoji_remove_form_custom_id(emoji)
    )


@SLASH_CLIENT.interactions(custom_id = EMOJI_REMOVE_FORM_PATTERN, target = 'form')
async def snipe_confirm_remove_emoji(client, event, emoji_id, emoji_name, emoji_animated, *, reason):
    """
    Handles emoji remove confirmation.
    
    This function is coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    emoji_id : `str`
        The emoji's identifier. (Later converted to integer.)
    emoji_name : `str`
        The emoji's name.
    emoji_animated : `bool`
        Whether the emoji is animated. (Later converted to boolean.)
    reason : `None`, `str` (Keyword only)
        Justification.
    """
    await client.interaction_component_acknowledge(event, wait = False)
    emoji = Emoji._create_partial(int(emoji_id), emoji_name, True if emoji_animated == '1' else False)
    reason = process_reason(event, reason)
    
    try:
        await client.emoji_delete(emoji, reason = reason)
    except ConnectionError:
        return
    
    except DiscordException as err:
        error_code = err.code
        
        if error_code == ERROR_CODES.unknown_emoji:
            error_message = 'Emoji already deleted.'
        
        elif error_code == ERROR_CODES.missing_access:
            return
        
        elif error_code == ERROR_CODES.missing_permissions:
            # Discord can drop this even if the client was removed. How stupid!
            guild = event.guild
            if (guild is None) or (guild not in client.guilds):
                return
            
            error_message = 'Missing permissions.'
        
        elif error_code == ERROR_CODES.invalid_form_body:
            error_message = '\n'.join(err.errors)
        
        else:
            raise
        
        await propagate_check_error_message(client, event, error_message)
        return
    
    await client.interaction_followup_message_create(
        event,
        components = ROW_SNIPE_ACTION_RESPONSE,
        embed = create_base_embed(emoji, 'Emoji removed'),
        show_for_invoking_user_only = True,
    )
    
    await client.interaction_followup_message_edit(
        event,
        event.message,
        components = discard_entity_from_components(
            translate_components(event.message.iter_components(), REMOVE_DISABLE),
            emoji.id,
        ),
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_REMOVE_STICKER)
async def snipe_interaction_remove_sticker(client, event):
    """
    Pops up an sticker remove confirmation form.
    
    This function is a coroutine.
    
    Returns
    -------
    form : `None`, ``InteractionForm``
    """
    if not await check_has_manage_guild_expressions_permission(client, event):
        return
    
    sticker_id = get_entity_id_from_event(event)
    if not sticker_id:
        return
        
    sticker = await get_sticker(client, sticker_id)
    if sticker is None:
        return
    
    if not await check_sticker_type_modify(client, event, sticker):
        return
    
    if not await check_sticker_guild(client, event, sticker):
        return
    
    return Form(
        f'Remove sticker: {sticker.name}',
        [
            TextInput(
                'Reason',
                min_length = 0,
                max_length = 400,
                custom_id = 'reason',
                placeholder = 'Justification',
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = create_sticker_remove_form_custom_id(sticker)
    )


@SLASH_CLIENT.interactions(custom_id = STICKER_REMOVE_FORM_PATTERN, target = 'form')
async def snipe_confirm_remove_sticker(client, event, sticker_id, *, reason):
    """
    Handles sticker remove confirmation.
    
    This function is coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    sticker_id : `str`
        The sticker's identifier. (Later converted to integer.)
    reason : `None`, `str` (Keyword only)
        Justification.
    """
    await client.interaction_component_acknowledge(event, wait = False)
    sticker = await get_sticker(client, int(sticker_id))
    reason = process_reason(event, reason)
    
    try:
        await client.sticker_delete(sticker, reason = reason)
    except ConnectionError:
        return
    
    except DiscordException as err:
        error_code = err.code
        
        if error_code == ERROR_CODES.unknown_sticker:
            error_message = 'Sticker already deleted.'
        
        elif error_code == ERROR_CODES.missing_access:
            return
        
        elif error_code == ERROR_CODES.missing_permissions:
            # Discord can drop this even if the client was removed. How stupid!
            guild = event.guild
            if (guild is None) or (guild not in client.guilds):
                return
            
            error_message = 'Missing permissions.'
        
        elif error_code == ERROR_CODES.invalid_form_body:
            error_message = '\n'.join(err.errors)
        
        else:
            raise
        
        await propagate_check_error_message(client, event, error_message)
        return
    
    await client.interaction_followup_message_create(
        event,
        components = ROW_SNIPE_ACTION_RESPONSE,
        embed = create_base_embed(sticker, 'Sticker removed'),
        show_for_invoking_user_only = True,
    )
    
    await client.interaction_followup_message_edit(
        event,
        event.message,
        components = discard_entity_from_components(
            translate_components(event.message.iter_components(), REMOVE_DISABLE),
            sticker.id,
        ),
    )
