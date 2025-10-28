import vampytest

from random import Random

from ...options import OptionBase

from ..loot_accumulation_logic import get_option_amount


def _iter_options():
    # 100% chance hit
    yield (
        OptionBase(
            1,
            1,
            10,
            20,
        ),
        Random(255),
        10,
    )
    
    # 90% chance miss
    yield (
        OptionBase(
            9,
            10,
            10,
            20,
        ),
        Random(23),
        0,
    )
    
    # 50% chance, miss.
    yield (
        OptionBase(
            1,
            2,
            10,
            20,
        ),
        Random(48),
        0,
    )
    
    # 50% chance, hit
    yield (
        OptionBase(
            1,
            2,
            10,
            20,
        ),
        Random(49),
        14,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_option_amount(option, Random):
    """
    tests whether ``get_option_amount`` works as intended.
    
    Parameters
    ----------
    option : ``OptionBase``
        Option to use.
    
    random : `random.Random`
        Random number generator to use.
    
    Returns
    -------
    output : `int`
    """
    output = get_option_amount(option, Random)
    vampytest.assert_instance(output, int)
    return output
