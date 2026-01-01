import vampytest

from random import Random

from ...options import OptionLoot

from ..loot_accumulation import LootAccumulation
from ..loot_accumulation_logic import accumulate_loot_loot


def _iter_options():
    # no loot
    yield (
        None,
        Random(255),
        1.0,
        {},
    )
    
    # 1 loot with hit -> increase duration
    yield (
        (
            OptionLoot(False, 1, 1, False, 10, 20, 9999, 100, 20, 10, 2),
        ),
        Random(23),
        1.0,
        {
            9999 : LootAccumulation(19, 480, 48)
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_loot_loot(loot, random, multiplier):
    """
    tests whether ``accumulate_loot_loot`` works as intended.
    
    Parameters
    ----------
    loot : ``None | tuple<OptionLoot>``
        Loot options.
    
    random : `random.Random`
        Random number generator to use.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    output : ``dict<int, LootAccumulation>``
    """
    accumulations = {}
    accumulate_loot_loot(loot, accumulations, random, multiplier)
    return accumulations
