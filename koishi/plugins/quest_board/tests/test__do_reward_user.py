import vampytest

from ..helpers import do_reward_user

from ...user_stats_core import UserStats
from ...inventory_core import Inventory
from ...item_core import ITEM_GROUP_ID_KNIFE, ITEM_ID_STRAWBERRY, get_item_nullable
from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
    QuestRewardSerialisableItemExact, QuestRewardSerialisableBalance,
    get_quest_template_nullable, get_user_adventurer_rank_info, QuestRewardSerialisableCredibility
)
from ...guild_stats import GuildStats
from ...user_balance import UserBalance


def _iter_options():
    item_strawberry = get_item_nullable(ITEM_ID_STRAWBERRY)
    assert item_strawberry is not None
    
    user_id = 202604160010
    guild_id = 202604160011
    batch_id = 5555
    
    
    yield (
        'give nothing x1',
        LinkedQuest(
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
    
    yield (
        'give item x1',
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableItemExact(item_strawberry.id, 20),
            ),
        ),
        1000,
        1000,
        1000,
        1,
        (
            [
                (QuestRewardSerialisableItemExact.TYPE, item_strawberry.id, 20),
            ],
            [
                (item_strawberry, 20),
            ],
            1000,
            1000,
            1000,
        ),
    )
    
    yield (
        'give credibility x1',
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableCredibility(20),
            ),
        ),
        1000,
        1000,
        1000,
        1,
        (
            [
                (QuestRewardSerialisableCredibility.TYPE, 0, 20),
            ],
            [],
            1020,
            1000,
            1020,
        ),
    )
    
    yield (
        'give balance x1',
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableBalance(20),
            ),
        ),
        1000,
        1000,
        1000,
        1,
        (
            [
                (QuestRewardSerialisableBalance.TYPE, 0, 20),
            ],
            [],
            1000,
            1020,
            1000,
        ),
    )
    
    yield (
        'give credibility x1 (high level)',
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableCredibility(20),
            ),
        ),
        10000,
        1000,
        20000,
        1,
        (
            [
                (QuestRewardSerialisableCredibility.TYPE, 0, 10),
            ],
            [],
            10010,
            1000,
            20012,
        ),
    )
    
    yield (
        'give credibility x10 (high level)',
        LinkedQuest(
            user_id,
            guild_id,
            batch_id,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableCredibility(19),
            ),
        ),
        10000,
        1000,
        20000,
        10,
        (
            [
                (QuestRewardSerialisableCredibility.TYPE, 0, 95),
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
    user_stats = UserStats(linked_quest.user_id)
    user_stats.modify_credibility_by(user_credibility)
    user_balance = UserBalance(linked_quest.user_id)
    user_balance.modify_balance_by(user_balance_amount)
    guild_stats = GuildStats(linked_quest.guild_id)
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
