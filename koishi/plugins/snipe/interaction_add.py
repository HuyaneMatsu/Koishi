__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, Emoji, InteractionForm, TextInputStyle, create_text_input

from ...bots import FEATURE_CLIENTS

from .action_helpers import (
    check_emoji_counts, check_emoji_type, check_is_emoji_name_valid, check_sticker_counts, check_sticker_type_create,
    join_sticker_tags, parse_and_join_tags, parse_roles
)
from .cache_sticker import get_sticker
from .component_translate_tables import ADD_DISABLE
from .constants import (
    CUSTOM_ID_SNIPE_ADD_EMOJI, CUSTOM_ID_SNIPE_ADD_STICKER, EMOJI_ADD_FORM_PATTERN, ROW_SNIPE_ACTION_RESPONSE,
    STICKER_ADD_FORM_PATTERN, create_emoji_add_form_custom_id, create_sticker_add_form_custom_id
)
from .embed_builder_base import create_base_embed
from .embed_parsers import get_emoji_from_event, get_entity_id_from_event
from .helpers import (
    check_has_create_guild_expressions_permission, propagate_check_error_message, translate_components
)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_ADD_EMOJI)
async def snipe_interaction_add_emoji(client, event):
    """
    Pops up an emoji add confirmation form.
    
    This function is a coroutine.
    
    Returns
    -------
    form : `None`, ``InteractionForm``
    """
    if not await check_has_create_guild_expressions_permission(client, event):
        return
    
    emoji = get_emoji_from_event(event)
    if (emoji is None):
        return
    
    if not await check_emoji_type(client, event, emoji):
        return
    
    if not await check_emoji_counts(client, event, emoji):
        return
    
    return InteractionForm(
        f'Add emoji: {emoji.name}',
        [
            create_text_input(
                'Name',
                min_length = 2,
                max_length = 32,
                custom_id = 'name',
                placeholder = 'Emoji name',
                value = emoji.name,
            ),
            create_text_input(
                'Roles (separate with comma)',
                min_length = 0,
                max_length = 1024,
                custom_id = 'roles',
                placeholder = 'Limits the emoji\'s usage only to users with any of the specified roles.',
                value = '',
            ),
        ],
        custom_id = create_emoji_add_form_custom_id(emoji)
    )


@FEATURE_CLIENTS.interactions(custom_id = EMOJI_ADD_FORM_PATTERN, target = 'form')
async def snipe_confirm_add_emoji(client, event, emoji_id, emoji_name, emoji_animated, *, name, roles):
    """
    Handles emoji add confirmation.
    
    This function is a coroutine.
    
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
    name : `None`, `str` (Keyword only)
        The name of the emoji.
    roles : `None`, `str` (Keyword only)
        The roles to limit the emoji's usage to. (Later converted to list of roles.)
    """
    if not await check_is_emoji_name_valid(client, event, name):
        return
    
    if (roles is not None):
        roles = parse_roles(roles, event.guild)
    
    await client.interaction_component_acknowledge(event, wait = False)
    
    emoji = Emoji._create_partial(int(emoji_id), emoji_name, True if emoji_animated == '1' else False)
    
    if name is None:
        name = emoji.name
    
    async with client.http.get(emoji.url) as response:
        data = await response.read()
    
    try:
        new_emoji = await client.emoji_create(event.guild_id, name = name, image = data, roles = roles)
    except ConnectionError:
        return
    
    except DiscordException as err:
        error_code = err.code
        
        if error_code == ERROR_CODES.missing_access:
            return
        
        elif error_code == ERROR_CODES.missing_permissions:
            # Discord can drop this even if the client was removed. How stupid!
            guild = event.guild
            if (guild is None) or (guild not in client.guilds):
                return
            
            error_message = 'Missing permissions.'
        
        elif error_code == ERROR_CODES.invalid_form_body:
            error_message = '\n'.join(err.errors)
        
        elif error_code == ERROR_CODES.failed_to_resize_asset_below_max_size:
            error_message = 'Failed to resize emoji below max size.'
        
        elif error_code == ERROR_CODES.max_emojis:
            error_message = 'Emoji limit hit.'
        
        elif error_code == ERROR_CODES.cannot_mix_subscription_and_non_subscription_roles_for_an_emoji:
            error_message = 'Cannot mix subscription and non-subscription roles for an emoji.'
        
        else:
            raise
        
        await propagate_check_error_message(client, event, error_message)
        return
    
    await client.interaction_followup_message_create(
        event,
        components = ROW_SNIPE_ACTION_RESPONSE,
        embed = create_base_embed(new_emoji, 'Emoji added'),
        show_for_invoking_user_only = True,
    )
    
    await client.interaction_followup_message_edit(
        event,
        event.message,
        components = translate_components(event.message.iter_components(), ADD_DISABLE),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_ADD_STICKER)
async def snipe_interaction_add_sticker(client, event):
    """
    Pops up a sticker add confirmation form.
    
    This function is a coroutine.
    
    Returns
    -------
    form : `None`, ``InteractionForm``
    """
    if not await check_has_create_guild_expressions_permission(client, event):
        return
    
    sticker_id = get_entity_id_from_event(event)
    if not sticker_id:
        return
        
    sticker = await get_sticker(client, sticker_id)
    if sticker is None:
        return
    
    if not await check_sticker_type_create(client, event, sticker):
        return
    
    if not await check_sticker_counts(client, event):
        return
    
    return InteractionForm(
        f'Add sticker: {sticker.name}',
        [
            create_text_input(
                'Name',
                min_length = 2,
                max_length = 32,
                custom_id = 'name',
                placeholder = 'Sticker name',
                value = sticker.name,
            ),
            create_text_input(
                'Tags',
                min_length = 0,
                max_length = 100,
                custom_id = 'tags',
                placeholder = 'Sticker tags',
                value = join_sticker_tags(sticker),
            ),
            create_text_input(
                'Description',
                min_length = 0,
                max_length = 1024,
                custom_id = 'description',
                placeholder = 'Sticker description',
                value = sticker.description,
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = create_sticker_add_form_custom_id(sticker)
    )


@FEATURE_CLIENTS.interactions(custom_id = STICKER_ADD_FORM_PATTERN, target = 'form')
async def snipe_confirm_add_sticker(client, event, sticker_id, *, name, tags, description):
    """
    handles sticker add confirmation.
    
    This function is coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    sticker_id : `str`
        The sticker's identifier. (Later converted to integer.)
    name : `None`, `str` (Keyword only)
        The name of the sticker.
    tags : `None`, `str` (Keyword only)
        The tags of the sticker.
    description : `None`, `str` (Keyword only)
        The description of the sticker.
    """
    await client.interaction_component_acknowledge(event, wait = False)
    
    sticker = await get_sticker(client, int(sticker_id))
    
    if name is None:
        name = sticker.name
    
    if tags is None:
        tags = join_sticker_tags(sticker)
    else:
        tags = parse_and_join_tags(tags)
    
    async with client.http.get(sticker.url) as response:
        data = await response.read()
    
    try:
        new_sticker = await client.sticker_create(
            event.guild_id,
            name = name,
            image = data,
            tags = tags,
            description = description,
        )
    except ConnectionError:
        return
    
    except DiscordException as err:
        error_code = err.code
        
        if error_code == ERROR_CODES.missing_access:
            return
        
        elif error_code == ERROR_CODES.missing_permissions:
            # Discord can drop this even if the client was removed. How stupid!
            guild = event.guild
            if (guild is None) or (guild not in client.guilds):
                return
            
            error_message = 'Missing permissions.'
        
        elif error_code == ERROR_CODES.invalid_form_body:
            error_message = '\n'.join(err.errors)
        
        elif error_code == ERROR_CODES.failed_to_resize_asset_below_max_size:
            error_message = 'Failed to resize sticker below max size.'
        
        elif error_code == ERROR_CODES.max_stickers:
            error_message = 'Sticker limit hit.'
        
        else:
            raise
        
        await propagate_check_error_message(client, event, error_message)
        return
    
    await client.interaction_followup_message_create(
        event,
        components = ROW_SNIPE_ACTION_RESPONSE,
        embed = create_base_embed(new_sticker, 'Sticker added'),
        show_for_invoking_user_only = True,
    )
    
    await client.interaction_followup_message_edit(
        event,
        event.message,
        components = translate_components(event.message.iter_components(), ADD_DISABLE),
    )
