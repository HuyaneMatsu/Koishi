from datetime import datetime as DateTime, timezone as TimeZone

import vampytest


from ...item_core import ITEM_ID_STRAWBERRY

from ..amount_types import AMOUNT_TYPE_WEIGHT
from ..linked_quest import LinkedQuest
from ..linked_quest_completion_states import (
    LINKED_QUEST_COMPLETION_STATE_ACTIVE, LINKED_QUEST_COMPLETION_STATE_COMPLETED
)
from ..quest_requirement_serialisables import (
    QuestRequirementSerialisableDuration, QuestRequirementSerialisableExpiration, QuestRequirementSerialisableItemExact
)
from ..quest_reward_serialisables import (
    QuestRewardSerialisableBalance, QuestRewardSerialisableCredibility
)
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
from ..serialisation import quest_serialisable_serialise


def _assert_fields_set(linked_quest):
    """
    Asserts whether the given linked quest has all of its fields set.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The quest to test.
    """
    vampytest.assert_instance(linked_quest, LinkedQuest)
    vampytest.assert_instance(linked_quest.batch_id, int)
    vampytest.assert_instance(linked_quest.completion_count, int)
    vampytest.assert_instance(linked_quest.completion_state, int)
    vampytest.assert_instance(linked_quest.entry_id, int)
    vampytest.assert_instance(linked_quest.flags, int)
    vampytest.assert_instance(linked_quest.guild_id, int)
    vampytest.assert_instance(linked_quest.requirements, tuple, nullable = True)
    vampytest.assert_instance(linked_quest.rewards, tuple, nullable = True)
    vampytest.assert_instance(linked_quest.template_id, int)
    vampytest.assert_instance(linked_quest.user_id, int)


def test__LinkedQuest__new():
    """
    Tests whether ``LinkedQuest.__new__`` works as intended.
    """
    user_id = 202505090000
    guild_id = 202505090001
    batch_id = 5666
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    requirements = (
        QuestRequirementSerialisableDuration(3600 * 24 * 3),
        QuestRequirementSerialisableExpiration(DateTime(2016, 10, 28, tzinfo = TimeZone.utc)),
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 0),
    )
    rewards = (
        QuestRewardSerialisableBalance(2600),
        QuestRewardSerialisableCredibility(4),
    )
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        template_id,
        requirements,
        rewards,
    )
    
    _assert_fields_set(linked_quest)
    
    vampytest.assert_eq(linked_quest.batch_id, batch_id)
    vampytest.assert_eq(linked_quest.completion_count, 0)
    vampytest.assert_eq(linked_quest.completion_state, LINKED_QUEST_COMPLETION_STATE_ACTIVE)
    vampytest.assert_eq(linked_quest.entry_id, 0)
    vampytest.assert_eq(linked_quest.flags, 0)
    vampytest.assert_eq(linked_quest.guild_id, guild_id)
    vampytest.assert_eq(linked_quest.requirements, requirements)
    vampytest.assert_eq(linked_quest.rewards, rewards)
    vampytest.assert_eq(linked_quest.template_id, template_id)
    vampytest.assert_eq(linked_quest.user_id, user_id)


def test__LinkedQuest__repr():
    """
    Tests whether ``LinkedQuest.__repr__`` works as intended.
    """
    user_id = 202505090000
    guild_id = 202505090001
    batch_id = 5666
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    requirements = (
        QuestRequirementSerialisableDuration(3600 * 24 * 3),
        QuestRequirementSerialisableExpiration(DateTime(2016, 10, 28, tzinfo = TimeZone.utc)),
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 0),
    )
    rewards = (
        QuestRewardSerialisableBalance(2600),
        QuestRewardSerialisableCredibility(4),
    )
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        template_id,
        requirements,
        rewards,
    )
    
    output = repr(linked_quest)
    vampytest.assert_instance(output, str)


def test__LinkedQuest__from_entry():
    """
    Tests whether ``LinkedQuest.from_entry`` works as intended.
    """
    user_id = 202505090000
    guild_id = 202505090001
    batch_id = 5666
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    requirements = (
        QuestRequirementSerialisableDuration(3600 * 24 * 3),
        QuestRequirementSerialisableExpiration(DateTime(2016, 10, 28, tzinfo = TimeZone.utc)),
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 0),
    )
    rewards = (
        QuestRewardSerialisableBalance(2600),
        QuestRewardSerialisableCredibility(4),
    )
    
    completion_count = 1
    completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    entry_id = 1222
    
    
    entry = {
        'user_id': user_id,
        'guild_id': guild_id,
        'batch_id': batch_id,
        'template_id': template_id,
        'requirements': quest_serialisable_serialise(requirements),
        'rewards': quest_serialisable_serialise(rewards),
        'completion_count': completion_count,
        'completion_state': completion_state,
        'id': entry_id,
    }
    
    
    linked_quest = LinkedQuest.from_entry(entry)
    
    _assert_fields_set(linked_quest)
    
    vampytest.assert_eq(linked_quest.completion_count, completion_count)
    vampytest.assert_eq(linked_quest.completion_state, completion_state)
    vampytest.assert_eq(linked_quest.batch_id, batch_id)
    vampytest.assert_eq(linked_quest.entry_id, entry_id)
    vampytest.assert_eq(linked_quest.flags, 0)
    vampytest.assert_eq(linked_quest.guild_id, guild_id)
    vampytest.assert_eq(linked_quest.requirements, requirements)
    vampytest.assert_eq(linked_quest.rewards, rewards)
    vampytest.assert_eq(linked_quest.template_id, template_id)
    vampytest.assert_eq(linked_quest.user_id, user_id)
