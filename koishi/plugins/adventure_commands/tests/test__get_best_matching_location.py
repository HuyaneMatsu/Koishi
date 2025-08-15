import vampytest

from ...adventure_core import LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATIONS, Location

from ..location_suggesting import get_best_matching_location


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        'potato',
        None,
    )
    
    yield (
        format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x'),
        LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
    )
    
    yield (
        'village',
        LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_best_matching_location(value):
    """
    Tests whether ``get_best_matching_location`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : ``None | Location``
    """
    output = get_best_matching_location(value)
    vampytest.assert_instance(output, Location, nullable = True)
    return output
    
