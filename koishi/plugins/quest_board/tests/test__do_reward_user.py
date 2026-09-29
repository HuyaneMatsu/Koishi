import vampytest

from ..helpers import do_reward_user

from ...inventory_core import Inventory
from ...item_core import ITEM_ID_STRAWBERRY, get_item_nullable
from ...guild_stats_core import guild_stats_create
from ...quest_core import (
    LinkedQuest, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, quest_reward_serialisable_create_item_exact,
    quest_reward_serialisable_create_balance, get_quest_template_nullable, get_user_adventurer_rank_info,
    linked_quest_create, quest_reward_serialisable_create_credibility
)
from ...user_balance import user_balance_create, user_balance_modify_balance_by
from ...user_stats_core import user_stats_create, user_stats_modify_credibility_by


def _iter_options():
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_strawberry is not None
    
    user_id = 202604160010
    guild_id = 202604160011
    batch_id = 5555
    
    
    yield (
        'give nothing x1',
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            None,
        ),
        1000,
        1000,
        1000,
        1,
        (
            None,
            [],
            1000,
            1000,
            1000,
        ),
    )
    
    reward = quest_reward_serialisable_create_item_exact(item_strawberry.id, 20)
    
    yield (
        'give item x1',
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                reward,
            ),
        ),
        1000,
        1000,
        1000,
        1,
        (
            [
                (reward.behaviour.type, reward.configuration.item_id, reward.configuration.amount_given),
            ],
            [
                (item_strawberry, 20),
            ],
            1000,
            1000,
            1000,
        ),
    )
    
    reward = quest_reward_serialisable_create_credibility(20)
    
    yield (
        'give credibility x1',
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                reward,
            ),
        ),
        1000,
        1000,
        1000,
        1,
        (
            [
                (reward.behaviour.type, 0, reward.configuration.credibility),
            ],
            [],
            1020,
            1000,
            1020,
        ),
    )
    
    reward = quest_reward_serialisable_create_balance(20)
    
    yield (
        'give balance x1',
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                reward,
            ),
        ),
        1000,
        1000,
        1000,
        1,
        (
            [
                (reward.behaviour.type, 0, reward.configuration.balance),
            ],
            [],
            1000,
            1020,
            1000,
        ),
    )
    
    reward = quest_reward_serialisable_create_credibility(20)
    
    yield (
        'give credibility x1 (high level)',
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                reward,
            ),
        ),
        10000,
        1000,
        20000,
        1,
        (
            [
                (reward.behaviour.type, 0, reward.configuration.credibility // 2),
            ],
            [],
            10010,
            1000,
            20012,
        ),
    )
    
    reward = quest_reward_serialisable_create_credibility(19)
    
    yield (
        'give credibility x10 (high level)',
        linked_quest_create(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                reward,
            ),
        ),
        10000,
        1000,
        20000,
        10,
        (
            [
                (reward.behaviour.type, 0, reward.configuration.credibility * 5),
            ],
            [],
            10095,
            1000,
            20114,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__do_reward_user(
    linked_quest, user_credibility, user_balance_amount, guild_credibility, reward_count
):
    """
    Tests whether ``do_reward_user`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to distribute the awards from..
    
    user_credibility : `int`
        The user's credibility.
    
    user_balance_amount : `int`
        The user's balance.
    
    guild_credibility : `int`
        The guild's credibility.
    
    reward_count : `int`
        How much times to reward the user.
    
    Returns
    -------
    output : ``(None | list<(int, int, int)>, list<(Item, int)>, int, int, int)``
    """
    inventory = Inventory(linked_quest.user_id)
    user_stats = user_stats_create(linked_quest.user_id)
    user_stats_modify_credibility_by(user_stats, user_credibility)
    user_balance = user_balance_create(linked_quest.user_id)
    user_balance_modify_balance_by(user_balance, user_balance_amount)
    guild_stats = guild_stats_create(linked_quest.guild_id)
    guild_stats.credibility = guild_credibility
    quest_template = get_quest_template_nullable(linked_quest.template_id)
    assert quest_template is not None
    quest_level = quest_template.level
    user_level = get_user_adventurer_rank_info(user_stats.credibility).level
    
    output = do_reward_user(
        linked_quest, inventory, user_stats, user_balance, guild_stats, quest_level, user_level, reward_count
    )
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, tuple)
            vampytest.assert_eq(len(element), 3)
            reward_type, identifier, amount_given = element
            vampytest.assert_instance(reward_type, int)
            vampytest.assert_instance(identifier, int)
            vampytest.assert_instance(amount_given, int)
    
    return (
        output,
        [(item_entry.item, item_entry.amount) for item_entry in inventory.iter_item_entries()],
        user_stats.credibility,
        user_balance.balance,
        guild_stats.credibility,
    )
