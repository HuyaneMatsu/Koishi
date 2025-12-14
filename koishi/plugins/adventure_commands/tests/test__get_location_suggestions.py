import vampytest

from ...adventure_core import (
    LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATION_ID_HUMAN_VILLAGE_VINEYARDS, LOCATION_ID_MORIYA_SHRINE, LOCATIONS,
    LOCATIONS_ALLOWED
)
from ..location_suggesting import get_location_suggestions


def _iter_options():
    yield (
        None,
        0,
        [
            (location.name, format(location.id, 'x'))
            for location in LOCATIONS_ALLOWED[:25] if location.level <= 0
        ],
    )
    
    yield (
        'potato',
        0,
        [],
    )
    
    yield (
        format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x'),
        0,
        [
            (LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name, format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x')),
        ],
    )
    
    yield (
        'village',
        0,
        [
            (LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name, format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x')),
            (LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_VINEYARDS].name, format(LOCATION_ID_HUMAN_VILLAGE_VINEYARDS, 'x')),
        ],
    )
    
    # Reject higher level locations
    yield (
        format(LOCATION_ID_MORIYA_SHRINE, 'x'),
        0,
        [],
    )
    
    yield (
        'moriya',
        0,
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_location_suggestions(value, user_level):
    """
    Tests whether ``get_location_suggestions`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to test with.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    output : `list<(str, str)>`
    """
    output = get_location_suggestions(value, user_level)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 2)
        vampytest.assert_instance(element[0], str)
        vampytest.assert_instance(element[1], str)
    return output
