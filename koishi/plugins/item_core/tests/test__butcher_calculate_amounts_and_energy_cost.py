from random import Random

import vampytest

from ..logic_butcher import butcher_calculate_amounts_and_energy_cost
from ..option_butcher import OptionButcher


def _iter_options():
    item_id_0 = 10
    item_id_1 = 12
    item_id_2 = 14
    
    yield (
        '1 % chance, scaling, single option; no multiplier',
        (
            OptionButcher(True, 1, 100, 1, item_id_0, 10, 11, 13),
        ),
        Random(18),
        1.0,
        (
            None,
            23,
        ),
    )
    
    yield (
        '100 % chance, scaling, single option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
        ),
        Random(18),
        1.0,
        (
            [
                (item_id_0, 100),
            ],
            1110,
        ),
    )
    
    yield (
        '50 % chance, scaling, single option; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        Random(18),
        1.0,
        (
            [
                (item_id_0, 30),
            ],
            1250,
        )
    )
    
    yield (
        '100 % chance, scaling, single option; with multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
        ),
        Random(18),
        1.5,
        (
            [
                (item_id_0, 100),
            ],
            740,
        ),
    )
    
    yield (
        '50 % chance, scaling, single option; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        Random(18),
        1.5,
        (
            [
                (item_id_0, 45),
            ],
            814,
        ),
    )
    
    yield (
        '50 % chance, scaling, single option; with over multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        Random(18),
        3.0,
        (
            [
                (item_id_0, 89),
            ],
            378,
        ),
    )
    
    yield (
        '50 % chance, no scaling, single option; with multiplier',
        (
            OptionButcher(False, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        Random(18),
        1.5,
        (
            [
                (item_id_0, 30),
            ],
            834,
        ),
    )
    
    yield (
        '100 % chance, scaling, multiple option, same item; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 1, 300, item_id_0, 8, 13, 15),
        ),
        Random(18),
        1.0,
        (
            [
                (item_id_0, 600),
            ],
            7427,
        ),
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        Random(18),
        1.0,
        (
            [
                (item_id_0, 169),
            ],
            8289,
        ),
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        Random(18),
        1.5,
        (
            [
                (item_id_0, 209),
            ],
            5473,
        ),
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; with over multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        Random(18),
        3.0,
        (
            [
                (item_id_0, 355),
            ],
            2639,
        ),
    )
    
    yield (
        '100 % chance, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 1, 60, item_id_2, 8, 13, 15),
        ),
        Random(18),
        1.0,
        (
            [
                (item_id_0, 100),
                (item_id_1, 80),
                (item_id_2, 60),
            ],
            2867,
        ),
    )
    
    yield (
        '100 % chance, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 1, 60, item_id_2, 8, 13, 15),
        ),
        Random(18),
        1.0,
        (
            [
                (item_id_0, 100),
                (item_id_1, 80),
                (item_id_2, 60),
            ],
            2867,
        ),
    )
    
    yield (
        'Different % chances, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 8, 60, item_id_2, 8, 13, 15),
        ),
        Random(18),
        1.0,
        (
            [
                (item_id_0, 50),
                (item_id_1, 36),
                (item_id_2, 4),
            ],
            3167,
        ),
    )
    
    yield (
        'Different % chances, scaling, multiple option, same repeated; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 8, 50, item_id_0, 8, 13, 15),
        ),
        Random(18),
        1.5,
        (
            [
                (item_id_0, 81),
                (item_id_1, 36),
            ],
            1976,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__butcher_calculate_amounts_and_energy_cost(butcher_options, random, multiplier):
    """
    Tests whether ``butcher_calculate_amounts_and_energy_cost`` works as intended.
    
    Parameters
    ----------
    butcher_options : ``tuple<OptionButcher>``
        Options for butchering.
    
    random : `random.Random`
        Random number generator to use.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    output : `None | (list<(int, int)>, int)`
    """
    output = butcher_calculate_amounts_and_energy_cost(butcher_options, random, multiplier)
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
