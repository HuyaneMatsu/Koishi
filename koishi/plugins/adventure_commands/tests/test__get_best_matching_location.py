import vampytest

from ...adventure_core import LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, LOCATION_ID_MORIYA_SHRINE, LOCATIONS, Location

from ..location_suggesting import get_best_matching_location


def _iter_options():
    yield (
        None,
        0,
        None,
    )
    
    yield (
        'potato',
        0,
        None,
    )
    
    yield (
        format(LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS, 'x'),
        0,
        LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
    )
    
    yield (
        'village',
        0,
        LOCATIONS[LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS],
    )
    
    # Reject higher level locations
    yield (
        format(LOCATION_ID_MORIYA_SHRINE, 'x'),
        0,
        None,
    )
    
    yield (
        'moriya',
        0,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_best_matching_location(value, user_level):
    """
    Tests whether ``get_best_matching_location`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to test with.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    output : ``None | Location``
    """
    output = get_best_matching_location(value, user_level)
    vampytest.assert_instance(output, Location, nullable = True)
    return output
