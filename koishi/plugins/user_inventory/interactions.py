__all__ = ('get_inventory_page_response',)

from hata.ext.slash import InteractionResponse

from ...bots import FEATURE_CLIENTS

from ..inventory_core import get_inventory
from ..stats_core import get_stats

from .component_builders import build_component_switch_page
from .constants import (
    CUSTOM_ID_INVENTORY_PAGE_CLOSE, CUSTOM_ID_INVENTORY_PAGE_DISABLED_DECREMENT,
    CUSTOM_ID_INVENTORY_PAGE_DISABLED_INCREMENT, CUSTOM_ID_INVENTORY_PAGE_N_PATTERN,
)
from .embed_builders import build_inventory_embed
from .paging import get_inventory_page


async def get_inventory_page_response(user_id, sort_by, sort_order, page_index):
    """
    Gets inventory page response for the given parameters.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The respective user's identifier.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_index : `int`
        The current page's index.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    stats = await get_stats(user_id)
    inventory = await get_inventory(user_id)
    item_entries, page_count = get_inventory_page(inventory, sort_by, sort_order, page_index)
    
    return InteractionResponse(
        components = build_component_switch_page(sort_by, sort_order, page_index, page_count),
        embed = build_inventory_embed(
            item_entries, page_index, sort_by, sort_order, inventory.weight, stats.stats_calculated.extra_inventory
        ),
    )


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
async def inventory_page_n(event, sort_by, sort_order, page_index):
    """
    Handles disabled inventory components.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
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
    if (event.user is not event.message.interaction.user):
        return
    
    try:
        sort_by = int(sort_by, 16)
        sort_order = int(sort_order, 16)
        page_index = int(page_index, 16)
    except ValueError:
        return
    
    yield
    yield await get_inventory_page_response(event.user_id, sort_by, sort_order, page_index)
