import vampytest

from ...options import OptionBase

from ..loot_accumulation_logic import get_option_amount


def _iter_options():
    # If seed is 255, we can loot only if loot chance is 100%, or 1.0.
    yield (
        OptionBase(
            1.0,
            10,
            20,
        ),
        255,
        12,
    )
    
    # 255 seed, with not 100% chance, loot none.
    yield (
        OptionBase(
            0.9,
            10,
            20,
        ),
        255,
        0,
    )
    
    # Use 200 for seed to skip the loot (with 50% chance)
    yield (
        OptionBase(
            0.5,
            10,
            20,
        ),
        200,
        0,
    )
    
    # Use 105 for seed to loot (with 50% chance)
    yield (
        OptionBase(
            0.5,
            10,
            20,
        ),
        115,
        15,
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
