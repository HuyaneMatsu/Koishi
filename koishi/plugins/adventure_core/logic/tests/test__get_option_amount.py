import vampytest

from random import Random

from ...options import OptionBase

from ..loot_accumulation_logic import get_option_amount


def _iter_options():
    yield (
        '100% chance hit',
        OptionBase(
            False,
            1,
            1,
            False,
            10,
            20,
        ),
        Random(255),
        2.0,
        11,
    )
    
    yield (
        '100% chance hit with multiplier',
        OptionBase(
            False,
            1,
            1,
            True,
            10,
            20,
        ),
        Random(255),
        2.0,
        21,
    )
    
    yield (
        '90% chance miss',
        OptionBase(
            False,
            9,
            10,
            False,
            10,
            20,
        ),
        Random(22),
        2.0,
        0,
    )
    
    yield (
        '50% chance, miss.',
        OptionBase(
            False,
            1,
            2,
            False,
            10,
            20,
        ),
        Random(48),
        2.0,
        0,
    )
    
    yield (
        '50% chance, hit due to multiplier.',
        OptionBase(
            True,
            1,
            2,
            False,
            10,
            20,
        ),
        Random(48),
        2.0,
        11,
    )
    
    yield (
        '50% chance, hit',
        OptionBase(
            False,
            1,
            2,
            False,
            10,
            20,
        ),
        Random(49),
        2.0,
        14,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__get_option_amount(option, random, multiplier):
    """
    tests whether ``get_option_amount`` works as intended.
    
    Parameters
    ----------
    option : ``OptionBase``
        Option to use.
    
    random : `random.Random`
        Random number generator to use.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    output : `int`
    """
    output = get_option_amount(option, random, multiplier)
    vampytest.assert_instance(output, int)
    return output
