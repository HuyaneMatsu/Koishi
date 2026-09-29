import vampytest

from ...item_core import ITEM_ID_STRAWBERRY
from ...unit_core import AMOUNT_TYPE_WEIGHT

from ..quest import Quest, quest_create
from ..quest_requirement_instantiables import (
    quest_requirement_instantiable_create_duration, quest_requirement_instantiable_create_item_exact
)
from ..quest_reward_instantiables import (
    quest_reward_instantiable_create_balance, quest_reward_instantiable_create_credibility
)
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


def test__Quest__repr():
    """
    Tests whether ``Quest.__repr__`` works as intended.
    """
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    requirements = (
        quest_requirement_instantiable_create_duration(3600 * 24 * 3),
        quest_requirement_instantiable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000),
    )
    rewards = (
        quest_reward_instantiable_create_balance(2600),
        quest_reward_instantiable_create_credibility(4),
    )
    
    quest = quest_create(
        quest_template_id,
        requirements,
        rewards,
    )
    
    output = repr(quest)
    vampytest.assert_instance(output, str)


def test__quest_create():
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    requirements = (
        quest_requirement_instantiable_create_duration(3600 * 24 * 3),
        quest_requirement_instantiable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000),
    )
    rewards = (
        quest_reward_instantiable_create_balance(2600),
        quest_reward_instantiable_create_credibility(4),
    )
    
    quest = quest_create(
        quest_template_id,
        requirements,
        rewards,
    )
    _assert_fields_set(quest)
    
    vampytest.assert_eq(quest.template_id, quest_template_id)
    vampytest.assert_eq(quest.requirements, requirements)
    vampytest.assert_eq(quest.rewards, rewards)
