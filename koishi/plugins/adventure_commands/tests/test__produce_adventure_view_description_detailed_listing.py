import vampytest

from ...adventure_core import (
    ADVENTURE_STATE_ACTIONING, ADVENTURE_STATE_FINALISED, AUTO_CANCELLATION_ID_DEFAULT, RETURN_ID_BEFORE,
    adventure_create, goal_create_item_exact
)
from ...item_core import ITEM_ID_PEACH, get_item_nullable
from ...unit_core import AMOUNT_TYPE_COUNT

from ..content_building import produce_adventure_view_description_detailed_listing


def _iter_options():
    item_peach = get_item_nullable(ITEM_ID_PEACH)
    assert item_peach is not None
    
    adventure = adventure_create(
        202609270000,
        0,
        0,
        RETURN_ID_BEFORE,
        0,
        None,
        6 * 3600,
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
            '- Departed at\n'
            '  - 2016-05-14 00:00:00 UTC\n'
            '- Used health\n'
            '  - 20 / 130\n'
            '- Used energy\n'
            '  - 30 / 140\n'
            '- Used inventory\n'
            '  - 20 / 45 kg\n'
            '- Elapsed time\n'
            '  - 5 hours, 30 minutes\n'
            '- Adventure settings\n'
            '  - Duration\n'
            '    - 6 hours, return before\n'
            'You are currently working on your target task.'
        ),
    )
    
    
    adventure = adventure_create(
        202609270001,
        0,
        0,
        RETURN_ID_BEFORE,
        AUTO_CANCELLATION_ID_DEFAULT,
        [goal_create_item_exact(item_peach.id, AMOUNT_TYPE_COUNT, 5)],
        6 * 3600,
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
        RETURN_ID_BEFORE,
        0,
        (
            f'- Departed at\n'
            f'  - 2016-05-14 00:00:00 UTC\n'
            f'- Used health\n'
            f'  - 20 / 130\n'
            f'- Used energy\n'
            f'  - 30 / 140\n'
            f'- Total duration\n'
            f'  - 5 hours, 30 minutes\n'
            f'- Recovery time\n'
            f'  - 6 hours, 20 minutes\n'
            f'- Adventure settings\n'
            f'  - Duration\n'
            f'    - 6 hours, return before\n'
            f'  - Auto cancellation\n'
            f'    - name: Default\n'
            f'    - inventory < 1 kg\n'
            f'    - health <= 50\n'
            f'    - energy <= 20 %\n'
            f'  - Goal\n'
            f'    - 5 {item_peach.emoji} {item_peach.name}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_adventure_view_description_detailed_listing(adventure, inventory_total, inventory_exhausted, now):
    """
    Tests whether ``produce_adventure_view_description_detailed_listing`` works as intended.
    
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
        produce_adventure_view_description_detailed_listing,
        unix_time_seconds_get = unix_time_seconds_get_patched,
    )
    
    output = [*mocked(adventure, inventory_total, inventory_exhausted)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
