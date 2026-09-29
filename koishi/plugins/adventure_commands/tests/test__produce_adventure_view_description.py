import vampytest

from ...adventure_core import ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_FINALISED, adventure_create

from ..content_building import produce_adventure_view_description


def _iter_options():
    adventure = adventure_create(
        202508030002,
        0,
        0,
        0,
        0,
        None,
        0,
        130,
        140,
    )
    adventure.created_at = 1463184000
    adventure.health_exhausted = 20
    adventure.energy_exhausted = 30
    adventure.state = ADVENTURE_STATE_ACTIONING
    
    yield (
        adventure,
        45000,
        20000,
        1463184000 + 5 * 3600 + 30 * 60,
        (
            'Departed at: 2016-05-14 00:00:00 UTC\n'
            'Used health: 20 / 130\n'
            'Used energy: 30 / 140\n'
            'Used inventory: 20 / 45 kg\n'
            'Elapsed time: 5 hours, 30 minutes\n'
            'You are currently working on your target task.'
        ),
    )
    
    
    adventure = adventure_create(
        202508030003,
        0,
        0,
        0,
        0,
        None,
        0,
        130,
        140,
    )
    adventure.created_at = 1463184000
    adventure.updated_at = 1463184000 + 5 * 3600 + 30 * 60
    adventure.health_exhausted = 20
    adventure.energy_exhausted = 30
    adventure.state = ADVENTURE_STATE_FINALISED
    
    yield (
        adventure,
        0,
        0,
        0,
        (
            'Departed at: 2016-05-14 00:00:00 UTC\n'
            'Used health: 20 / 130\n'
            'Used energy: 30 / 140\n'
            'Total duration: 5 hours, 30 minutes\n'
            'Recovery time: 6 hours, 20 minutes'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_view_description(adventure, inventory_total, inventory_exhausted, now):
    """
    Tests whether ``produce_adventure_view_description`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure to produce description for.
    
    inventory_total : `int`
        The user's total inventory.
    
    inventory_exhausted : `int`
        The user's used inventory.
    
    now : `int`
        The current time.
    
    Returns
    -------
    output : `str`
    """
    def unix_time_seconds_get_patched():
        nonlocal now
        return now
    
    mocked = vampytest.mock_globals(
        produce_adventure_view_description,
        unix_time_seconds_get = unix_time_seconds_get_patched,
    )
    
    output = [*mocked(adventure, inventory_total, inventory_exhausted)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
