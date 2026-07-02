import vampytest

from ..logic_butcher import butcher_estimate_loot_chance_and_amounts
from ..option_butcher import OptionButcher


def _iter_options():
    item_id_0 = 10
    item_id_1 = 12
    item_id_2 = 14
    
    yield (
        '100 % chance, scaling, single option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
        ),
        1.0,
        [
            (item_id_0, 1.0, 100),
        ],
    )
    
    yield (
        '50 % chance, scaling, single option; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        1.0,
        [
            (item_id_0, 0.5, 100),
        ],
    )
    
    yield (
        '100 % chance, scaling, single option; with multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
        ),
        1.5,
        [
            (item_id_0, 1.0, 100),
        ],
    )
    
    yield (
        '50 % chance, scaling, single option; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        1.5,
        [
            (item_id_0, 0.6666666666666667, 100),
        ],
    )
    
    yield (
        '50 % chance, scaling, single option; with over multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        3.0,
        [
            (item_id_0, 0.8333333333333335, 100),
        ],
    )
    
    yield (
        '50 % chance, no scaling, single option; with multiplier',
        (
            OptionButcher(False, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        1.5,
        [
            (item_id_0, 0.5, 100),
        ],
    )
    
    yield (
        '100 % chance, scaling, multiple option, same item; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 1, 300, item_id_0, 8, 13, 15),
        ),
        1.0,
        [
            (item_id_0, 1.0, 600),
        ],
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        1.0,
        [
            (item_id_0, 0.34722222222222227, 600),
        ],
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        1.5,
        [
            (item_id_0, 0.45486111111111116, 600),
        ],
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; with over multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        3.0,
        [
            (item_id_0, 11.0 / 18.0, 600),
        ],
    )
    
    yield (
        '100 % chance, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 1, 60, item_id_2, 8, 13, 15),
        ),
        1.0,
        [
            (item_id_0, 1.0, 100),
            (item_id_1, 1.0, 80),
            (item_id_2, 1.0, 60),
        ],
    )
    
    yield (
        '100 % chance, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 1, 60, item_id_2, 8, 13, 15),
        ),
        1.0,
        [
            (item_id_0, 1.0, 100),
            (item_id_1, 1.0, 80),
            (item_id_2, 1.0, 60),
        ],
    )
    
    yield (
        'Different % chances, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 8, 60, item_id_2, 8, 13, 15),
        ),
        1.0,
        [
            (item_id_0, 0.5, 100),
            (item_id_1, 3.0 / 8.0, 80),
            (item_id_2, 7.0 / 32.0, 60),
        ],
    )
    
    yield (
        'Different % chances, scaling, multiple option, same repeated; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 8, 50, item_id_0, 8, 13, 15),
        ),
        1.5,
        [
            (10, 0.5460069444444445, 150),
            (12, 15.0 / 32.0, 80),
        ]
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__butcher_estimate_loot_chance_and_amounts(options, multiplier):
    """
    Tests whether ``butcher_estimate_loot_chance_and_amounts`` works as intended.
    
    Parameters
    ----------
    options : ``None | tuple<OptionButcher>``
        Options for butchering.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    output : `list<(int, float, int)>`
    """
    output = butcher_estimate_loot_chance_and_amounts(options, multiplier)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 3)
        item_id, chance, amount = element
        vampytest.assert_instance(item_id, int)
        vampytest.assert_instance(chance, float)
        vampytest.assert_instance(amount, int)
    
    return output
