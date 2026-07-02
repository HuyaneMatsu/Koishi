from random import Random

import vampytest

from ..logic_butcher import get_option_amount
from ..option_butcher import OptionButcher


def _iter_options():
    yield (
        OptionButcher(True, 1, 1, 100, 8, 10, 11, 13),
        Random(56),
        1.0,
        100,
    )
    
    yield (
        OptionButcher(True, 1, 1, 100, 8, 10, 11, 13),
        Random(56),
        5.0,
        100,
    )
    
    yield (
        OptionButcher(True, 1, 10, 100, 8, 10, 11, 13),
        Random(56),
        1.0,
        19,
    )
    
    yield (
        OptionButcher(True, 1, 2, 100, 8, 10, 11, 13),
        Random(56),
        5.0,
        100,
    )
    
    yield (
        OptionButcher(True, 1, 10, 100, 8, 10, 11, 13),
        Random(18),
        1.0,
        6,
    )
    
    yield (
        OptionButcher(True, 1, 10, 100, 8, 10, 11, 13),
        Random(18),
        5.0,
        30,
    )
    
    yield (
        OptionButcher(False, 1, 10, 100, 8, 10, 11, 13),
        Random(18),
        5.0,
        6,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_option_amount(option, random, multiplier):
    """
    Tests whether ``get_option_amount`` works as intended.
    
    Parameters
    ----------
    options : ``tuple<OptionButcher>``
        Options for butchering.
    
    random : `random.Random`
        Random number generator to use.
    
    multiplier : `float`
        Chance multiplier of the user.
    
    Returns
    -------
    output : `int`
    """
    output = get_option_amount(option, random, multiplier)
    vampytest.assert_instance(output, int)
    return output
