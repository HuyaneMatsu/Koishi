import vampytest

from ...inventory_core import Inventory
from ...item_core import ITEM_FLAG_HEAD, ITEM_FLAG_WEAPON, ITEM_ID_FISHING_ROD, Item, get_item

from ..selection import select_item


def _iter_options():
    yield (
        202504010011,
        None,
        ITEM_FLAG_WEAPON,
        'fish',
        None,
    )
    
    yield (
        202504010013,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_WEAPON,
        'fish',
        get_item(ITEM_ID_FISHING_ROD),
    )
    
    yield (
        202504010017,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_HEAD,
        'fish',
        None
    )
    
    yield (
        202504010014,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_WEAPON,
        'potato',
        None,
    )
    
    yield (
        202504010016,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_WEAPON,
        str(ITEM_ID_FISHING_ROD),
        get_item(ITEM_ID_FISHING_ROD),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_item(user_id, item_ids, item_flag, value):
    """
    Tests whether ``select_item`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create inventory for.
    
    item_ids : `None | tuple<int>`
        Item identifiers to fill the inventory with.
    
    item_flag : `int`
        The item flag to filter for.
    
    value : `str`
        Value to filter for.
    
    Returns
    -------
    output : ``None | Item``
    """
    inventory = Inventory(user_id)
    
    if (item_ids is not None):
        for item_id in item_ids:
            inventory.modify_item_amount(get_item(item_id), 4)
    
    output = select_item(inventory, item_flag, value)
    vampytest.assert_instance(output, Item, nullable = True)
    return output
