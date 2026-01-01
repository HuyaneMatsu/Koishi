import vampytest

from ...inventory_core import Inventory
from ...item_core import (
    ITEM_FLAG_HEAD, ITEM_FLAG_EDIBLE, ITEM_ID_PEACH, ITEM_FLAG_WEAPON, ITEM_ID_FISHING_ROD, ITEM_ID_STRAWBERRY, get_item
)
from ..selection import create_item_suggestions


def _iter_options():
    yield (
        202504010003,
        None,
        ITEM_FLAG_WEAPON,
        None,
        None,
    )
    
    yield (
        202504010004,
        None,
        ITEM_FLAG_WEAPON,
        'fish',
        None,
    )
    
    yield (
        202504010005,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_WEAPON,
        None,
        [
            (get_item(ITEM_ID_FISHING_ROD).name, format(ITEM_ID_FISHING_ROD, 'x')),
        ],
    )
    
    yield (
        202504010006,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_WEAPON,
        'fish',
        [
            (get_item(ITEM_ID_FISHING_ROD).name, format(ITEM_ID_FISHING_ROD, 'x')),
        ],
    )
    
    yield (
        202504010007,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_HEAD,
        None,
        None
    )
    
    yield (
        202504010010,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_HEAD,
        'fish',
        None
    )
    
    yield (
        202504010008,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_WEAPON,
        'potato',
        None,
    )
    
    yield (
        202504010009,
        (ITEM_ID_FISHING_ROD,),
        ITEM_FLAG_WEAPON,
        format(ITEM_ID_FISHING_ROD, 'x'),
        [
            (get_item(ITEM_ID_FISHING_ROD).name, format(ITEM_ID_FISHING_ROD, 'x')),
        ],
    )
    
    # Test whether sorting works as intended.
    yield (
        202508190000,
        (
            ITEM_ID_PEACH,
            ITEM_ID_STRAWBERRY,
        ),
        ITEM_FLAG_EDIBLE,
        None,
        [
            (get_item(ITEM_ID_PEACH).name, format(ITEM_ID_PEACH, 'x')),
            (get_item(ITEM_ID_STRAWBERRY).name, format(ITEM_ID_STRAWBERRY, 'x')),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__create_item_suggestions(user_id, item_ids, item_flag, value):
    """
    Tests whether ``create_item_suggestions`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to create inventory for.
    
    item_ids : `None | tuple<int>`
        Item identifiers to fill the inventory with.
    
    item_flag : `int`
        The item flag to filter for.
    
    value : `None | str`
        Value to filter for.
    
    Returns
    -------
    output : `None | list<(str, str)>`
    """
    inventory = Inventory(user_id)
    
    if (item_ids is not None):
        for item_id in item_ids:
            inventory.modify_item_amount(get_item(item_id), 4)
    
    output = create_item_suggestions(inventory, item_flag, value)
    vampytest.assert_instance(output, list, nullable = True)
    return output
