__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, Emoji
from hata.ext.slash import Form, TextInput, TextInputStyle

from .action_helpers import (
    check_emoji_type, check_is_emoji_name_valid, check_sticker_type_modify, join_roles, join_sticker_tags,
    parse_and_join_tags, parse_roles
)
from .cache_sticker import get_sticker
from .constants import (
    CUSTOM_ID_SNIPE_EDIT_EMOJI, CUSTOM_ID_SNIPE_EDIT_STICKER, EMOJI_EDIT_FORM_PATTERN, ROW_SNIPE_ACTION_RESPONSE,
    STICKER_EDIT_FORM_PATTERN, create_emoji_edit_form_custom_id, create_sticker_edit_form_custom_id
)
from .embed_builder_base import create_base_embed
from .embed_parsers import get_emoji_from_event, get_entity_id_from_event
from .helpers import check_has_manage_emojis_and_stickers_permission, propagate_check_error_message


SLASH_CLIENT : Client


def add_change_field(embed, field_name, old_value, new_value):
    """
    Adds  change field to the given embed.
    
    Parameters
    ----------
    embed : ``Embed``
        The embed to extend.
    field_name : `str`
        The fields name.
    old_value : `str`
        The field's old value.
    new_value : `str`
        The field's new value.
    """
    if old_value == new_value:
        return
    
    # Do not allow backtick (or grave character)
    old_value = old_value.replace('`', '')
    new_value = new_value.replace('`', '')
    
    # Set length limit.
    if len(old_value) > 500:
        old_value = old_value[:500] + ' ...'
    
    if len(new_value) > 500:
        new_value = new_value[:500] + ' ...'
    
    embed.add_field(
        f'{field_name} change',
        (
            f'```\n'
            f'{old_value} -> {new_value}\n'
            f'```'
        )
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_EDIT_EMOJI)
async def snipe_interaction_edit_emoji(client, event):
    """
    Pops up an emoji edit form.
    
    This function is a coroutine.
    
    Returns
    -------
    form : `None`, ``InteractionForm``
    """
    if not await check_has_manage_emojis_and_stickers_permission(client, event):
        return
    
    emoji = get_emoji_from_event(event)
    if (emoji is None):
        return
    
    if not await check_emoji_type(client, event, emoji):
        return
    
    return Form(
        f'Edit emoji: {emoji.name}',
        [
            TextInput(
                'Name',
                min_length = 2,
                max_length = 32,
                custom_id = 'name',
                placeholder = 'Emoji name',
                value = emoji.name,
            ),
            TextInput(
                'Roles (separate with comma)',
                min_length = 0,
                max_length = 1024,
                custom_id = 'roles',
                placeholder = 'Limits the emoji\'s usage only to users with any of the specified roles.',
                value = join_roles(emoji.roles),
            ),
        ],
        custom_id = create_emoji_edit_form_custom_id(emoji)
    )


@SLASH_CLIENT.interactions(custom_id = EMOJI_EDIT_FORM_PATTERN, target = 'form')
async def snipe_confirm_edit_emoji(client, event, emoji_id, emoji_name, emoji_animated, *, name, roles):
    """
    Handles emoji edit confirmation.
    
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
    name : `None`, `str` (Keyword only)
        The new name of the emoji.
    roles : `None`, `str` (Keyword only)
        The roles to limit the emoji's usage to. (Later converted to list of roles.)
    """
    if not await check_is_emoji_name_valid(client, event, name):
        return
    
    if (roles is not None):
        roles = parse_roles(roles, event.guild)
    
    await client.interaction_component_acknowledge(event, wait = False)
    emoji = Emoji._create_partial(int(emoji_id), emoji_name, True if emoji_animated == '1' else False)
    
    old_name = emoji.name
    old_roles = emoji.roles
    
    try:
        await client.emoji_edit(emoji, name = name, roles = roles)
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
        
        elif error_code == ERROR_CODES.cannot_mix_subscription_and_non_subscription_roles_for_an_emoji:
            error_message = 'Cannot mix subscription and non-subscription roles for an emoji.'
        
        else:
            raise
        
        await propagate_check_error_message(client, event, error_message)
        return
    
    embed = create_base_embed(emoji, 'Emoji edited')
    add_change_field(embed, 'Name', old_name, name)
    add_change_field(
        embed,
        'Roles',
        join_roles(old_roles),
        join_roles(sorted(roles) if (roles is not None) else None),
    )
    await client.interaction_followup_message_create(
        event,
        components = ROW_SNIPE_ACTION_RESPONSE,
        embed = embed,
        show_for_invoking_user_only = True,
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_EDIT_STICKER)
async def snipe_interaction_edit_sticker(client, event):
    """
    Pops up an sticker edit confirmation form.
    
    This function is a coroutine.
    
    Returns
    -------
    form : `None`, ``InteractionForm``
    """
    if not await check_has_manage_emojis_and_stickers_permission(client, event):
        return
    
    sticker_id = get_entity_id_from_event(event)
    if not sticker_id:
        return
    
    sticker = await get_sticker(client, sticker_id)
    if sticker is None:
        return
    
    if not await check_sticker_type_modify(client, event, sticker):
        return
    
    return Form(
        f'Edit sticker: {sticker.name}',
        [
            TextInput(
                'Name',
                min_length = 2,
                max_length = 32,
                custom_id = 'name',
                placeholder = 'Sticker name',
                value = sticker.name,
            ),
            TextInput(
                'Tags',
                min_length = 0,
                max_length = 100,
                custom_id = 'tags',
                placeholder = 'Sticker tags',
                value = join_sticker_tags(sticker),
            ),
            TextInput(
                'Description',
                min_length = 0,
                max_length = 1024,
                custom_id = 'description',
                placeholder = 'Sticker description',
                value = sticker.description,
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = create_sticker_edit_form_custom_id(sticker)
    )


@SLASH_CLIENT.interactions(custom_id = STICKER_EDIT_FORM_PATTERN, target = 'form')
async def snipe_confirm_edit_sticker(client, event, sticker_id, *, name, tags, description):
    """
    Handles sticker edit confirmation.
    
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
        The new name of the sticker.
    tags : `None`, `str` (Keyword only)
        The new tags of the sticker.
    description : `None`, `str` (Keyword only)
        The new description of the sticker.
    """
    await client.interaction_component_acknowledge(event, wait = False)
    sticker = await get_sticker(client, int(sticker_id))
    
    
    old_name = sticker.name
    old_tags = join_sticker_tags(sticker)
    old_description = sticker.description
    
    if name is None:
        name = old_name
    
    if tags is None:
        tags = old_tags
    else:
        tags = parse_and_join_tags(tags)
    
    try:
        await client.sticker_guild_edit(sticker, name = name, tags = tags, description = description)
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
        
        else:
            raise
        
        await propagate_check_error_message(client, event, error_message)
        return
    
    embed = create_base_embed(sticker, 'Sticker edited')
    add_change_field(embed, 'Name', old_name, name)
    add_change_field(embed, 'Tags', old_tags, tags)
    add_change_field(
        embed,
        'Tags',
        (old_description if (old_description is not None) else ''),
        (description if (description is not None) else ''),
    )
    await client.interaction_followup_message_create(
        event,
        components = ROW_SNIPE_ACTION_RESPONSE,
        embed = embed,
        show_for_invoking_user_only = True,
    )
