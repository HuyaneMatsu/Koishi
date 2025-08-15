import vampytest

from ...adventure import Adventure
from ...constants import (
    RECOVERY_DURATION_BY_LOST_ENERGY, RECOVERY_DURATION_BY_LOST_HEALTH, RECOVERY_DURATION_MULTIPLIER_FATALITY
)
from ..helpers import get_duration_till_recovery_end


def _iter_options():
    adventure = Adventure(
        202508030004,
        0,
        0,
        0,
        0,
        0,
        200,
        200,
    )
    
    yield (adventure, 0)
    
    adventure = Adventure(
        202508030005,
        0,
        0,
        0,
        0,
        0,
        200,
        200,
    )
    adventure.energy_exhausted = 100
    
    yield (adventure, 100 * RECOVERY_DURATION_BY_LOST_ENERGY)
    
    adventure = Adventure(
        202508030006,
        0,
        0,
        0,
        0,
        0,
        200,
        200,
    )
    adventure.health_exhausted = 100
    
    yield (adventure, 100 * RECOVERY_DURATION_BY_LOST_HEALTH)
    
    
    adventure = Adventure(
        202508030006,
        0,
        0,
        0,
        0,
        0,
        200,
        200,
    )
    adventure.health_exhausted = 100
    adventure.energy_exhausted = 66
    
    yield (adventure, 100 * RECOVERY_DURATION_BY_LOST_HEALTH + 66 * RECOVERY_DURATION_BY_LOST_ENERGY)
    
    
    adventure = Adventure(
        202508030007,
        0,
        0,
        0,
        0,
        0,
        90,
        200,
    )
    adventure.health_exhausted = 100
    
    yield (adventure, 100 * RECOVERY_DURATION_BY_LOST_HEALTH * RECOVERY_DURATION_MULTIPLIER_FATALITY)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_duration_till_recovery_end(adventure):
    """
    Tests whether ``get_duration_till_recovery_end`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user finished.
    
    Returns
    -------
    output : `int`
    """
    output = get_duration_till_recovery_end(adventure)
    vampytest.assert_instance(output, int)
    return output
