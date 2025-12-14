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
        1.0,
        {},
    )
    
    # 1 battle that is always selected (x2 enemy), but no loot -> duration stays
    yield (
        (
            OptionBattle(
                False,
                1,
                1,
                True,
                1,
                2,
                999,
                None,
            ),
        ),
        Random(23),
        1.0,
        {},
    )
    
    # 1 battle that is always selected (x2 enemy), with always loot -> duration changes
    
    yield (
        (
            OptionBattle(
                False,
                1,
                1,
                True,
                1,
                2,
                999,
                (
                    OptionLoot(False, 1, 1, False, 10, 20, 9999, 100, 20, 10, 2),
                ),
            ),
        ),
        Random(27),
        1.0,
        {
            9999 : LootAccumulation(37, 940, 94)
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_battle_loot(battle, random, multiplier):
    """
    tests whether ``accumulate_battle_loot`` works as intended.
    
    Parameters
    ----------
    battle : ``None | tuple<OptionBattle>``
        Battle options.
    
    random : `random.Random`
        Random number generator to use.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    output : ``dict<int, LootAccumulation>``
    """
    accumulations = {}
    accumulate_battle_loot(battle, accumulations, random, multiplier)
    return accumulations
