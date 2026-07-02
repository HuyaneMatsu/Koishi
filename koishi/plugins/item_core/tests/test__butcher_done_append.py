import vampytest

from ..flags import ITEM_FLAG_BUTCHERABLE
from ..item import Item
from ..logic_butcher import butcher_done_append
from ..option_butcher import OptionButcher


def _iter_options():
    item_id_0 = 10
    item_id_1 = 11
    item_id_2 = 12
    
    item_0 = Item(
        item_id_0,
        'item 0',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(True, 1, 2, 100, item_id_1, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_1, 8, 13, 15),
        ),
    )
    
    item_1 = Item(
        item_id_1,
        'item 1',
        None,
        'description',
        0,
        0,
        0,
        None,
        None,
    )
    
    item_2 = Item(
        item_id_2,
        'item 2',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(True, 1, 2, 100, item_id_1, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_1, 8, 13, 15),
        ),
    )
    
    items = {
        item_id_0 : item_0,
        item_id_1 : item_1,
        item_id_2 : item_2,
    }
    
    yield (
        [
            (item_id_0, 1),
            (item_id_1, 2),
        ],
        12,
        [
            (item_0, 0),
        ],
        item_0,
        0,
        [
            (item_id_2, 2),
            (item_id_1, 4),
        ],
        5,
        items,
        (
            [
                (item_id_1, 6),
                (item_id_2, 2),
            ],
            17,
            [
                (item_2, 1),
                (item_2, 2),
            ],
        ),
    )
    
    yield (
        None,
        0,
        None,
        item_1,
        0,
        None,
        0,
        items,
        (
            None,
            0,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__butcher_done_append(
    butcher_amounts_accumulated,
    energy_cost_accumulated,
    butcherables,
    butchered_item,
    butchered_index,
    butcher_amounts,
    energy_cost,
    items,
):
    """
    Tests whether ``butcher_done_append`` works as intended.
    
    Parameters
    ----------
    butcher_amounts_accumulated : `None | list<(int, int)>`
        Butchered amounts accumulated.
    
    energy_cost_accumulated : `int`
        Energy used accumulated.
    
    butcherables : ``None | list<(Item, int)>``
        Items which can be further butchered.
    
    butchered_item : ``Item``
        The just butchered item.
    
    butchered_index : `int`
        The just butchered item's index in the butcher queue.
        
    butcher_amounts : ``None | list<(int, int)>``
        Butchered amounts from the item.
    
    energy_cost : `int`
        Energy used by butchering.
    
    Returns
    -------
    output : ``(None | list<(int, int), int, None | list<(Item, int)>, int)``
    """
    if (butcher_amounts_accumulated is not None):
        butcher_amounts_accumulated = butcher_amounts_accumulated.copy()
    
    if (butcherables is not None):
        butcherables = butcherables.copy()
    
    if (butcher_amounts is not None):
        butcher_amounts = butcher_amounts.copy()
    
    
    mocked = vampytest.mock_globals(
        butcher_done_append,
        2,
        ITEMS = items,
    )
    output = mocked(
        butcher_amounts_accumulated,
        energy_cost_accumulated,
        butcherables,
        butchered_item,
        butchered_index,
        butcher_amounts,
        energy_cost,
    )
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 3)
    butcher_amounts_accumulated, energy_cost_accumulated, butcherables = output
    
    vampytest.assert_instance(butcher_amounts_accumulated, list, nullable = True)
    if (butcher_amounts_accumulated is not None):
        for element in butcher_amounts_accumulated:
            vampytest.assert_instance(element, tuple)
            vampytest.assert_eq(len(element), 2)
            item_id, amount = element
            vampytest.assert_instance(item_id, int)
            vampytest.assert_instance(amount, int)
    
    vampytest.assert_instance(energy_cost_accumulated, int)
    
    vampytest.assert_instance(butcherables, list, nullable = True)
    if (butcherables is not None):
        for element in butcherables:
            vampytest.assert_instance(element, tuple)
            vampytest.assert_eq(len(element), 2)
            item, amount = element
            vampytest.assert_instance(item, Item)
            vampytest.assert_instance(amount, int)
    
    return output
