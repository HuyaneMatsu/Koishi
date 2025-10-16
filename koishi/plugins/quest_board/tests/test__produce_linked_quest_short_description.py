from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import BUILTIN_EMOJIS

from ...quest_core import (
    LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest, QUEST_TEMPLATE_ID_MYSTIA_PEACH,
    QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, Quest, get_quest_template
)

from ..content_builders import produce_linked_quest_short_description


class DateTimeMock(DateTime):
    current_date_time = None
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    @classmethod
    def now(cls, tz):
        value = cls.current_date_time
        if value is None:
            value = DateTime.now(tz)
        return value


def _iter_options():
    now = DateTime(2016, 5, 14, 0, 0, 20, tzinfo = TimeZone.utc)
    
    quest_template_id_0 = QUEST_TEMPLATE_ID_MYSTIA_PEACH
    quest_template_0 = get_quest_template(quest_template_id_0)
    
    quest_template_id_1 = QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH
    quest_template_1 = get_quest_template(quest_template_id_1)
    
    user_id = 202510130000
    guild_id = 202510130001
    batch_id = 5999
    
    duration = 3600 * 24 * 3
    amount_required = 20
    reward_balance = 2600
    reward_credibility = 4
    
    quest_0 = Quest(
        quest_template_id_0,
        amount_required,
        duration,
        reward_credibility,
        reward_balance,
    )
    
    quest_1 = Quest(
        quest_template_id_1,
        amount_required,
        duration,
        reward_credibility,
        reward_balance,
    )
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_0,
    )
    linked_quest_0.taken_at = now - TimeDelta(seconds = 20)
    linked_quest_0.expires_at = now + TimeDelta(seconds = duration - 20)
    linked_quest_0.amount_submitted = 2
    
    yield (
        linked_quest_0,
        quest_template_0,
        now,
        (
            f'Time left: 2 days, 23 hours, 59 minutes\n'
            f'Submit 2 / 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_0,
    )
    linked_quest_1.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    linked_quest_1.completion_count = 1
    
    yield (
        linked_quest_1,
        quest_template_0,
        now,
        (
            f'Completed: 1 / 3 times, re-acceptable for 23 hours, 59 minutes, 40 seconds\n'
            f'Submit 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_0,
    )
    linked_quest_2.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    linked_quest_2.completion_count = 3
    
    yield (
        linked_quest_2,
        quest_template_0,
        now,
        (
            f'Completed: 3 / 3 times, cannot be re-accepted anymore\n'
            f'Submit 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    linked_quest_3 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_0,
    )
    linked_quest_3.taken_at = now - TimeDelta(seconds = duration)
    linked_quest_3.expires_at = now - TimeDelta(seconds = duration)
    linked_quest_3.amount_submitted = 2
    
    yield (
        linked_quest_3,
        quest_template_0,
        now,
        (
            f'Expired\n'
            f'Submit 2 / 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    linked_quest_4 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_1,
    )
    linked_quest_4.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    linked_quest_4.completion_count = 1
    
    yield (
        linked_quest_4,
        quest_template_1,
        now,
        (
            f'Completed: 1 times, re-acceptable for 23 hours, 59 minutes, 40 seconds\n'
            f'Submit 0.02 kg {BUILTIN_EMOJIS["grapes"]} Bluefrankish to Sakuya.'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_short_description(linked_quest, quest_template, current_date):
    """
    Tests whether ``produce_linked_quest_short_description`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        The linked quest being rendered.
    
    quest_template : ``QuestTemplate``
        The quest's template.
    
    Returns
    -------
    output : `str`
    """
    DateTimeMock.set_current(current_date)
    mocked = vampytest.mock_globals(
        produce_linked_quest_short_description,
        DateTime = DateTimeMock,
        recursion = 2,
    )
    output = [*mocked(linked_quest, quest_template)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
