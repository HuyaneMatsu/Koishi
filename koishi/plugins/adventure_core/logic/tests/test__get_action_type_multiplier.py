import vampytest

from math import log

from ....user_stats_core import user_stats_create, user_stats_calculate

from ...action import (
    ACTION_TYPE_BUTCHERING, ACTION_TYPE_ENCOUNTER, ACTION_TYPE_FISHING, ACTION_TYPE_FORAGING, ACTION_TYPE_GARDENING,
    ACTION_TYPE_HUNT, ACTION_TYPE_TRAP
)

from ..helpers import get_action_type_multiplier


def _iter_options():
    user_stats = user_stats_create(
        202507300000,
    )
    user_stats_calculate(user_stats).extra_gardening = 100
    
    yield (
        ACTION_TYPE_GARDENING,
        user_stats,
        log(100) / 2.302585092994046,
    )
    
    user_stats = user_stats_create(
        202507300001,
    )
    user_stats_calculate(user_stats).extra_foraging = 100
    
    yield (
        ACTION_TYPE_FORAGING,
        user_stats,
        log(100) / 2.302585092994046,
    )
    
    user_stats = user_stats_create(
        202507300003,
    )
    user_stats_calculate(user_stats).extra_butchering = 100
    
    yield (
        ACTION_TYPE_BUTCHERING,
        user_stats,
        log(100) / 2.302585092994046,
    )
    
    user_stats = user_stats_create(
        202507300004,
    )
    user_stats_calculate(user_stats).extra_fishing = 100
    
    yield (
        ACTION_TYPE_FISHING,
        user_stats,
        log(100) / 2.302585092994046,
    )
    
    user_stats = user_stats_create(
        202507300005,
    )
    
    yield (
        ACTION_TYPE_ENCOUNTER,
        user_stats,
        log(10) / 2.302585092994046,
    )
    
    user_stats = user_stats_create(
        202507300006,
    )
    user_stats_calculate(user_stats).extra_hunting = 100
    
    yield (
        ACTION_TYPE_HUNT,
        user_stats,
        log(100) / 2.302585092994046,
    )
    
    user_stats = user_stats_create(
        202508130000,
    )
    user_stats_calculate(user_stats).extra_movement = 1000
    
    yield (
        ACTION_TYPE_TRAP,
        user_stats,
        log(12) / 2.302585092994046,
    )
    
    user_stats = user_stats_create(
        202507300007,
    )
    
    yield (
        9999,
        user_stats,
        log(10) / 2.302585092994046,
    )
    
    
    # Value at 1
    user_stats = user_stats_create(
        202512270000,
    )
    user_stats_calculate(user_stats).extra_hunting = 1
    
    yield (
        ACTION_TYPE_HUNT,
        user_stats,
        0.15,
    )
    
    # Value at 0
    user_stats = user_stats_create(
        202512270000,
    )
    user_stats_calculate(user_stats).extra_hunting = 0
    
    yield (
        ACTION_TYPE_HUNT,
        user_stats,
        0.05,
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
