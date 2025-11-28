__all__ = ('user_inventory_command',)

from ..inventory_core import get_inventory
from ..user_stats_core import get_user_stats

from .component_building import build_inventory_view_components
from .constants import SORT_BY_DEFAULT, SORT_BYES, SORT_ORDER_DEFAULT, SORT_ORDERS
from .paging import get_inventory_page


async def user_inventory_command(
    client,
    interaction_event,
    sort_by : (SORT_BYES, 'How to sort the items.') = SORT_BY_DEFAULT,
    sort_order : (SORT_ORDERS, 'Sort ordering') = SORT_ORDER_DEFAULT,
):
    """
    Displays your inventory.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    sort_by : `int` = `SORT_BY_DEFAULT`, Optional
        How to sort the items.
    
    sort_order : `int` = `SORT_ORDER_DEFAULT`, Optional
        Sort ordering.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user = interaction_event.user
    
    stats = await get_user_stats(user.id)
    inventory = await get_inventory(user.id)
    item_entries, page_count = get_inventory_page(inventory, sort_by, sort_order, 0)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_inventory_view_components(
            user,
            interaction_event.guild_id,
            item_entries,
            sort_by,
            sort_order,
            0,
            page_count,
            inventory.weight,
            stats.stats_calculated.extra_inventory,
        ),
    )
