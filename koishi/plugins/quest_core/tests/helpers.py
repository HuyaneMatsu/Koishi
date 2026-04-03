from datetime import datetime as DateTime, timezone as TimeZone, timedelta as TimeDelta

from ...item_core import ITEM_ID_STRAWBERRY

from ..amount_types import AMOUNT_TYPE_WEIGHT
from ..quest import Quest
from ..quest_requirement_instantiables import (
    QuestRequirementInstantiableDuration, QuestRequirementInstantiableItemExact
)
from ..quest_requirement_serialisables import (
    QuestRequirementSerialisableDuration, QuestRequirementSerialisableExpiration, QuestRequirementSerialisableItemExact
)
from ..quest_reward_instantiables import QuestRewardInstantiableBalance, QuestRewardInstantiableCredibility
from ..quest_reward_serialisables import QuestRewardSerialisableBalance, QuestRewardSerialisableCredibility
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY


def _create_quest():
    return Quest(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        (
            QuestRequirementInstantiableDuration(3600 * 24 * 3),
            QuestRequirementInstantiableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000),
        ),
        (
            QuestRewardInstantiableBalance(2600),
            QuestRewardInstantiableCredibility(4),
        ),
    )


def _create_linked_quest_additional_input_fields():
    return (
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        (
            QuestRequirementSerialisableDuration(3600 * 24 * 3),
            QuestRequirementSerialisableExpiration(
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc) + TimeDelta(seconds = 3600 * 24 * 3)
            ),
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 0),
        ),
        (
            QuestRewardSerialisableBalance(2600),
            QuestRewardSerialisableCredibility(4),
        ),
    )


class DateTimeMock(DateTime):
    current_date_time = None
    
    @classmethod
    def set_current(cls, value):
        cls.current_date_time = value
    
    @classmethod
    def now(cls, time_zone):
        value = cls.current_date_time
        if value is None:
            value = DateTime.now(time_zone)
        return value
