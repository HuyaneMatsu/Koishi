import vampytest

from ....user_stats_core import UserStats

from ...adventure import Adventure
from ...location import Location

from ..helpers import get_location_distance_travel_duration


def _iter_options():
    user_id_0 = 202507250000
    location_id = 9999
    
    adventure_0 = Adventure(
        user_id_0,
        location_id,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    
    user_stats_0 = UserStats(
        user_id_0,
    )
    # If the user has every of its stats as 10, they should move 1.2 m / s
    user_stats_0.stat_housewife = 10
    user_stats_0.stat_cuteness = 10
    user_stats_0.stat_bedroom = 10
    user_stats_0.stat_charm = 10
    user_stats_0.stat_loyalty = 10
    
    # Set distance to 1200 meters, like this, it will take us 1000 seconds to complete it.
    location = Location(
        location_id,
        'Pudding land',
        1_200,
        (),
        0,
    )
    
    yield (
        adventure_0,
        user_stats_0,
        {
            location_id : location,
        },
        1000,
    )
    
    # If the location is not found, we take a default distance.
    yield (
        adventure_0,
        user_stats_0,
        {},
        833,
    )
    
    user_id_1 = 202512270001
    
    adventure_1 = Adventure(
        user_id_1,
        location_id,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    
    user_stats_1 = UserStats(
        user_id_1,
    )
    stats_calculated = user_stats_1.stats_calculated
    stats_calculated.extra_movement = 0
    
    # Movement at 0
    yield (
        adventure_1,
        user_stats_1,
        {
            location_id : location,
        },
        12_000_000,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_location_distance_travel_duration(adventure, user_stats, locations):
    """
    tests whether ``get_location_distance_travel_duration`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to update.
    
    user_stats : ``UserStats``
        The user's stats.
    
    locations : ``dict<int, Location>``
        The locations to patch the function with.
    
    Returns
    -------
    output : `int`
    """
    patched = vampytest.mock_globals(
        get_location_distance_travel_duration,
        LOCATIONS = locations,
    )
    output = patched(adventure, user_stats)
    vampytest.assert_instance(output, int)
    return output
