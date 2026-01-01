__all__ = ()

from ...bots import FEATURE_CLIENTS
from ...bot_utils.user_getter import get_user

from ..user_stats_core import get_user_stats

from .component_building import build_user_stats_primary_components, build_user_stats_secondary_components
from .custom_ids import CUSTOM_ID_USER_STATS_PRIMARY_RP, CUSTOM_ID_USER_STATS_SECONDARY_RP


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_USER_STATS_PRIMARY_RP)
async def handle_user_stats_primary(
    client,
    interaction_event,
    user_id,
    target_user_id,
):
    """
    Handles a user stats primary view event. 
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as a string representing a hexadecimal integer.
    
    target_user_id : `str`
        The target user's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        target_user_id = int(target_user_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    target_user = interaction_event.user
    if target_user.id != target_user_id:
        target_user = await get_user(target_user_id)
    
    user_stats = await get_user_stats(target_user_id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_user_stats_primary_components(
            user_id, target_user, user_stats, interaction_event.guild_id
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_USER_STATS_SECONDARY_RP)
async def handle_user_stats_secondary(
    client,
    interaction_event,
    user_id,
    target_user_id,
):
    """
    Handles a user stats secondary view event. 
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as a string representing a hexadecimal integer.
    
    target_user_id : `str`
        The target user's identifier as a string representing a hexadecimal integer.
    """
    try:
        user_id = int(user_id, 16)
        target_user_id = int(target_user_id, 16)
    except ValueError:
        return
    
    if interaction_event.user_id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    target_user = interaction_event.user
    if target_user.id != target_user_id:
        target_user = await get_user(target_user_id)
    
    user_stats = await get_user_stats(target_user_id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_user_stats_secondary_components(
            user_id, target_user, user_stats, interaction_event.guild_id
        ),
    )
