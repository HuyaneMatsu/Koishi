import vampytest

from ...adventure_core import (
    LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATION_ID_HUMAN_VILLAGE_VINEYARDS, LOCATIONS, LOCATIONS_ALLOWED
)
from ..location_suggesting import get_location_suggestions


def _iter_options():
    yield (
        None,
        [
            (location.name, format(location.id, 'x'))
            for location in LOCATIONS_ALLOWED[:25]
        ],
    )
    
    yield (
        'potato',
        [],
    )
    
    yield (
        format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x'),
        [
            (LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name, format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x')),
        ],
    )
    
    yield (
        'village',
        [
            (LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS].name, format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x')),
            (LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_VINEYARDS].name, format(LOCATION_ID_HUMAN_VILLAGE_VINEYARDS, 'x')),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_location_suggestions(value):
    """
    Tests whether ``get_location_suggestions`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : ``list<(str, str)>``
    """
    output = get_location_suggestions(value)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, tuple)
        vampytest.assert_eq(len(element), 2)
        vampytest.assert_instance(element[0], str)
        vampytest.assert_instance(element[1], str)
    return output
