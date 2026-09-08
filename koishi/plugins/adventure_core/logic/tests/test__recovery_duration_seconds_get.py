import vampytest

from ...adventure import adventure_create
from ...constants import (
    RECOVERY_DURATION_BY_LOST_ENERGY, RECOVERY_DURATION_BY_LOST_HEALTH, RECOVERY_DURATION_MULTIPLIER_FATALITY
)
from ..helpers import recovery_duration_seconds_get


def _iter_options():
    adventure = adventure_create(
        202508030004,
        0,
        0,
        0,
        0,
        0,
        200,
        200,
    )
    
    yield (
        adventure,
        0,
    )
    
    adventure = adventure_create(
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
    
    yield (
        adventure,
        (100 * RECOVERY_DURATION_BY_LOST_ENERGY),
    )
    
    adventure = adventure_create(
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
    
    yield (
        adventure,
        (100 * RECOVERY_DURATION_BY_LOST_HEALTH),
    )
    
    
    adventure = adventure_create(
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
    
    yield (
        adventure,
        (100 * RECOVERY_DURATION_BY_LOST_HEALTH + 66 * RECOVERY_DURATION_BY_LOST_ENERGY),
    )
    
    
    adventure = adventure_create(
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
    
    yield (
        adventure,
        (100 * RECOVERY_DURATION_BY_LOST_HEALTH * RECOVERY_DURATION_MULTIPLIER_FATALITY),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__recovery_duration_seconds_get(adventure):
    """
    Tests whether ``recovery_duration_seconds_get`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure the user finished.
    
    Returns
    -------
    output : `int`
    """
    output = recovery_duration_seconds_get(adventure)
    vampytest.assert_instance(output, int)
    return output
