from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone

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
from ..utils import reset_linked_quest

from .helpers import DateTimeMock, _create_linked_quest_additional_input_fields


def test__reset_linked_quest__never_under_zero():
    """
    Tests whether ``reset_linked_quest`` works as intended.
    
    Case: do not go under 0.
    """
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id = 202602230003
    guild_id = 202602230004
    batch_id = 202602230005
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        *_create_linked_quest_additional_input_fields(),
    )
    linked_quest.completion_count = 1
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    DateTimeMock.set_current(now)
    
    mocked = vampytest.mock_globals(
        reset_linked_quest,
        DateTime = DateTimeMock
    )
    
    mocked(linked_quest)
    
    vampytest.assert_instance(linked_quest, LinkedQuest)
    vampytest.assert_eq(linked_quest.completion_state, LINKED_QUEST_COMPLETION_STATE_ACTIVE)
    vampytest.assert_eq(
        linked_quest.requirements,
        (
            QuestRequirementSerialisableDuration(3600 * 24 * 3),
            QuestRequirementSerialisableExpiration(now + TimeDelta(seconds = 3600 * 24 * 3)),
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 0),
        ),
    )


def test__reset_linked_quest__over_submitted():
    """
    Tests whether ``reset_linked_quest`` works as intended.
    
    Case: over submitted.
    """
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_id = 202604160000
    guild_id = 202604160001
    batch_id = 202604160002
    
    linked_quest = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        *_create_linked_quest_additional_input_fields(),
    )
    linked_quest.completion_count = 1
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    linked_quest.requirements[2].amount_submitted = 1200
    
    
    DateTimeMock.set_current(now)
    
    mocked = vampytest.mock_globals(
        reset_linked_quest,
        DateTime = DateTimeMock
    )
    
    mocked(linked_quest)
    
    vampytest.assert_instance(linked_quest, LinkedQuest)
    vampytest.assert_eq(linked_quest.completion_state, LINKED_QUEST_COMPLETION_STATE_ACTIVE)
    vampytest.assert_eq(
        linked_quest.requirements,
        (
            QuestRequirementSerialisableDuration(3600 * 24 * 3),
            QuestRequirementSerialisableExpiration(now + TimeDelta(seconds = 3600 * 24 * 3)),
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 200),
        ),
    )
