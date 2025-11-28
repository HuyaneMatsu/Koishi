__all__ = ()

from ...bots import FEATURE_CLIENTS

from ..user_balance import USER_BALANCE_ALLOCATION_HOOKS, get_user_balance

from .component_building import build_details_components, build_view_components
from .constants import PAGE_SIZE
from .custom_ids import (
    USER_ALLOCATIONS_CUSTOM_ID_DETAILS_PATTERN, USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_INCREMENT_DISABLED, USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_PATTERN,
    USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED
)


@FEATURE_CLIENTS.interactions(
    custom_id = [
        USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
        USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_INCREMENT_DISABLED,
        USER_ALLOCATION_CUSTOM_ID_LINK_DISABLED,
    ],
)
async def handle_allocations_disabled():
    """
    Dummy interaction event handler.
    
    This function is a coroutine.
    """


@FEATURE_CLIENTS.interactions(
    custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_PATTERN,
)
async def handle_allocations_view_page(
    client,
    interaction_event,
    user_id,
    page_index,
):
    """
    Handles an allocation view page interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction.
    
    user_id : `str`
        The original invoking user's identifier as hexadecimal string.
    
    page_index : `str`
        The selected page's index as hexadecimal string.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
    )
    
    user_balance = await get_user_balance(user_id)
    allocations = [*user_balance.iter_allocations()]
    page_count = (len(allocations) + PAGE_SIZE - 1) // PAGE_SIZE
    allocations_page = allocations[page_index * PAGE_SIZE : (page_index + 1) * PAGE_SIZE]
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_view_components(
            interaction_event.user, page_index, page_count, interaction_event.guild_id, allocations_page
        ),
    )
    return


@FEATURE_CLIENTS.interactions(
    custom_id = USER_ALLOCATIONS_CUSTOM_ID_DETAILS_PATTERN,
)
async def handle_allocations_details(
    client,
    interaction_event,
    user_id,
    page_index,
    allocation_feature_id,
    allocation_session_id,
):
    """
    Handles an allocation details interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction.
    
    user_id : `str`
        The original invoking user's identifier as hexadecimal string.
    
    page_index : `str`
        The current page's index as hexadecimal string.
    
    allocation_feature_id : `str`
        The allocation feature's identifier as hexadecimal string.
    
    allocation_session_id : `str`
        The allocation session's identifier as hexadecimal string.
    """
    try:
        user_id = int(user_id, 16)
        page_index = int(page_index, 16)
        allocation_feature_id = int(allocation_feature_id, 16)
        allocation_session_id = int(allocation_session_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
    )
    
    while True:
        user_balance = await get_user_balance(user_id)
        for feature_id, session_id, amount in user_balance.iter_allocations():
            if (feature_id == allocation_feature_id) and (session_id == allocation_session_id):
                break
        else:
            error_message = 'The allocation no longer exists.'
            break
        
        try:
            user_balance_allocation_hook = USER_BALANCE_ALLOCATION_HOOKS[allocation_feature_id]
        except KeyError:
            session = None
        
        else:
            get_session_enty = user_balance_allocation_hook.get_session_enty
            if (get_session_enty is None):
                session = None
            else:
                session = await get_session_enty(allocation_session_id)
        
        await client.interaction_response_message_edit(
            interaction_event,
            components = build_details_components(
                user_id, page_index, allocation_feature_id, session_id, amount, session, interaction_event.guild_id
            ),
        )
        return
        
    await client.interaction_followup_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
    return
