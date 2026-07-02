import vampytest

from ..flags import ITEM_FLAG_BUTCHERABLE
from ..item import Item
from ..logic_butcher import butcher_calculate_done
from ..option_butcher import OptionButcher


def _iter_options():
    item_id_0 = 8
    item_id_1 = 9
    item_id_2 = 10
    item_id_3 = 11
    
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
            OptionButcher(False, 1, 2, 2, item_id_1, 0, 10, 0),
            OptionButcher(False, 1, 2, 2, item_id_3, 0, 2, 0),
        ),
    )
    
    item_1 = Item(
        item_id_1,
        'item 1',
        None,
        'description',
        ITEM_FLAG_BUTCHERABLE,
        0,
        0,
        None,
        (
            OptionButcher(True, 1, 2, 2, item_id_2, 0, 5, 0),
            OptionButcher(True, 1, 2, 2, item_id_3, 0, 3, 0),
        ),
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
            OptionButcher(True, 1, 2, 10, item_id_3, 0, 1, 0),
        ),
    )
    
    item_3 = Item(
        item_id_3,
        'item 3',
        None,
        'description',
        0,
        0,
        0,
        None,
        None,
    )
    
    items = {
        item_id_0 : item_0,
        item_id_1 : item_1,
        item_id_2 : item_2,
        item_id_3 : item_3,
    }
    
    yield (
        'Butcherable, no flags',
        item_0,
        901,
        0,
        1.0,
        items,
        (
            [
                (item_id_1, 1),
                (item_id_3, 1),
            ],
            12,
            [
                (item_1, 0),
            ],
        ),
    )
    
    yield (
        'Butcherable, no flags, with multiplier',
        item_0,
        501,
        0,
        2.0,
        items,
        (
            [
                (item_id_1, 1),
                (item_id_3, 1),
            ],
            6,
            [
                (item_1, 0),
            ],
        ),
    )
    
    yield (
        'Butcherable, no flags (no loot)',
        item_0,
        123,
        0,
        1.0,
        items,
        (
            None,
            0,
            None,
        ),
    )
    
    yield (
        'Butcherable, no flags (all loot)',
        item_0,
        261,
        0,
        1.0,
        items,
        (
            [
                (item_id_1, 2),
                (item_id_3, 1),
            ],
            22,
            [
                (item_1, 0),
                (item_1, 3),
            ],
        ),
    )
    
    yield (
        'Butcherable, no flags, with multiplier, butchered 1',
        item_0,
        261,
        8,
        2.0,
        items,
        (
            [
                (item_id_1, 1),
                (item_id_3, 1),
                (item_id_2, 2),
            ],
            16,
            [
                (item_1, 0),
                (item_2, 4),
                (item_2, 5),
            ],
        ),
    )
    
    yield (
        'Butcherable, no flags, with multiplier, butchered 1 + nested 1',
        item_0,
        261,
        40,
        2.0,
        items,
        (
            [
                (item_id_1, 1),
                (item_id_3, 11),
                (item_id_2, 1),
            ],
            21,
            [
                (item_1, 0),
                (item_2, 4),
            ],
        ),
    )
    
    yield (
        'Butcherable, no flags, with multiplier, butchered all',
        item_0,
        261,
        63,
        2.0,
        items,
        (
            [
                (item_id_3, 33),
            ],
            40,
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__butcher_calculate_done(item, seed, butcher_flags, multiplier, items):
    """
    Tests whether ``butcher_calculate_done`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        Item to butcher.
    
    seed : `int`
        Seed to use for generation.
    
    butcher_flags : `int`
        Flags described which body parts were already butchered.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    output : ``(None | list<(int, int), int, None | list<(Item, int)>)``
    """
    mocked = vampytest.mock_globals(
        butcher_calculate_done,
        2,
        ITEMS = items,
    )
    
    output = mocked(item, seed, butcher_flags, multiplier)
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
