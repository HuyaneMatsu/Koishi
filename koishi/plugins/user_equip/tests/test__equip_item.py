import vampytest

from ....bot_utils.models import DB_ENGINE

from ...inventory_core import Inventory
from ...item_core import ITEM_FLAG_WEAPON, ITEM_ID_FISHING_ROD, ITEM_ID_PEACH, get_item
from ...user_stats_core import UserStats

from ..actions import equip_item


def _iter_options():
    yield (
        202504020010,
        None,
        'item_id_weapon',
        0,
        ITEM_FLAG_WEAPON,
        'fish',
        (
            set(),
            0,
            (
                None,
                None,
            ),
        ),
        
    )
    
    yield (
        202504020011,
        (ITEM_ID_FISHING_ROD,),
        'item_id_weapon',
        ITEM_ID_PEACH,
        ITEM_FLAG_WEAPON,
        'fish',
        (
            {ITEM_ID_PEACH},
            ITEM_ID_FISHING_ROD,
            (
                get_item(ITEM_ID_PEACH),
                get_item(ITEM_ID_FISHING_ROD),
            )
        ),
    )
    
    yield (
        202504020012,
        (ITEM_ID_FISHING_ROD,),
        'item_id_weapon',
        0,
        ITEM_FLAG_WEAPON,
        'fish',
        (
            set(),
            ITEM_ID_FISHING_ROD,
            (
                None,
                get_item(ITEM_ID_FISHING_ROD),
            )
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__equip_item(user_id, item_ids, equipped_item_field_name, equipped_item_id, item_flag, value):
    """
    Tests whether ``equip_item`` works as intended.
    
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
    
    value : `str`
        Item name to select.
    
    Returns
    -------
    item_ids__and_equipped_item_and_output : `(set<int>, int, (None | Item, None | Item)>)`
    """
    inventory = Inventory(user_id)
    stats = UserStats(user_id)
    stats.set(equipped_item_field_name, equipped_item_id)
    
    if (item_ids is not None):
        for item_id in item_ids:
            inventory.modify_item_amount(get_item(item_id), 1)
    
    async def mock_get_inventory(input_user_id):
        nonlocal inventory
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return inventory
    
    async def mock_get_user_stats(input_user_id):
        nonlocal stats
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return stats
    
    mocked = vampytest.mock_globals(
        equip_item,
        get_inventory = mock_get_inventory,
        get_user_stats = mock_get_user_stats,
    )
    
    output = await mocked(user_id, item_flag, value)
    vampytest.assert_instance(output, tuple)
    return (
        {item_entry.item.id for item_entry in inventory.iter_item_entries()},
        getattr(stats, equipped_item_field_name),
        output,
    )
