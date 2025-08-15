from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest

from ....inventory_core import Inventory
from ....item_core import ITEM_ID_PEACH, get_item
from ....user_stats_core import UserStats

from ...auto_cancellation import AUTO_CANCELLATION_ID_DEFAULT
from ...adventure import Adventure
from ...return_ import RETURN_ID_AFTER, RETURN_ID_BEFORE

from ..helpers import get_should_cancel_adventure


def _iter_options():
    # ---- passes ----
    
    user_id = 202507290010
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    adventure = Adventure(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now
    adventure.updated_at = now
    
    user_stats = UserStats(
        user_id,
    )
    # If the user has every of its stats as 10, they should move 1.2 m / s
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 10
    
    inventory = Inventory(user_id)
    
    yield (
        adventure,
        user_stats,
        inventory,
        now + TimeDelta(hours = 6),
        3600,
        1600,
        False,
    )
    
    # ---- condition succeeds, health ----
    
    user_id = 202507290011
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    adventure = Adventure(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now
    adventure.updated_at = now
    adventure.health_exhausted = 100
    
    user_stats = UserStats(
        user_id,
    )
    # If the user has every of its stats as 10, they should move 1.2 m / s
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 10
    
    inventory = Inventory(user_id)
    
    yield (
        adventure,
        user_stats,
        inventory,
        now + TimeDelta(hours = 6),
        3600,
        1600,
        True,
    )
    
    # ---- condition succeeds, energy ----
    
    user_id = 202507290012
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    adventure = Adventure(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now
    adventure.updated_at = now
    adventure.energy_exhausted = 100
    
    user_stats = UserStats(
        user_id,
    )
    # If the user has every of its stats as 10, they should move 1.2 m / s
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 10
    
    inventory = Inventory(user_id)
    
    yield (
        adventure,
        user_stats,
        inventory,
        now + TimeDelta(hours = 6),
        3600,
        1600,
        True,
    )
    
    # ---- condition succeeds, inventory ----
    
    user_id = 202507290013
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    adventure = Adventure(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now
    adventure.updated_at = now
    
    user_stats = UserStats(
        user_id,
    )
    # If the user has every of its stats as 10, they should move 1.2 m / s
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 10
    
    inventory = Inventory(user_id)
    inventory.modify_item_amount(get_item(ITEM_ID_PEACH), 1000000)
    
    yield (
        adventure,
        user_stats,
        inventory,
        now + TimeDelta(hours = 6),
        3600,
        1600,
        True,
    )
    
    # ---- return - after ----
    
    user_id = 202507290014
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    adventure = Adventure(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now
    adventure.updated_at = now
    
    user_stats = UserStats(
        user_id,
    )
    # If the user has every of its stats as 10, they should move 1.2 m / s
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 10
    
    inventory = Inventory(user_id)
    
    yield (
        adventure,
        user_stats,
        inventory,
        now + TimeDelta(hours = 11, minutes = 40),
        3600,
        1600,
        True,
    )
    
    # ---- return - before ----
    
    user_id = 202507290015
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    adventure = Adventure(
        user_id,
        9999,
        0,
        RETURN_ID_BEFORE,
        AUTO_CANCELLATION_ID_DEFAULT,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now
    adventure.updated_at = now
    
    user_stats = UserStats(
        user_id,
    )
    # If the user has every of its stats as 10, they should move 1.2 m / s
    user_stats.stat_housewife = 10
    user_stats.stat_cuteness = 10
    user_stats.stat_bedroom = 10
    user_stats.stat_charm = 10
    user_stats.stat_loyalty = 10
    
    inventory = Inventory(user_id)
    
    yield (
        adventure,
        user_stats,
        inventory,
        now + TimeDelta(hours = 10, minutes = 40),
        3600,
        1600,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_should_cancel_adventure(
    adventure, user_stats, inventory, now, duration_till_next_occurrence, travel_duration
):
    """
    Tests whether ``get_should_cancel_adventure`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure in context.
    
    user_stats : ``UserStats``
        The user's stats.
    
    inventory : ``Inventory``
        The user's inventory.
    
    now : `DateTime`
        The current time.
    
    duration_till_next_occurrence : `int`
        How much is the duration till the next occurrence.
    
    travel_duration : `int`
        The duration to travel back.
    
    Returns
    -------
    output : `bool`
    """
    output = get_should_cancel_adventure(
        adventure, user_stats, inventory, now, duration_till_next_occurrence, travel_duration
    )
    vampytest.assert_instance(output, bool)
    return output
