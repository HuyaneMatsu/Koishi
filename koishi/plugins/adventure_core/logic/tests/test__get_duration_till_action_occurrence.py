from random import Random

import vampytest

from ..helpers import get_duration_till_action_occurrence
from ..loot_accumulation import LootAccumulation

def _iter_options():
    yield (
        1000,
        Random(188),
        {
            9999: LootAccumulation(16, 420, 42),
        },
        1.25,
        1452,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_duration_till_action_occurrence(base_duration, random, loot_accumulations, multiplier):
    """
    Tests whether ``get_duration_till_action_occurrence`` works as intended.
    
    Parameters
    ----------
    base_duration : `int`
        The action's base duration.
    
    random : `random.Random`
        Random number generator to use.
    
    loot_accumulations : ``dict<int, LootAccumulation>``
        Accumulated loot from the action.
    
    multiplier : `float`
        Multiplier of the user for this given action.
    
    Returns
    -------
    output : `int`
    """
    output = get_duration_till_action_occurrence(base_duration, random, loot_accumulations, multiplier)
    vampytest.assert_instance(output, int)
    return output
