import vampytest

from ..flags import ITEM_FLAG_BUTCHERABLE
from ..item import Item
from ..logic_butcher import butcher_calculate_done, butcher_calculate_step, butcher_done_append
from ..option_butcher import OptionButcher


def test__equals__butcher_calculate_step__butcher_calculate_done():
    """
    Tests whether both ``butcher_calculate_step`` and ``butcher_calculate_done`` act the same for the same input.
    """
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
    
    items = {
        item_id_0 : item_0,
        item_id_1 : item_1,
    }
    
    butcher_calculate_done_mocked = vampytest.mock_globals(
        butcher_calculate_done,
        2,
        ITEMS = items,
    )
    seed = 18
    multiplier = 1.0
    
    output_0 = butcher_calculate_step(item_0, -1, seed, multiplier)
    output_1 = butcher_calculate_done_mocked(item_0, seed, 0, multiplier)
    vampytest.assert_eq(output_0[0], output_1[0])
    vampytest.assert_eq(output_0[1], output_1[1])


def test__equals_butcher_add_to_amounts_accumulation__butcher_calculate_done():
    """
    Tests whether both ``butcher_add_to_amounts_accumulation`` and ``butcher_calculate_done``
    act the same for the same input.
    """
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
    
    butcher_calculate_done_mocked = vampytest.mock_globals(
        butcher_calculate_done,
        2,
        ITEMS = items,
    )
    
    butcher_done_append_mocked = vampytest.mock_globals(
        butcher_done_append,
        2,
        ITEMS = items,
    )
    
    seed = 261
    multiplier = 2.0
    
    butchered_item = item_2
    butchered_index = 5
    
    butcher_amounts_accumulated, energy_cost_accumulated, butcherables = butcher_calculate_done_mocked(
        item_0, seed, 8, multiplier
    )
    
    vampytest.assert_is_not(butcher_amounts_accumulated, None)
    vampytest.assert_is_not(butcherables, None)
    
    butcher_amounts, energy_cost = butcher_calculate_step(butchered_item, butchered_index, seed, multiplier)
    
    vampytest.assert_is_not(butcher_amounts, None)
    
    output = butcher_done_append_mocked(
        butcher_amounts_accumulated,
        energy_cost_accumulated,
        butcherables,
        butchered_item,
        butchered_index,
        butcher_amounts,
        energy_cost,
    )
    
    expected_output = butcher_calculate_done_mocked(item_0, seed, 8 | (1 << 5), multiplier)
    
    vampytest.assert_eq(output, expected_output)
