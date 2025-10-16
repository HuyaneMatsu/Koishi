import vampytest

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
        255,
        12,
    )
    
    # 90% chance miss
    yield (
        OptionBase(
            9,
            10,
            10,
            20,
        ),
        209,
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
        201,
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
        116,
        16,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_option_amount(option, seed):
    """
    tests whether ``get_option_amount`` works as intended.
    
    Parameters
    ----------
    option : ``OptionBase``
        Option to use.
    
    seed : `int`
        Seed used for randomization.
    
    Returns
    -------
    output : `int`
    """
    output = get_option_amount(option, seed)
    vampytest.assert_instance(output, int)
    return output
