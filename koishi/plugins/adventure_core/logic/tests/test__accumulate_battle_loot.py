import vampytest

from ...options import OptionBattle, OptionLoot

from ..loot_accumulation import LootAccumulation
from ..loot_accumulation_logic import accumulate_battle_loot


def _iter_options():
    # no loot
    yield (
        None,
        ((255 << 42) | (123 << 0)),
        (
            ((255 << 42) | (123 << 0)),
            {},
        ),
    )
    
    # 1 battle that is always selected (x2 enemy), but no loot -> duration stays, seed changes
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
        ((255 << 42) | (123 << 0)),
        (
            ((255 << 0) | (123 << 22)),
            {},
        ),
    )
    
    # 1 battle that is always selected (x2 enemy), with always loot -> duration changes, seed changes x3
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
        ((255 << 42) | (123 << 0)),
        (
            ((255 << 44) | (123 << 2)),
            {
                9999 : LootAccumulation(37, 940, 94)
            },
        ),
    )
    
    # 1 battle that is never selected -> duration stays, seed changes
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
        ((255 << 42) | (123 << 0)),
        (
            ((255 << 0) | (123 << 22)),
            {},
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_battle_loot(loot, seed):
    """
    tests whether ``accumulate_battle_loot`` works as intended.
    
    Parameters
    ----------
    loot : ``None | tuple<OptionBattle>``
        Loot options.
    
    seed : `int`
        Seed used for randomization.
    
    Returns
    -------
    output : ``(int, dict<int, LootAccumulation>)``
    """
    accumulations = {}
    seed = accumulate_battle_loot(loot, accumulations, seed)
    vampytest.assert_instance(seed, int)
    return seed, accumulations
