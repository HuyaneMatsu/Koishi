import vampytest

from ...adventure_core import (
    LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATION_ID_HUMAN_VILLAGE_VINEYARDS, LOCATIONS, LOCATIONS_ALLOWED, Location
)

from ..location_suggesting import get_matching_locations


def _iter_options():
    yield (
        None,
        [*LOCATIONS_ALLOWED],
    )
    
    yield (
        'potato',
        [],
    )
    
    yield (
        format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x'),
        [
            LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
        ],
    )
    
    yield (
        'village',
        [
            LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
            LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_VINEYARDS],
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_matching_locations(value):
    """
    Tests whether ``get_matching_locations`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : ``list<Location>``
    """
    output = get_matching_locations(value)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Location)
    return output
