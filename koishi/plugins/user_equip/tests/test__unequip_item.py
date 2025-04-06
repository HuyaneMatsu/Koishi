import vampytest

from ....bot_utils.models import DB_ENGINE

from ...inventory_core import Inventory
from ...item_core import ITEM_FLAG_WEAPON, ITEM_ID_FISHING_ROD, ITEM_ID_PEACH, Item, get_item
from ...stats_core import Stats

from ..actions import unequip_item


def _iter_options():
    yield (
        202504020020,
        None,
        'item_id_weapon',
        0,
        ITEM_FLAG_WEAPON,
        (
            set(),
            0,
            None,
        ),
        
    )
    
    yield (
        202504020021,
        (ITEM_ID_FISHING_ROD,),
        'item_id_weapon',
        ITEM_ID_PEACH,
        ITEM_FLAG_WEAPON,
        (
            {ITEM_ID_FISHING_ROD, ITEM_ID_PEACH},
            0,
            get_item(ITEM_ID_PEACH)
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__unequip_item(user_id, item_ids, equipped_item_field_name, equipped_item_id, item_flag):
    """
    Tests whether ``unequip_item`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create inventory for.
    
    item_ids : `None | tuple<int>`
        Item identifiers to fill the inventory with.
    
    equipped_item_field_name : `str`
        The quipped item's name.
    
    equipped_item_id : `int`
        The equipped item's identifier.
    
    item_flag : `int`
        The item flag to filter for.
    
    Returns
    -------
    item_ids__and_unequipped_item_and_output : `(set<int>, int, None | Item>)`
    """
    inventory = Inventory(user_id)
    stats = Stats(user_id)
    stats.set(equipped_item_field_name, equipped_item_id)
    
    if (item_ids is not None):
        for item_id in item_ids:
            inventory.modify_item_amount(get_item(item_id), 1)
    
    async def mock_get_inventory(input_user_id):
        nonlocal inventory
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return inventory
    
    async def mock_get_stats(input_user_id):
        nonlocal stats
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return stats
    
    mocked = vampytest.mock_globals(
        unequip_item,
        get_inventory = mock_get_inventory,
        get_stats = mock_get_stats,
    )
    
    output = await mocked(user_id, item_flag)
    vampytest.assert_instance(output, Item, nullable = True)
    return (
        {item_entry.item.id for item_entry in inventory.iter_item_entries()},
        getattr(stats, equipped_item_field_name),
        output,
    )
