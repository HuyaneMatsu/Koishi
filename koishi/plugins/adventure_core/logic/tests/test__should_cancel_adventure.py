import vampytest

from ....inventory_core import Inventory
from ....item_core import ITEM_ID_PEACH, get_item
from ....unit_core import AMOUNT_TYPE_COUNT
from ....user_stats_core import user_stats_create

from ...action import ACTION_ID_HAKUGYOKUROU_MANSION_GARDENING_PEACH
from ...adventure import LOOT_STATE_SUCCESS, adventure_action_create, adventure_create, loot_data_build
from ...auto_cancellation import AUTO_CANCELLATION_ID_DEFAULT
from ...goal import goal_create_item_exact
from ...return_ import RETURN_ID_AFTER, RETURN_ID_BEFORE

from ..helpers import should_cancel_adventure


def _iter_options():
    # ---- passes ----
    
    user_id = 202507290010
    now_seconds = 1463184000
    
    adventure = adventure_create(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        None,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now_seconds
    adventure.updated_at = now_seconds
    
    user_stats = user_stats_create(
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
        'Should not',
        adventure,
        user_stats,
        inventory,
        now_seconds + (6 * 3600),
        3600,
        1600,
        [],
        False,
    )
    
    # ---- condition succeeds, health ----
    
    user_id = 202507290011
    now_seconds = 1463184000
    
    adventure = adventure_create(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        None,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now_seconds
    adventure.updated_at = now_seconds
    adventure.health_exhausted = 100
    
    user_stats = user_stats_create(
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
        'Low health',
        adventure,
        user_stats,
        inventory,
        now_seconds + (6 * 3600),
        3600,
        1600,
        [],
        True,
    )
    
    # ---- condition succeeds, energy ----
    
    user_id = 202507290012
    now_seconds = 1463184000
    
    adventure = adventure_create(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        None,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now_seconds
    adventure.updated_at = now_seconds
    adventure.energy_exhausted = 100
    
    user_stats = user_stats_create(
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
        'Low energy',
        adventure,
        user_stats,
        inventory,
        now_seconds + (6 * 3600),
        3600,
        1600,
        [],
        True,
    )
    
    # ---- condition succeeds, inventory ----
    
    user_id = 202507290013
    now_seconds = 1463184000
    
    adventure = adventure_create(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        None,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now_seconds
    adventure.updated_at = now_seconds
    
    user_stats = user_stats_create(
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
        'Low inventory',
        adventure,
        user_stats,
        inventory,
        now_seconds + (6 * 3600),
        3600,
        1600,
        [],
        True,
    )
    
    # ---- return - after ----
    
    user_id = 202507290014
    now_seconds = 1463184000
    
    adventure = adventure_create(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        None,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now_seconds
    adventure.updated_at = now_seconds
    
    user_stats = user_stats_create(
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
        'return - after',
        adventure,
        user_stats,
        inventory,
        now_seconds + (11 * 3600 + 40 * 60),
        3600,
        1600,
        [],
        True,
    )
    
    # ---- return - before ----
    
    user_id = 202507290015
    now_seconds = 1463184000
    
    adventure = adventure_create(
        user_id,
        9999,
        0,
        RETURN_ID_BEFORE,
        AUTO_CANCELLATION_ID_DEFAULT,
        None,
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now_seconds
    adventure.updated_at = now_seconds
    
    user_stats = user_stats_create(
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
        'return - before',
        adventure,
        user_stats,
        inventory,
        now_seconds + (11 * 3600 + 40 * 60),
        3600,
        1600,
        [],
        True,
    )
    
    # ---- goal - Item exact ----
    
    user_id = 202609230000
    now_seconds = 1463184000
    
    goal = goal_create_item_exact(
        ITEM_ID_PEACH,
        AMOUNT_TYPE_COUNT,
        5,
    )
    
    adventure_action = adventure_action_create(
        ACTION_ID_HAKUGYOKUROU_MANSION_GARDENING_PEACH,
        now_seconds + 3600,
        None,
        loot_data_build([
            (LOOT_STATE_SUCCESS, ITEM_ID_PEACH, 10),
        ]),
        0,
        0,
    )
    
    
    adventure = adventure_create(
        user_id,
        9999,
        0,
        RETURN_ID_AFTER,
        AUTO_CANCELLATION_ID_DEFAULT,
        [goal],
        3600 * 12,
        100,
        100,
    )
    adventure.created_at = now_seconds
    adventure.updated_at = now_seconds
    adventure.action_listing = [adventure_action]
    
    user_stats = user_stats_create(
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
        'Goal - Item exact - success',
        adventure,
        user_stats,
        inventory,
        now_seconds + (6 * 3600),
        3600,
        1600,
        [],
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__should_cancel_adventure(
    adventure,
    user_stats,
    inventory,
    now_seconds,
    action_duration_seconds,
    travel_duration_seconds,
    looted_items,
):
    """
    Tests whether ``should_cancel_adventure`` works as intended.
    
    Parameters
    ----------
    adventure : ``Adventure``
        Adventure in context.
    
    user_stats : ``UserStats``
        The user's stats.
    
    inventory : ``Inventory``
        The user's inventory.
    
    now_seconds : `int`
        The current time in seconds.
    
    action_duration_seconds : `int`
        How much is the duration till the next occurrence.
    
    travel_duration_seconds : `int`
        The duration to travel back.
    
    looted_items : `list<(int, int, int)>`
        A list of tuple of 3 elements: loot state, item id and given amount.
    
    Returns
    -------
    output : `bool`
    """
    output = should_cancel_adventure(
        adventure,
        user_stats,
        inventory,
        now_seconds,
        action_duration_seconds,
        travel_duration_seconds,
        looted_items,
    )
    vampytest.assert_instance(output, bool)
    return output
