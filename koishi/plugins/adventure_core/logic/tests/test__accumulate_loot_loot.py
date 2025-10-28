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
        {},
    )
    
    # 1 loot with hit -> increase duration
    yield (
        (
            OptionLoot(1, 1, 10, 20, 9999, 100, 20, 10, 2),
        ),
        Random(23),
        {
            9999 : LootAccumulation(20, 500, 50)
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_loot_loot(loot, random):
    """
    tests whether ``accumulate_loot_loot`` works as intended.
    
    Parameters
    ----------
    loot : ``None | tuple<OptionLoot>``
        Loot options.
    
    random : `random.Random`
        Random number generator to use.
    
    Returns
    -------
    output : ``dict<int, LootAccumulation>``
    """
    accumulations = {}
    accumulate_loot_loot(loot, accumulations, random)
    return accumulations
