import vampytest

from ...adventure_core import (
    LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATION_ID_HUMAN_VILLAGE_VINEYARDS, LOCATION_ID_MORIYA_SHRINE, LOCATIONS,
    LOCATIONS_ALLOWED, Location
)

from ..location_suggesting import get_matching_locations


def _iter_options():
    yield (
        None,
        0,
        [location for location in LOCATIONS_ALLOWED if location.level <= 0],
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
            LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
        ],
    )
    
    yield (
        'village',
        0,
        [
            LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
            LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_VINEYARDS],
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
def test__get_matching_locations(value, user_level):
    """
    Tests whether ``get_matching_locations`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to test with.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    output : ``list<Location>``
    """
    output = get_matching_locations(value, user_level)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Location)
    return output
