import vampytest

from ...item_core import (
    ITEM_ID_BLUEBERRY, ITEM_ID_DEVILCART_OYSTER, ITEM_ID_FLYKILLER_AMANITA, ITEM_ID_PEACH, ITEM_ID_STRAWBERRY, get_item
)
from ...inventory_core import Inventory, ItemEntry

from ..paging import get_inventory_page


def _iter_options():
    item_blueberry = get_item(ITEM_ID_BLUEBERRY)
    item_devilcart_oyster = get_item(ITEM_ID_DEVILCART_OYSTER)
    item_flykiller_amanita = get_item(ITEM_ID_FLYKILLER_AMANITA)
    item_peach = get_item(ITEM_ID_PEACH)
    item_strawberry = get_item(ITEM_ID_STRAWBERRY)
    
    yield (
        202504050000,
        None,
        0,
        0,
        0,
        (
            [],
            0,
        )
    )
    
    yield (
        202504050001,
        [
            (item_blueberry, 4),
            (item_devilcart_oyster, 5),
            (item_flykiller_amanita, 6),
            (item_peach, 7),
            (item_strawberry, 8),
        ],
        0,
        0,
        1,
        (
            [
                ItemEntry(item_flykiller_amanita, 6),
                ItemEntry(item_peach, 7),
            ],
            3,
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_inventory_page(user_id, items_and_counts, sort_by, sort_order, page_index):
    """
    Tests whether ``get_inventory_page`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to who the inventory belongs.
    
    items_and_counts : `None | list<(Item, int)>`
        Items and their amounts in the inventory.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_index : `int`
        The current page's index.
    
    Returns
    -------
    output : `(list<ItemEntry>, int)`
    """
    mocked = vampytest.mock_globals(
        get_inventory_page,
        PAGE_SIZE = 2,
    )
    
    inventory = Inventory(user_id)
    
    if (items_and_counts is not None):
        for item_and_count in items_and_counts:
            inventory.modify_item_amount(*item_and_count)
    
    output = mocked(inventory, sort_by, sort_order, page_index)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], list)
    vampytest.assert_instance(output[1], int)
    return output
    
