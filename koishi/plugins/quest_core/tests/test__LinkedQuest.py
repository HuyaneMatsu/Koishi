from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..linked_quest import LinkedQuest
from ..quest import Quest
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY


def _assert_fields_set(linked_quest):
    """
    Asserts whether the given linked quest has all of its fields set.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The quest to test.
    """
    vampytest.assert_instance(linked_quest, LinkedQuest)
    vampytest.assert_instance(linked_quest.amount_submitted, int)
    vampytest.assert_instance(linked_quest.amount_required, int)
    vampytest.assert_instance(linked_quest.entry_id, int)
    vampytest.assert_instance(linked_quest.entry_id, int)
    vampytest.assert_instance(linked_quest.expires_at, DateTime)
    vampytest.assert_instance(linked_quest.reward_balance, int)
    vampytest.assert_instance(linked_quest.reward_credibility, int)
    vampytest.assert_instance(linked_quest.taken_at, DateTime)
    vampytest.assert_instance(linked_quest.template_id, int)
    vampytest.assert_instance(linked_quest.user_id, int)


def test__LinkedQuest__new():
    """
    Tests whether ``LinkedQuest.__new__`` works as intended.
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
    
    user_id = 202505090000
    guild_id = 202505090001
    batch_id = 5666
    
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest,
    )
    
    _assert_fields_set(linked_quest)
    
    vampytest.assert_eq(linked_quest.amount_submitted, 0)
    vampytest.assert_eq(linked_quest.amount_required, amount)
    vampytest.assert_eq(linked_quest.batch_id, batch_id)
    vampytest.assert_eq(linked_quest.entry_id, -1)
    # skip expires_at
    vampytest.assert_eq(linked_quest.guild_id, guild_id)
    vampytest.assert_eq(linked_quest.reward_balance, reward_balance)
    vampytest.assert_eq(linked_quest.reward_credibility, reward_credibility)
    # skip taken_at
    vampytest.assert_eq(linked_quest.template_id, template_id)
    vampytest.assert_eq(linked_quest.user_id, user_id)


def test__LinkedQuest__repr():
    """
    Tests whether ``LinkedQuest.__repr__`` works as intended.
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
    
    user_id = 202505090002
    guild_id = 202505090003
    batch_id = 5666
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest,
    )
    
    output = repr(linked_quest)
    vampytest.assert_instance(output, str)


def test__LinkedQuest__from_entry():
    """
    Tests whether ``LinkedQuest.from_entry`` works as intended.
    """
    taken_at = DateTime(2016, 5, 10, tzinfo = TimeZone.utc)
    expires_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    amount_submitted = 4
    amount_required = 20
    reward_balance = 2600
    reward_credibility = 4
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    user_id = 202505090000
    guild_id = 202505090001
    batch_id = 5666
    entry_id = 1222
    
    
    entry = {
        'taken_at': taken_at.replace(tzinfo = None),
        'expires_at': expires_at.replace(tzinfo = None),
        'amount_submitted': amount_submitted,
        'amount_required': amount_required,
        'reward_balance': reward_balance,
        'reward_credibility': reward_credibility,
        'template_id': template_id,
        'user_id': user_id,
        'guild_id': guild_id,
        'batch_id': batch_id,
        'id': entry_id,
    }
    
    
    linked_quest = LinkedQuest.from_entry(entry)
    
    _assert_fields_set(linked_quest)
    
    vampytest.assert_eq(linked_quest.amount_submitted, amount_submitted)
    vampytest.assert_eq(linked_quest.amount_required, amount_required)
    vampytest.assert_eq(linked_quest.batch_id, batch_id)
    vampytest.assert_eq(linked_quest.entry_id, entry_id)
    vampytest.assert_eq(linked_quest.expires_at, expires_at)
    vampytest.assert_eq(linked_quest.guild_id, guild_id)
    vampytest.assert_eq(linked_quest.reward_balance, reward_balance)
    vampytest.assert_eq(linked_quest.reward_credibility, reward_credibility)
    vampytest.assert_eq(linked_quest.taken_at, taken_at)
    vampytest.assert_eq(linked_quest.template_id, template_id)
    vampytest.assert_eq(linked_quest.user_id, user_id)
