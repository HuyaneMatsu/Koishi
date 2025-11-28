__all__ = ()


from ...bots import FEATURE_CLIENTS

from ..inventory_core import get_inventory
from ..user_stats_core import get_user_stats

from .component_building import build_inventory_view_components
from .constants import (
    CUSTOM_ID_INVENTORY_PAGE_CLOSE, CUSTOM_ID_INVENTORY_PAGE_DISABLED_DECREMENT,
    CUSTOM_ID_INVENTORY_PAGE_DISABLED_INCREMENT, CUSTOM_ID_INVENTORY_PAGE_N_PATTERN,
)
from .paging import get_inventory_page


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_INVENTORY_PAGE_CLOSE)
async def inventory_close(client, event):
    """
    Closes the inventory message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    if not ((event.user is event.message.interaction.user) or event.user_permissions.manage_messages):
        return
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_response_message_delete(event)


@FEATURE_CLIENTS.interactions(
    custom_id = [CUSTOM_ID_INVENTORY_PAGE_DISABLED_DECREMENT, CUSTOM_ID_INVENTORY_PAGE_DISABLED_INCREMENT],
)
async def inventory_disabled():
    """
    Handles disabled inventory components.
    
    This function is a coroutine.
    """


@FEATURE_CLIENTS.interactions(
    custom_id = CUSTOM_ID_INVENTORY_PAGE_N_PATTERN,
)
async def inventory_page_n(client, interaction_event, user_id, sort_by, sort_order, page_index):
    """
    Handles disabled inventory components.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The user's identifier as a hexadecimal integer.
    
    sort_by : `str`
        Identifier to determine how item entries should be sorted.
        Hexadecimal representation of an integer.
    
    sort_order : `str`
        Identifier to determine sorting order.
        Hexadecimal representation of an integer.
    
    page_index : `str`
        The current page's index.
        Hexadecimal representation of an integer.
    
    Yields
    ------
    acknowledge / response : `None` / ``InteractionResponse``
    """
    try:
        user_id = int(user_id, 16)
        sort_by = int(sort_by, 16)
        sort_order = int(sort_order, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    user = interaction_event.user
    if user.id != user_id:
        return
    
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    stats = await get_user_stats(user_id)
    inventory = await get_inventory(user_id)
    item_entries, page_count = get_inventory_page(inventory, sort_by, sort_order, page_index)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_inventory_view_components(
            user,
            interaction_event.guild_id,
            item_entries,
            sort_by,
            sort_order,
            page_index,
            page_count,
            inventory.weight,
            stats.stats_calculated.extra_inventory,
        ),
    )
