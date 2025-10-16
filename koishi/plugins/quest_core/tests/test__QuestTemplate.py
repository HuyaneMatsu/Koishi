import vampytest

from ...item_core import ITEM_ID_GARLIC, ITEM_ID_MYSTIA

from ..amount_types import AMOUNT_TYPE_COUNT
from ..quest_template import QuestTemplate
from ..quest_types import QUEST_TYPE_ITEM_SUBMISSION


def _assert_fields_set(quest_template):
    """
    Asserts whether the given quest has all of its fields set.
    
    Parameters
    ----------
    quest_template : ``QuestTemplate``
        The quest to test.
    """
    vampytest.assert_instance(quest_template, QuestTemplate)
    vampytest.assert_instance(quest_template.amount_base, int)
    vampytest.assert_instance(quest_template.amount_require_multiple_of, int)
    vampytest.assert_instance(quest_template.amount_type, int)
    vampytest.assert_instance(quest_template.amount_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_template.amount_variance_percentage_upper_threshold, int)
    vampytest.assert_instance(quest_template.description, str, nullable = True)
    vampytest.assert_instance(quest_template.duration_base, int)
    vampytest.assert_instance(quest_template.duration_require_multiple_of, int)
    vampytest.assert_instance(quest_template.duration_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_template.duration_variance_percentage_upper_threshold, int)
    vampytest.assert_instance(quest_template.id, int)
    vampytest.assert_instance(quest_template.item_id, int)
    vampytest.assert_instance(quest_template.level, int)
    vampytest.assert_instance(quest_template.repeat_count, int)
    vampytest.assert_instance(quest_template.requester_id, int)
    vampytest.assert_instance(quest_template.reward_balance_base, int)
    vampytest.assert_instance(quest_template.reward_balance_require_multiple_of, int)
    vampytest.assert_instance(quest_template.reward_balance_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_template.reward_balance_variance_percentage_upper_threshold, int)
    vampytest.assert_instance(quest_template.reward_credibility, int)
    vampytest.assert_instance(quest_template.type, int)


def test__QuestTemplate__new():
    """
    Tests whether ``QuestTemplate.__new__`` works as intended.
    """
    amount_base = 1000
    amount_require_multiple_of = 100
    amount_type = AMOUNT_TYPE_COUNT
    amount_variance_percentage_lower_threshold = 75
    amount_variance_percentage_upper_threshold = 125
    description = 'Orin carted.'
    duration_base = 3600
    duration_require_multiple_of = 60
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    quest_template_id = 9999
    item_id = ITEM_ID_GARLIC
    level = 2
    repeat_count = 3
    requester_id = ITEM_ID_MYSTIA
    reward_balance_base = 2000
    reward_balance_require_multiple_of = 50
    reward_balance_variance_percentage_lower_threshold = 99
    reward_balance_variance_percentage_upper_threshold = 101
    reward_credibility = 2
    quest_type = QUEST_TYPE_ITEM_SUBMISSION

    quest_template = QuestTemplate(
        quest_template_id,
        description,
        quest_type,
        level,
        repeat_count,
        item_id,
        requester_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
        amount_type,
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
        reward_credibility,
        reward_balance_base,
        reward_balance_require_multiple_of,
        reward_balance_variance_percentage_lower_threshold,
        reward_balance_variance_percentage_upper_threshold,
    )
    _assert_fields_set(quest_template)
    
    vampytest.assert_eq(quest_template.amount_base, amount_base)
    vampytest.assert_eq(quest_template.amount_require_multiple_of, amount_require_multiple_of)
    vampytest.assert_eq(quest_template.amount_type, amount_type)
    vampytest.assert_eq(
        quest_template.amount_variance_percentage_lower_threshold, amount_variance_percentage_lower_threshold
    )
    vampytest.assert_eq(
        quest_template.amount_variance_percentage_upper_threshold, amount_variance_percentage_upper_threshold
    )
    vampytest.assert_eq(quest_template.description, description)
    vampytest.assert_eq(quest_template.duration_base, duration_base)
    vampytest.assert_eq(quest_template.duration_require_multiple_of, duration_require_multiple_of)
    vampytest.assert_eq(
        quest_template.duration_variance_percentage_lower_threshold, duration_variance_percentage_lower_threshold
    )
    vampytest.assert_eq(
        quest_template.duration_variance_percentage_upper_threshold, duration_variance_percentage_upper_threshold
    )
    vampytest.assert_eq(quest_template.id, quest_template_id)
    vampytest.assert_eq(quest_template.item_id, item_id)
    vampytest.assert_eq(quest_template.level, level)
    vampytest.assert_eq(quest_template.repeat_count, repeat_count)
    vampytest.assert_eq(quest_template.requester_id, requester_id)
    vampytest.assert_eq(quest_template.reward_balance_base, reward_balance_base)
    vampytest.assert_eq(quest_template.reward_balance_require_multiple_of, reward_balance_require_multiple_of)
    vampytest.assert_eq(
        quest_template.reward_balance_variance_percentage_lower_threshold,
        reward_balance_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        quest_template.reward_balance_variance_percentage_upper_threshold,
        reward_balance_variance_percentage_upper_threshold,
    )
    vampytest.assert_eq(quest_template.reward_credibility, reward_credibility)
    vampytest.assert_eq(quest_template.type, quest_type)


def test__QuestTemplate__repr():
    """
    Tests whether ``QuestTemplate.__repr__`` works as intended.
    """
    amount_base = 1000
    amount_require_multiple_of = 100
    amount_type = AMOUNT_TYPE_COUNT
    amount_variance_percentage_lower_threshold = 75
    amount_variance_percentage_upper_threshold = 125
    description = 'Orin carted.'
    duration_base = 3600
    duration_require_multiple_of = 60
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    quest_template_id = 9999
    item_id = ITEM_ID_GARLIC
    level = 2
    repeat_count = 3
    requester_id = ITEM_ID_MYSTIA
    reward_balance_base = 2000
    reward_balance_require_multiple_of = 50
    reward_balance_variance_percentage_lower_threshold = 99
    reward_balance_variance_percentage_upper_threshold = 101
    reward_credibility = 2
    quest_type = QUEST_TYPE_ITEM_SUBMISSION

    quest_template = QuestTemplate(
        quest_template_id,
        description,
        quest_type,
        level,
        repeat_count,
        item_id,
        requester_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
        amount_type,
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
        reward_credibility,
        reward_balance_base,
        reward_balance_require_multiple_of,
        reward_balance_variance_percentage_lower_threshold,
        reward_balance_variance_percentage_upper_threshold,
    )
    
    output = repr(quest_template)
    vampytest.assert_instance(output, str)
