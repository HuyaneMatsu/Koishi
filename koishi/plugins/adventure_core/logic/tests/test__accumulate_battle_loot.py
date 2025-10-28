from random import Random

import vampytest

from ...options import OptionBattle, OptionLoot

from ..loot_accumulation import LootAccumulation
from ..loot_accumulation_logic import accumulate_battle_loot


def _iter_options():
    # no loot
    yield (
        None,
        Random(255),
        {},
    )
    
    # 1 battle that is always selected (x2 enemy), but no loot -> duration stays
    yield (
        (
            OptionBattle(
                1,
                1,
                1,
                2,
                999,
                None,
            ),
        ),
        Random(23),
        {},
    )
    
    # 1 battle that is always selected (x2 enemy), with always loot -> duration changes
    
    yield (
        (
            OptionBattle(
                1,
                1,
                1,
                2,
                999,
                (
                    OptionLoot(1, 1, 10, 20, 9999, 100, 20, 10, 2),
                ),
            ),
        ),
        Random(27),
        {
            9999 : LootAccumulation(37, 940, 94)
        },
    )

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_battle_loot(loot, random):
    """
    tests whether ``accumulate_battle_loot`` works as intended.
    
    Parameters
    ----------
    loot : ``None | tuple<OptionBattle>``
        Loot options.
    
    random : `random.Random`
        Random number generator to use.
    
    Returns
    -------
    output : ``dict<int, LootAccumulation>``
    """
    accumulations = {}
    accumulate_battle_loot(loot, accumulations, random)
    return accumulations
