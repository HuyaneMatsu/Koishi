import vampytest

from ..quest import Quest
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
    vampytest.assert_instance(quest.amount, int)
    vampytest.assert_instance(quest.duration, int)
    vampytest.assert_instance(quest.reward_balance, int)
    vampytest.assert_instance(quest.reward_credibility, int)
    vampytest.assert_instance(quest.template_id, int)


def test__Quest__new():
    """
    Tests whether ``Quest.__new__`` works as intended.
    """
    duration = 3600 * 24 * 3
    amount = 4
    reward_balance = 2600
    reward_credibility = 4
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    quest = Quest(
        quest_template_id,
        amount,
        duration,
        reward_credibility,
        reward_balance,
    )
    _assert_fields_set(quest)
    
    vampytest.assert_eq(quest.amount, amount)
    vampytest.assert_eq(quest.duration, duration)
    vampytest.assert_eq(quest.reward_balance, reward_balance)
    vampytest.assert_eq(quest.reward_credibility, reward_credibility)
    vampytest.assert_eq(quest.template_id, quest_template_id)


def test__Quest__repr():
    """
    Tests whether ``Quest.__repr__`` works as intended.
    """
    duration = 3600 * 24 * 3
    amount = 4
    reward_balance = 2600
    reward_credibility = 4
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    quest = Quest(
        template_id,
        amount,
        duration,
        reward_credibility,
        reward_balance,
    )
    
    output = repr(quest)
    vampytest.assert_instance(output, str)
