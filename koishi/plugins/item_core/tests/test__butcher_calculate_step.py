import vampytest

from ..flags import ITEM_FLAG_BUTCHERABLE
from ..item import Item
from ..logic_butcher import butcher_calculate_step
from ..option_butcher import OptionButcher


def _iter_options():
    item_id_0 = 10
    item_id_1 = 12
    
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
    
    
    yield (
        item_0,
        -1,
        18,
        1.0,
        (
            [
                (item_id_1, 169),
            ],
            8289,
        ),
    )
    
    yield (
        item_0,
        0,
        18,
        1.0,
        (
            [
                (item_id_1, 258),
            ],
            8111,
        ),
    )
    
    yield (
        item_1,
        -1,
        18,
        1.0,
        (
            None,
            0,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__butcher_calculate_step(item, index, seed, multiplier):
    """
    Tests whether ``butcher_calculate_step`` works as intended.
    
    Parameters
    ----------
    item : ``Item``
        The item to butcher.
    
    index : `int`
        The item's index in the butcher queue. `-1` if initial.
    
    seed : `int`
        Seed to use.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    output : `(None | list<(int, int)>, int)`
    """
    output = butcher_calculate_step(item, index, seed, multiplier)
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    
    accumulated_loot_normalised, accumulated_energy_cost = output
    vampytest.assert_instance(accumulated_loot_normalised, list, nullable = True)
    vampytest.assert_instance(accumulated_energy_cost, int)
    
    if (accumulated_loot_normalised is not None):
        for element in accumulated_loot_normalised:
            vampytest.assert_instance(element, tuple)
            vampytest.assert_eq(len(element), 2)
            item_id, amount = element
            vampytest.assert_instance(item_id, int)
            vampytest.assert_instance(amount, int)
    
    return output
