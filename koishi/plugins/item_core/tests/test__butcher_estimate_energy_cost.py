import vampytest

from ..logic_butcher import butcher_estimate_energy_cost
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
        1310,
    )
    
    yield (
        '50 % chance, scaling, single option; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        1.0,
        1310,
    )
    
    yield (
        '100 % chance, scaling, single option; with multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
        ),
        1.5,
        874,
    )
    
    yield (
        '50 % chance, scaling, single option; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        1.5,
        874,
    )
    
    yield (
        '50 % chance, scaling, single option; with over multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        3.0,
        437,
    )
    
    yield (
        '50 % chance, no scaling, single option; with multiplier',
        (
            OptionButcher(False, 1, 2, 100, item_id_0, 10, 11, 13),
        ),
        1.5,
        874,
    )
    
    yield (
        '100 % chance, scaling, multiple option, same item; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 1, 300, item_id_0, 8, 13, 15),
        ),
        1.0,
        8627,
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        1.0,
        8627,
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        1.5,
        5752,
    )
    
    yield (
        'mixed chance, scaling, multiple option, same item; with over multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 200, item_id_0, 9, 12, 14),
            OptionButcher(True, 1, 6, 300, item_id_0, 8, 13, 15),
        ),
        3.0,
        2876,
    )
    
    yield (
        '100 % chance, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 1, 60, item_id_2, 8, 13, 15),
        ),
        1.0,
        3347,
    )
    
    yield (
        '100 % chance, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 1, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 1, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 1, 60, item_id_2, 8, 13, 15),
        ),
        1.0,
        3347,
    )
    
    yield (
        'Different % chances, scaling, multiple option; no multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 8, 60, item_id_2, 8, 13, 15),
        ),
        1.0,
        3347,
    )
    
    yield (
        'Different % chances, scaling, multiple option, same repeated; with multiplier',
        (
            OptionButcher(True, 1, 2, 100, item_id_0, 10, 11, 13),
            OptionButcher(True, 1, 4, 80, item_id_1, 9, 12, 14),
            OptionButcher(True, 1, 8, 50, item_id_0, 8, 13, 15),
        ),
        1.5,
        2132,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__butcher_estimate_energy_cost(options, multiplier):
    """
    Tests whether ``butcher_estimate_energy_cost`` works as intended.
    
    Parameters
    ----------
    options : ``None | tuple<OptionButcher>``
        Options for butchering.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    output : `int`
    """
    output = butcher_estimate_energy_cost(options, multiplier)
    vampytest.assert_instance(output, int)
    return output
