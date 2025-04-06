import vampytest

from ...inventory_core import Inventory
from ...item_core import ITEM_ID_FISHING_ROD, get_item

from ..actions import get_discard_item_suggestions


def _iter_options():
    yield (
        202504050010,
        None,
        None,
        None,
    )
    
    yield (
        202504050011,
        (ITEM_ID_FISHING_ROD,),
        'fish',
        [
            (get_item(ITEM_ID_FISHING_ROD).name, ITEM_ID_FISHING_ROD),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_discard_item_suggestions(user_id, item_ids, value):
    """
    Tests whether ``get_discard_item_suggestions`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create inventory for.
    
    item_ids : `None | tuple<int>`
        Item identifiers to fill the inventory with.
    
    value : `None | str`
        Value to filter for.
    
    Returns
    -------
    output : `None | list<(str, int)>`
    """
    inventory = Inventory(user_id)
    
    if (item_ids is not None):
        for item_id in item_ids:
            inventory.modify_item_amount(get_item(item_id), 4)
    
    async def mock_get_inventory(input_user_id):
        nonlocal inventory
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return inventory
    
    mocked = vampytest.mock_globals(
        get_discard_item_suggestions,
        get_inventory = mock_get_inventory,
    )
    
    output = await mocked(user_id, value)
    vampytest.assert_instance(output, list, nullable = True)
    return output
