import vampytest

from ...item_core import ITEM_ID_GARLIC, ITEM_ID_MYSTIA

from ..amount_types import AMOUNT_TYPE_COUNT
from ..quest_requirement_generators import QuestRequirementGeneratorDuration, QuestRequirementGeneratorItemExact
from ..quest_reward_generators import QuestRewardGeneratorBalance, QuestRewardGeneratorCredibility
from ..quest_template import QuestTemplate


def _assert_fields_set(quest_template):
    """
    Asserts whether the given quest has all of its fields set.
    
    Parameters
    ----------
    quest_template : ``QuestTemplate``
        The quest to test.
    """
    vampytest.assert_instance(quest_template, QuestTemplate)
    vampytest.assert_instance(quest_template.chance_in, int)
    vampytest.assert_instance(quest_template.chance_out, int)
    vampytest.assert_instance(quest_template.description, str, nullable = True)
    vampytest.assert_instance(quest_template.id, int)
    vampytest.assert_instance(quest_template.level, int)
    vampytest.assert_instance(quest_template.mutually_exclusive_with_ids, tuple, nullable = True)
    vampytest.assert_instance(quest_template.repeat_count, int)
    vampytest.assert_instance(quest_template.requester_id, int)
    vampytest.assert_instance(quest_template.requirements, tuple, nullable = True)
    vampytest.assert_instance(quest_template.rewards, tuple, nullable = True)


def test__QuestTemplate__new():
    """
    Tests whether ``QuestTemplate.__new__`` works as intended.
    """
    chance_in = 1
    chance_out = 2
    description = 'Orin carted.'
    quest_template_id = 9999
    level = 2
    mutually_exclusive_with_ids = (
        9998,
        9997,
    )
    repeat_count = 3
    requester_id = ITEM_ID_MYSTIA
    requirements = (
        QuestRequirementGeneratorDuration(3600, 60, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_GARLIC, AMOUNT_TYPE_COUNT, 1000, 100, 75, 125),
    )
    rewards = (
        QuestRewardGeneratorBalance(2000, 50, 99, 101),
        QuestRewardGeneratorCredibility(2),
    )

    quest_template = QuestTemplate(
        quest_template_id,
        mutually_exclusive_with_ids,
        chance_in,
        chance_out,
        description,
        level,
        repeat_count,
        requester_id,
        requirements,
        rewards,
    )
    _assert_fields_set(quest_template)
    
    vampytest.assert_eq(quest_template.chance_in, chance_in)
    vampytest.assert_eq(quest_template.chance_out, chance_out)
    vampytest.assert_eq(quest_template.description, description)
    vampytest.assert_eq(quest_template.id, quest_template_id)
    vampytest.assert_eq(quest_template.level, level)
    vampytest.assert_eq(quest_template.mutually_exclusive_with_ids, mutually_exclusive_with_ids)
    vampytest.assert_eq(quest_template.repeat_count, repeat_count)
    vampytest.assert_eq(quest_template.requester_id, requester_id)
    vampytest.assert_eq(quest_template.requirements, requirements)
    vampytest.assert_eq(quest_template.rewards, rewards)


def test__QuestTemplate__repr():
    """
    Tests whether ``QuestTemplate.__repr__`` works as intended.
    """
    chance_in = 1
    chance_out = 2
    description = 'Orin carted.'
    quest_template_id = 9999
    level = 2
    mutually_exclusive_with_ids = (
        9998,
        9997,
    )
    repeat_count = 3
    requester_id = ITEM_ID_MYSTIA
    requirements = (
        QuestRequirementGeneratorDuration(3600, 60, 80, 120),
        QuestRequirementGeneratorItemExact(ITEM_ID_GARLIC, AMOUNT_TYPE_COUNT, 1000, 100, 75, 125),
    )
    rewards = (
        QuestRewardGeneratorBalance(2000, 50, 99, 101),
        QuestRewardGeneratorCredibility(2),
    )
    
    quest_template = QuestTemplate(
        quest_template_id,
        mutually_exclusive_with_ids,
        chance_in,
        chance_out,
        description,
        level,
        repeat_count,
        requester_id,
        requirements,
        rewards,
    )
    
    output = repr(quest_template)
    vampytest.assert_instance(output, str)
