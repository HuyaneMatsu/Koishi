import vampytest

from ...options import OptionLoot

from ..loot_accumulation import LootAccumulation
from ..loot_accumulation_logic import accumulate_loot_loot


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
    
    # 1 loot with hit -> increase duration & step seed
    yield (
        (
            OptionLoot(1, 1, 10, 20, 9999, 100, 20, 10, 2),
        ),
        ((255 << 42) | (123 << 0)),
        (
            ((255 << 0) | (123 << 22)),
            {
                9999 : LootAccumulation(20, 500, 50)
            },
        ),
    )
    
    # 1 loot with miss -> duration stay, step seed
    yield (
        (
            OptionLoot(0, 1, 10, 20, 9999, 100, 20, 10, 2),
        ),
        ((255 << 42) | (123 << 0)),
        (
            ((255 << 0) | (123 << 22)),
            {},
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__accumulate_loot_loot(loot, seed):
    """
    tests whether ``accumulate_loot_loot`` works as intended.
    
    Parameters
    ----------
    loot : ``None | tuple<OptionLoot>``
        Loot options.
    
    seed : `int`
        Seed used for randomization.
    
    Returns
    -------
    output : ``(int, dict<int, LootAccumulation>)``
    """
    accumulations = {}
    seed = accumulate_loot_loot(loot, accumulations, seed)
    vampytest.assert_instance(seed, int)
    return seed, accumulations
