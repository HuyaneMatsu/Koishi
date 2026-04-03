import vampytest

from ....bot_utils.models import DB_ENGINE

from ...inventory_core import Inventory, ItemEntry
from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..actions import discard_item


def _iter_options():
    yield (
        202504050012,
        None,
        'fish',
        2,
        (
            set(),
            (
                None,
                0,
                0,
            ),
        ),
        
    )
    
    yield (
        202504050013,
        [
            (ITEM_ID_FISHING_ROD, 4),
        ],
        'fish',
        -2,
        (
            {
                ItemEntry(get_item(ITEM_ID_FISHING_ROD), 4)
            },
            (
                get_item(ITEM_ID_FISHING_ROD),
                0,
                4,
            )
        ),
    )
    
    yield (
        202504050014,
        [
            (ITEM_ID_FISHING_ROD, 4),
        ],
        'fish',
        5,
        (
            set(),
            (
                get_item(ITEM_ID_FISHING_ROD),
                4,
                0,
            )
        ),
    )
    
    yield (
        202504050015,
        [
            (ITEM_ID_FISHING_ROD, 4),
        ],
        'fish',
        2,
        (
            {
                ItemEntry(get_item(ITEM_ID_FISHING_ROD), 2)
            },
            (
                get_item(ITEM_ID_FISHING_ROD),
                2,
                2,
            )
        ),
    )


@vampytest.skip_if(DB_ENGINE is not None)
@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__discard_item(user_id, item_ids_and_amounts, value, amount):
    """
    Tests whether ``discard_item`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create inventory for.
    
    item_ids_and_amounts : `None | list<(int, int)>`
        Item identifiers and amounts to fill the inventory with.
    
    value : `str`
        Item name to select.
    
    amount : `int`
        The amount of items to discard.
    
    Returns
    -------
    item_ids_and_output : `(set<int>, (None | Item, int, int)>)`
    """
    inventory = Inventory(user_id)
    
    if (item_ids_and_amounts is not None):
        for item_id, item_amount in item_ids_and_amounts:
            inventory.modify_item_amount(get_item(item_id), item_amount)
    
    async def mock_get_inventory(input_user_id):
        nonlocal inventory
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return inventory
    
    mocked = vampytest.mock_globals(
        discard_item,
        get_inventory = mock_get_inventory,
    )
    
    output = await mocked(user_id, value, amount)
    vampytest.assert_instance(output, tuple)
    return (
        {*inventory.iter_item_entries()},
        output,
    )
