from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

import vampytest
from hata import BUILTIN_EMOJIS

from ...item_core import ITEM_ID_BLUEFRANKISH, ITEM_ID_PEACH
from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest,
    QUEST_TEMPLATE_ID_MYSTIA_PEACH, QUEST_TEMPLATE_ID_SAKUYA_BLUEFRANKISH, QuestRequirementSerialisableDuration,
    QuestRequirementSerialisableExpiration, QuestRequirementSerialisableItemExact, QuestRewardSerialisableBalance,
    QuestRewardSerialisableCredibility, get_quest_template
)

from ..content_building import produce_linked_quest_short_description

from .helpers import DateTimeMock


def _iter_options():
    quest_accepted_at = DateTime(2016, 5, 14, 0, 0, 0, tzinfo = TimeZone.utc)
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
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_template_id_0,
        (
            QuestRequirementSerialisableDuration(duration),
            QuestRequirementSerialisableExpiration(quest_accepted_at + TimeDelta(seconds = duration)),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, amount_required, 2),
        ),
        (
            QuestRewardSerialisableBalance(reward_balance),
            QuestRewardSerialisableCredibility(reward_credibility),
        ),
    )
    
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
        quest_template_id_0,
        (
            QuestRequirementSerialisableDuration(duration),
            QuestRequirementSerialisableExpiration(quest_accepted_at + TimeDelta(seconds = duration)),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, amount_required, 0),
        ),
        (
            QuestRewardSerialisableBalance(reward_balance),
            QuestRewardSerialisableCredibility(reward_credibility),
        ),
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
        quest_template_id_0,
        (
            QuestRequirementSerialisableDuration(duration),
            QuestRequirementSerialisableExpiration(quest_accepted_at + TimeDelta(seconds = duration)),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, amount_required, 0),
        ),
        (
            QuestRewardSerialisableBalance(reward_balance),
            QuestRewardSerialisableCredibility(reward_credibility),
        ),
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
        quest_template_id_0,
        (
            QuestRequirementSerialisableDuration(duration),
            QuestRequirementSerialisableExpiration(quest_accepted_at),
            QuestRequirementSerialisableItemExact(ITEM_ID_PEACH, AMOUNT_TYPE_COUNT, amount_required, 2),
        ),
        (
            QuestRewardSerialisableBalance(reward_balance),
            QuestRewardSerialisableCredibility(reward_credibility),
        ),
    )
    
    yield (
        linked_quest_3,
        quest_template_0,
        now,
        (
            f'Time left: expired\n'
            f'Submit 2 / 20 {BUILTIN_EMOJIS["peach"]} Peach to Mystia.'
        ),
    )
    
    linked_quest_4 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_template_id_0,
        (
            QuestRequirementSerialisableDuration(duration),
            QuestRequirementSerialisableExpiration(now + TimeDelta(seconds = duration)),
            QuestRequirementSerialisableItemExact(ITEM_ID_BLUEFRANKISH, AMOUNT_TYPE_WEIGHT, amount_required, 0),
        ),
        (
            QuestRewardSerialisableBalance(reward_balance),
            QuestRewardSerialisableCredibility(reward_credibility),
        ),
    )
    linked_quest_4.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    linked_quest_4.completion_count = 1
    
    yield (
        linked_quest_4,
        quest_template_1,
        now,
        (
            f'Completed: 1 / unlimited times, re-acceptable for 23 hours, 59 minutes, 40 seconds\n'
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
    
    current_date : `Datetime`
        The current date.
    
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
