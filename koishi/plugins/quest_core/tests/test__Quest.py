import vampytest

from ...item_core import ITEM_ID_STRAWBERRY

from ..amount_types import AMOUNT_TYPE_WEIGHT
from ..quest import Quest
from ..quest_requirement_instantiables import (
    QuestRequirementInstantiableDuration, QuestRequirementInstantiableItemExact
)
from ..quest_reward_instantiables import QuestRewardInstantiableBalance, QuestRewardInstantiableCredibility
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY


def _assert_fields_set(quest):
    """
    Asserts whether the given quest has all of its fields set.
    
    Parameters
    ----------
    quest : ``Quest``
        The quest to test.
    """
    vampytest.assert_instance(quest, Quest)
    vampytest.assert_instance(quest.requirements, tuple, nullable = True)
    vampytest.assert_instance(quest.rewards, tuple, nullable = True)
    vampytest.assert_instance(quest.template_id, int)


def test__Quest__new():
    """
    Tests whether ``Quest.__new__`` works as intended.
    """
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    requirements = (
        QuestRequirementInstantiableDuration(3600 * 24 * 3),
        QuestRequirementInstantiableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000),
    )
    rewards = (
        QuestRewardInstantiableBalance(2600),
        QuestRewardInstantiableCredibility(4),
    )
    
    quest = Quest(
        quest_template_id,
        requirements,
        rewards,
    )
    _assert_fields_set(quest)
    
    vampytest.assert_eq(quest.template_id, quest_template_id)
    vampytest.assert_eq(quest.requirements, requirements)
    vampytest.assert_eq(quest.rewards, rewards)


def test__Quest__repr():
    """
    Tests whether ``Quest.__repr__`` works as intended.
    """
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    requirements = (
        QuestRequirementInstantiableDuration(3600 * 24 * 3),
        QuestRequirementInstantiableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000),
    )
    rewards = (
        QuestRewardInstantiableBalance(2600),
        QuestRewardInstantiableCredibility(4),
    )
    
    quest = Quest(
        quest_template_id,
        requirements,
        rewards,
    )
    
    output = repr(quest)
    vampytest.assert_instance(output, str)
