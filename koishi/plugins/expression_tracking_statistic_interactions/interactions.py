__all__ = ()

from ...bots import FEATURE_CLIENTS

from ..expression_tracking import query_expression_in_guild_most_used, query_expression_of_guild_most_used

from .component_building import build_components
from .constants import VALID_ACTION_TYPE_COMBINATIONS_PACKED, MODE_GUILD_IN, MODE_GUILD_OF, VALID_MODES
from .custom_ids import (
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_CLOSE_RP,
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTIC_VIEW_RP,
)
from .helpers import unpack_action_types


@FEATURE_CLIENTS.interactions(custom_id = [
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_INCREMENT_DISABLED,
])
async def handle_expression_tracking_stats_dummy():
    """
    Dummy interaction event handler.
    
    This function is a coroutine.
    """


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_EXPRESSION_TRACKING_STATISTIC_VIEW_RP)
async def handle_expression_tracking_stats_view(
    client,
    interaction_event,
    user_id,
    mode,
    entity_id,
    action_types_packed,
    entity_filter_rule,
    months,
    page_index,
    page_size,
    order_decreasing,
):
    """
    Handles an expression tracking stats view interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as hexadecimal integer.
    
    mode : `str`
        The usage mode to respond with as hexadecimal integer.
    
    entity_id : `str`
        The entity's identifier in context as hexadecimal integer.
    
    action_types_packed : `str`
        The action types packed as a hexadecimal integer.
    
    entity_filter_rule : `str`
        Entity filter rule for detailed filtering as hexadecimal integer.
    
    months : `str`
        The amount of months to look back as a hexadecimal integer.
    
    page_index : `str`
        The page's index to display as a hexadecimal integer.
    
    page_size : `str`
        The page's size to display as a hexadecimal integer.
    
    order_decreasing : `str`
        Whether to order in a decreasing order as a hexadecimal integer.
    """
    # Convert input
    try:
        user_id = int(user_id, 16)
        mode = int(mode, 16)
        entity_id = int(entity_id, 16)
        action_types_packed = int(action_types_packed, 16)
        entity_filter_rule = int(entity_filter_rule, 16)
        months = int(months, 16)
        page_index = int(page_index, 16)
        page_size = int(page_size, 16)
        order_decreasing = int(order_decreasing, 16)
    except ValueError:
        return
    
    # Validate input
    if interaction_event.user_id != user_id:
        return
    
    if mode not in VALID_MODES:
        return
    
    if (not action_types_packed) or (action_types_packed not in VALID_ACTION_TYPE_COMBINATIONS_PACKED):
        return
    
    order_decreasing = True if order_decreasing else False
    
    guild = interaction_event.guild
    
    # If we are showing guild stats, make sure we are showing it of the current guild.
    if (mode == MODE_GUILD_OF) or (mode == MODE_GUILD_IN):
        if guild is None:
            return
        
        if (guild.id != entity_id):
            return
    
    else:
        # No other mode allowed currently
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    # Get data
    if mode == MODE_GUILD_OF:
        entries, page_count = await query_expression_of_guild_most_used(
            guild,
            unpack_action_types(action_types_packed),
            entity_filter_rule,
            months,
            page_index,
            page_size,
            order_decreasing,
        )
    
    elif mode == MODE_GUILD_IN:
        entries, page_count = await query_expression_in_guild_most_used(
            guild,
            unpack_action_types(action_types_packed),
            months,
            page_index,
            page_size,
            order_decreasing,
        )
    
    else:
        # No other cases:
        entries = []
        page_count = 0
    
    # Respond
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_components(
            client,
            interaction_event.user,
            guild,
            entries,
            page_count,
            mode,
            action_types_packed,
            entity_filter_rule,
            months,
            page_index,
            page_size,
            order_decreasing,
        ),
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_CLOSE_RP)
async def handle_expression_tracking_stats_close(
    client,
    interaction_event,
    user_id,
):
    """
    Handles an expression tracking stats close interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as hexadecimal integer.
    """
    # Convert input
    try:
        user_id = int(user_id, 16)
    except ValueError:
        return
    
    # Validate input
    if interaction_event.user_id != user_id:
        return
    
    # Delete the message
    await client.interaction_component_acknowledge(interaction_event)
    await client.interaction_response_message_delete(interaction_event)
