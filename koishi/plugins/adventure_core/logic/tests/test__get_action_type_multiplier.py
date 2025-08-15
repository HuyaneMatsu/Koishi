import vampytest

from math import log

from ....user_stats_core import UserStats

from ...action import (
    ACTION_TYPE_BUTCHERING, ACTION_TYPE_ENCOUNTER, ACTION_TYPE_FISHING, ACTION_TYPE_FORAGING, ACTION_TYPE_GARDENING,
    ACTION_TYPE_HUNT, ACTION_TYPE_TRAP
)

from ..helpers import get_action_type_multiplier


def _iter_options():
    user_stats = UserStats(
        202507300000,
    )
    user_stats.stats_calculated.extra_gardening = 100
    
    yield (
        ACTION_TYPE_GARDENING,
        user_stats,
        log(100) / 2.302585092994046
    )
    
    user_stats = UserStats(
        202507300001,
    )
    user_stats.stats_calculated.extra_foraging = 100
    
    yield (
        ACTION_TYPE_FORAGING,
        user_stats,
        log(100) / 2.302585092994046
    )
    
    user_stats = UserStats(
        202507300003,
    )
    user_stats.stats_calculated.extra_butchering = 100
    
    yield (
        ACTION_TYPE_BUTCHERING,
        user_stats,
        log(100) / 2.302585092994046
    )
    
    user_stats = UserStats(
        202507300004,
    )
    user_stats.stats_calculated.extra_fishing = 100
    
    yield (
        ACTION_TYPE_FISHING,
        user_stats,
        log(100) / 2.302585092994046
    )
    
    user_stats = UserStats(
        202507300005,
    )
    
    yield (
        ACTION_TYPE_ENCOUNTER,
        user_stats,
        log(10) / 2.302585092994046
    )
    
    user_stats = UserStats(
        202507300006,
    )
    user_stats.stats_calculated.extra_hunting = 100
    
    yield (
        ACTION_TYPE_HUNT,
        user_stats,
        log(100) / 2.302585092994046
    )
    
    user_stats = UserStats(
        202508130000,
    )
    user_stats.stats_calculated.extra_movement = 1000
    
    yield (
        ACTION_TYPE_TRAP,
        user_stats,
        log(12) / 2.302585092994046
    )
    
    user_stats = UserStats(
        202507300007,
    )
    
    yield (
        9999,
        user_stats,
        log(10) / 2.302585092994046
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_action_type_multiplier(action_type, user_stats):
    """
    Gets multiplier for the given action type.
    
    Parameters
    ----------
    action_type : `int`
        The action's type.
    
    user_stats : ``UserStats``
        The user's stats.
    
    Returns
    -------
    output : `float`
    """
    output = get_action_type_multiplier(action_type, user_stats)
    vampytest.assert_instance(output, float)
    return output
