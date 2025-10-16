__all__ = ()

from itertools import chain

from hata import DiscordException, ERROR_CODES, create_partial_emoji_from_id

from ...bots import FEATURE_CLIENTS

from .automation_reaction_role_item import AutomationReactionRoleItem
from .component_builders import (
    build_automation_reaction_role_entry_delete_form, build_automation_reaction_role_entry_overview_components,
    build_automation_reaction_role_entry_overview_deleted_components, build_automation_reaction_role_item_add_form,
    build_automation_reaction_role_item_delete_form, build_automation_reaction_role_item_modify_form,
    build_automation_reaction_role_listing_components
)
from .constants import AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID, ENTRY_PAGE_SIZE
from .content_builders import get_emoji_name, produce_role_listing
from .custom_ids import (
    CUSTOM_ID_ADD_ROLES, CUSTOM_ID_EMOJI, CUSTOM_ID_ENTRY_DELETE_PATTERN, CUSTOM_ID_ENTRY_PAGE_VIEW_DECREMENT_DISABLED,
    CUSTOM_ID_ENTRY_PAGE_VIEW_INCREMENT_DISABLED, CUSTOM_ID_ENTRY_PAGE_VIEW_PATTERN,
    CUSTOM_ID_LISTING_PAGE_VIEW_DECREMENT_DISABLED, CUSTOM_ID_LISTING_PAGE_VIEW_INCREMENT_DISABLED,
    CUSTOM_ID_LISTING_PAGE_VIEW_PATTERN,  CUSTOM_ID_ITEM_ADD_PATTERN, CUSTOM_ID_ITEM_DELETE_PATTERN,
    CUSTOM_ID_ITEM_MODIFY_PATTERN, CUSTOM_ID_REMOVE_ROLES
)
from .helpers import (
    get_automation_reaction_role_entry_and_sync, get_automation_reaction_role_entry_listing_and_sync_page,
    get_automation_reaction_role_item_with_emoji_id, get_highest_client_with_role,
    iter_automation_reaction_role_entry_role_ids, iter_automation_reaction_role_entry_role_ids_excluding_item,
    iter_role_ids_of_roles_nullable
)
from .queries import query_delete_automation_reaction_role_entry, query_update_automation_reaction_role_entry


@FEATURE_CLIENTS.interactions(
    custom_id = [
        CUSTOM_ID_ENTRY_PAGE_VIEW_DECREMENT_DISABLED,
        CUSTOM_ID_ENTRY_PAGE_VIEW_INCREMENT_DISABLED,
        CUSTOM_ID_LISTING_PAGE_VIEW_DECREMENT_DISABLED,
        CUSTOM_ID_LISTING_PAGE_VIEW_INCREMENT_DISABLED,
    ],
)
async def handle_dummy():
    """
    Dummy handler for always disabled components.
    
    This function is a coroutine.
    """
    pass


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_LISTING_PAGE_VIEW_PATTERN)
async def handle_listing_page_view(
    client,
    interaction_event,
    listing_page_index,
):
    """
    Handles a listing page view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The selected listing page's index as string representing a hexadecimal integer.
    """
    try:
        listing_page_index = int(listing_page_index, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    guild = interaction_event.guild
    if guild is None:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    automation_reaction_role_entry_listing = await get_automation_reaction_role_entry_listing_and_sync_page(
        guild.id, listing_page_index
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        components = build_automation_reaction_role_listing_components(
            guild,
            automation_reaction_role_entry_listing,
            listing_page_index,
        ),
    )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ENTRY_PAGE_VIEW_PATTERN)
async def handle_entry_page_view(
    client,
    interaction_event,
    listing_page_index,
    message_id,
    overview_page_index,
):
    """
    Handles an entry's item page view interaction.
    
    This function is a coroutine.
    
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    overview_page_index : `str`
        The current overview page's index as string representing a hexadecimal integer.
    """
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
        overview_page_index = int(overview_page_index, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    automation_reaction_role_entry = await get_automation_reaction_role_entry_and_sync(message_id)
    if automation_reaction_role_entry is None:
        components = build_automation_reaction_role_entry_overview_deleted_components(
            listing_page_index,
        )
    else:
        components = build_automation_reaction_role_entry_overview_components(
            client,
            listing_page_index,
            automation_reaction_role_entry,
            overview_page_index,
        )
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        components = components,
    )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ENTRY_DELETE_PATTERN)
async def handle_entry_delete_request(
    client,
    interaction_event,
    listing_page_index,
    message_id,
):
    """
    Handles an entry delete request.
    
    This function is a coroutine.
    
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    Returns
    -------
    interaction_form : ``None | InteractionForm``
    """
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    # Here we do not need to sync the message, we just prompt a confirmation.
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message_id]
    except KeyError:
        await client.interaction_component_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_deleted_components(
                listing_page_index,
            ),
        )
        return
    
    return build_automation_reaction_role_entry_delete_form(listing_page_index, automation_reaction_role_entry)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ENTRY_DELETE_PATTERN, target = 'form')
async def handle_entry_delete_submit(
    client,
    interaction_event,
    listing_page_index,
    message_id,
):
    """
    Handles an entry delete confirmation.
    
    This function is a coroutine.
    
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    """
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    guild = interaction_event.guild
    if guild is None:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    # Here we do not need to sync the message, just delete the entry if found.
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message_id]
    except KeyError:
        pass
    else:
        await query_delete_automation_reaction_role_entry(automation_reaction_role_entry)
    
    automation_reaction_role_entry_listing = await get_automation_reaction_role_entry_listing_and_sync_page(
        guild.id, listing_page_index
    )
    
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        components = build_automation_reaction_role_listing_components(
            guild,
            automation_reaction_role_entry_listing,
            listing_page_index,
        ),
    )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ITEM_ADD_PATTERN)
async def handle_item_add_request(
    client,
    interaction_event,
    listing_page_index,
    message_id,
):
    """
    Handles an item add request.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    Returns
    -------
    interaction_form : ``None | InteractionForm``
    """
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    # Here we do not need to sync the message, we just prompt a confirmation.
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message_id]
    except KeyError:
        await client.interaction_component_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_deleted_components(
                listing_page_index,
            ),
        )
        return
    
    return build_automation_reaction_role_item_add_form(client, listing_page_index, automation_reaction_role_entry)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ITEM_ADD_PATTERN, target = 'form')
async def handle_item_add_submit(
    client,
    interaction_event,
    listing_page_index,
    message_id,
    *,
    emoji_ids : CUSTOM_ID_EMOJI,
    add_roles : CUSTOM_ID_ADD_ROLES,
    remove_roles : CUSTOM_ID_REMOVE_ROLES,
):
    """
    Handles an item add confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    emoji_ids : `None | tuple<str>`, (Keyword only)
        The selected emoji's identifier.
    
    add_roles : ``None | tuple<Role>``, (Keyword only)
        The selected roles to be added identifiers.
    
    remove_roles : ``None | tuple<Role>``, (Keyword only)
        The selected roles to be removed identifiers.
    """
    if (emoji_ids is None):
        return
    
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
        emoji_id = int(emoji_ids[0], 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    guild = interaction_event.guild
    if guild is None:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    automation_reaction_role_entry = await get_automation_reaction_role_entry_and_sync(message_id)
    if (automation_reaction_role_entry is None):
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_deleted_components(
                listing_page_index,
            ),
        )
        return
    
    while True:
        if not emoji_id:
            error_message = 'Please select an emoji.'
            break
        
        highest_client_with_role = get_highest_client_with_role(guild)
        
        # If nothing is returned means we do not have anyone who can give a role out.
        if (highest_client_with_role is None):
            error_message = 'I require `manage roles` permission to add or remove roles.'
            break
        
        # Try to add the reaction.
        try:
            await highest_client_with_role[0].reaction_add(
                automation_reaction_role_entry.message, create_partial_emoji_from_id(emoji_id),
            )
        except ConnectionError:
            return
        
        except DiscordException as exception:
            if exception.status >= 500:
                return
            
            exception_code = exception.code
            if exception_code == ERROR_CODES.missing_access:
                return
            
            if exception_code == ERROR_CODES.unknown_message:
                error_message = 'Failed to add reaction: message deleted.'
                break
            
            if exception_code == ERROR_CODES.unknown_channel:
                error_message = 'Failed to add reaction: message\'s channel deleted.'
                break
            
            if exception_code == ERROR_CODES.missing_permissions:
                error_message = 'Failed to add reaction: permissions changed.'
                break
            
            if exception_code == ERROR_CODES.max_reactions:
                error_message = 'Failed to add reaction: message reached max reactions.'
                break
            
            raise
        
        
        # Check whether the emoji is already given out.
        if (get_automation_reaction_role_item_with_emoji_id(automation_reaction_role_entry, emoji_id) is not None):
            error_message = f'The selected emoji {get_emoji_name(client, emoji_id)!s} is already in use.'
            break
        
        # Check whether any of the roles is higher than our.
        client_highest_role = highest_client_with_role[1]
        selected_higher_role = next(
            (
                role for role in
                chain.from_iterable(roles for roles in (add_roles, remove_roles) if roles is not None)
                if role >= client_highest_role
            ),
            None,
        )
        if (selected_higher_role is not None):
            error_message = f'The selected role {selected_higher_role.mention} is higher than my top role (or same).'
            break
        
        # Check whether add_role_ids and remove_role_ids has intersection.
        intersection = {*iter_role_ids_of_roles_nullable(add_roles)} & {*iter_role_ids_of_roles_nullable(remove_roles)}
        if intersection:
            error_message = ''.join([
                'Added roles and removed roles cannot contain an intersection:',
                *produce_role_listing(tuple(intersection)),
            ])
            break
        
        # Check whether add_role_ids and existing_remove_role_ids has intersection.
        intersection = (
              {*iter_role_ids_of_roles_nullable(add_roles)} &
              {*iter_automation_reaction_role_entry_role_ids(
                  automation_reaction_role_entry, AutomationReactionRoleItem.remove_role_ids
              )}
        )
        if intersection:
            error_message = ''.join([
                'Added roles and existing removed roles cannot contain an intersection:',
                *produce_role_listing(tuple(intersection)),
            ])
            break
        
        # Check whether existing_add_role_ids and remove_role_ids has intersection.
        intersection = (
              {*iter_automation_reaction_role_entry_role_ids(
                  automation_reaction_role_entry, AutomationReactionRoleItem.add_role_ids
              )} &
              {*iter_role_ids_of_roles_nullable(remove_roles)}
        )
        if intersection:
            error_message = ''.join([
                'Existing added roles and removed roles cannot contain an intersection:',
                *produce_role_listing(tuple(intersection)),
            ])
            break
        
        # Save
        automation_reaction_role_item = AutomationReactionRoleItem(
            emoji_id,
            (None if add_roles is None else tuple(sorted(role.id for role in add_roles))),
            (None if remove_roles is None else tuple(sorted(role.id for role in remove_roles))),
        )
        
        automation_reaction_role_items = automation_reaction_role_entry.items
        if automation_reaction_role_items is None:
            automation_reaction_role_items = []
            automation_reaction_role_entry.items = automation_reaction_role_items
        
        automation_reaction_role_items.append(automation_reaction_role_item)
        await query_update_automation_reaction_role_entry(automation_reaction_role_entry)
        
        # Respond
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_components(
                client,
                listing_page_index,
                automation_reaction_role_entry,
                (len(automation_reaction_role_items) - 1) // ENTRY_PAGE_SIZE,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True,
    )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ITEM_MODIFY_PATTERN)
async def handle_item_modify_request(
    client,
    interaction_event,
    listing_page_index,
    message_id,
    overview_page_index,
    emoji_id,
):
    """
    Handles an item modify request.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    overview_page_index : `str`
        The current overview page's index as string representing a hexadecimal integer.
    
    emoji_id : `str`
        The selected emoji's identifier as string representing a hexadecimal integer.
    
    Returns
    -------
    interaction_form : ``None | InteractionForm``
    """
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
        overview_page_index = int(overview_page_index, 16)
        emoji_id = int(emoji_id, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    # Here we do not need to sync the message, we just prompt a confirmation.
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message_id]
    except KeyError:
        await client.interaction_component_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_deleted_components(
                listing_page_index,
            ),
        )
        return
    
    # Search the item we want to modify. On error send a message.
    automation_reaction_role_item = get_automation_reaction_role_item_with_emoji_id(
        automation_reaction_role_entry, emoji_id
    )
    if (automation_reaction_role_item is None):
        await client.interaction_component_acknowledge(
            interaction_event,
        )
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            content = 'The selected item does not exist anymore.',
            show_for_invoking_user_only = True,
        )
        return
    
    # Respond
    return build_automation_reaction_role_item_modify_form(
        client, listing_page_index, automation_reaction_role_entry, overview_page_index, automation_reaction_role_item
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ITEM_MODIFY_PATTERN, target = 'form')
async def handle_item_modify_submit(
    client,
    interaction_event,
    listing_page_index,
    message_id,
    overview_page_index,
    emoji_id,
    *,
    add_roles : CUSTOM_ID_ADD_ROLES,
    remove_roles : CUSTOM_ID_REMOVE_ROLES,
):
    """
    Handles an item modify confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    overview_page_index : `str`
        The current overview page's index as string representing a hexadecimal integer.
    
    emoji_id : `str`
        The selected emoji's identifier as string representing a hexadecimal integer.
    
    add_roles : ``None | tuple<Role>``, (Keyword only)
        The selected roles to be added identifiers.
    
    remove_roles : ``None | tuple<Role>``, (Keyword only)
        The selected roles to be removed identifiers.
    """
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
        overview_page_index = int(overview_page_index, 16)
        emoji_id = int(emoji_id, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    guild = interaction_event.guild
    if guild is None:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    automation_reaction_role_entry = await get_automation_reaction_role_entry_and_sync(message_id)
    if (automation_reaction_role_entry is None):
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_deleted_components(
                listing_page_index,
            ),
        )
        return
    
    while True:
        # Check whether the item was deleted in the meantime.
        automation_reaction_role_item = get_automation_reaction_role_item_with_emoji_id(
            automation_reaction_role_entry, emoji_id
        )
        if (automation_reaction_role_item is None):
            error_message = f'The item assigned to emoji {get_emoji_name(client, emoji_id)!s} was deleted.'
            break
        
        # Check whether add_role_ids and remove_role_ids has intersection.
        intersection = {*iter_role_ids_of_roles_nullable(add_roles)} & {*iter_role_ids_of_roles_nullable(remove_roles)}
        if intersection:
            error_message = ''.join([
                'Added roles and removed roles cannot contain an intersection:',
                *produce_role_listing(tuple(intersection)),
            ])
            break
        
        # Check whether add_role_ids and existing_remove_role_ids has intersection.
        intersection = (
              {*iter_role_ids_of_roles_nullable(add_roles)} &
              {*iter_automation_reaction_role_entry_role_ids_excluding_item(
                  automation_reaction_role_entry,
                  AutomationReactionRoleItem.remove_role_ids,
                  automation_reaction_role_item,
              )}
        )
        if intersection:
            error_message = ''.join([
                'Added roles and existing removed roles cannot contain an intersection:',
                *produce_role_listing(tuple(intersection)),
            ])
            break
        
        # Check whether existing_add_role_ids and remove_role_ids has intersection.
        intersection = (
              {*iter_automation_reaction_role_entry_role_ids_excluding_item(
                  automation_reaction_role_entry,
                  AutomationReactionRoleItem.add_role_ids,
                  automation_reaction_role_item,
              )} &
              {*iter_role_ids_of_roles_nullable(remove_roles)}
        )
        if intersection:
            error_message = ''.join([
                'Existing added roles and removed roles cannot contain an intersection:',
                *produce_role_listing(tuple(intersection)),
            ])
            break
        
        # Save
        automation_reaction_role_item.add_role_ids = (
            None if add_roles is None else tuple(sorted(role.id for role in add_roles))
        )
        automation_reaction_role_item.remove_role_ids = (
            None if remove_roles is None else tuple(sorted(role.id for role in remove_roles))
        )
        await query_update_automation_reaction_role_entry(automation_reaction_role_entry)
        
        # Respond
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_components(
                client,
                listing_page_index,
                automation_reaction_role_entry,
                overview_page_index,
            ),
        )
        return
    
    await client.interaction_followup_message_create(
        interaction_event,
        allowed_mentions = None,
        content = error_message,
        show_for_invoking_user_only = True,
    )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ITEM_DELETE_PATTERN)
async def handle_item_delete_request(
    client,
    interaction_event,
    listing_page_index,
    message_id,
    overview_page_index,
):
    """
    Handles an item delete request.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    overview_page_index : `str`
        The current overview page's index as string representing a hexadecimal integer.
    """
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
        overview_page_index = int(overview_page_index, 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    # Here we do not need to sync the message, we just prompt a confirmation.
    try:
        automation_reaction_role_entry = AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[message_id]
    except KeyError:
        await client.interaction_component_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_deleted_components(
                listing_page_index,
            ),
        )
        return
    
    return build_automation_reaction_role_item_delete_form(
        client, listing_page_index, automation_reaction_role_entry, overview_page_index
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ITEM_DELETE_PATTERN, target = 'form')
async def handle_item_delete_submit(
    client,
    interaction_event,
    listing_page_index,
    message_id,
    overview_page_index,
    *,
    emoji_ids : CUSTOM_ID_EMOJI,
):
    """
    Handles an item delete confirmation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    listing_page_index : `str`
        The current listing page's index as string representing a hexadecimal integer.
    
    message_id : `str`
        The selected entry's message's identifier.
    
    overview_page_index : `str`
        The current overview page's index as string representing a hexadecimal integer.
    
    emoji_ids : `None | tuple<str>`, (Keyword only)
        The selected emoji's identifier.
    """
    if (emoji_ids is None):
        return
    
    try:
        listing_page_index = int(listing_page_index, 16)
        message_id = int(message_id, 16)
        overview_page_index = int(overview_page_index, 16)
        emoji_id = int(emoji_ids[0], 16)
    except ValueError:
        return
    
    if not interaction_event.user_permissions.administrator:
        return
    
    guild = interaction_event.guild
    if guild is None:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    automation_reaction_role_entry = await get_automation_reaction_role_entry_and_sync(message_id)
    if (automation_reaction_role_entry is None):
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_deleted_components(
                listing_page_index,
            ),
        )
        return
    
    # We can ignore the case if it is already deleted.
    automation_reaction_role_item = get_automation_reaction_role_item_with_emoji_id(
        automation_reaction_role_entry, emoji_id
    )
    if (automation_reaction_role_item is not None):
        automation_reaction_role_items = automation_reaction_role_entry.items
        automation_reaction_role_items.remove(automation_reaction_role_item)
        if not automation_reaction_role_items:
            automation_reaction_role_entry.items = None
        
        await query_update_automation_reaction_role_entry(automation_reaction_role_entry)
    
    # Respond
    await client.interaction_response_message_edit(
        interaction_event,
        allowed_mentions = None,
        components = build_automation_reaction_role_entry_overview_components(
            client,
            listing_page_index,
            automation_reaction_role_entry,
            overview_page_index,
        ),
    )
    return
