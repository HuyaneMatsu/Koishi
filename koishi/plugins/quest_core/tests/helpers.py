from datetime import datetime as DateTime, timezone as TimeZone, timedelta as TimeDelta

from ...item_core import ITEM_ID_STRAWBERRY
from ...unit_core import AMOUNT_TYPE_WEIGHT

from ..quest import quest_create
from ..quest_requirement_instantiables import (
    quest_requirement_instantiable_create_duration, quest_requirement_instantiable_create_item_exact
)
from ..quest_requirement_serialisables import (
    quest_requirement_serialisable_create_duration, quest_requirement_serialisable_create_expiration,
    quest_requirement_serialisable_create_item_exact
)
from ..quest_reward_instantiables import (
    quest_reward_instantiable_create_balance, quest_reward_instantiable_create_credibility
)
from ..quest_reward_serialisables import (
    quest_reward_serialisable_create_balance, quest_reward_serialisable_create_credibility
)
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY


def _create_quest():
    return quest_create(
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        (
            quest_requirement_instantiable_create_duration(3600 * 24 * 3),
            quest_requirement_instantiable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000),
        ),
        (
            quest_reward_instantiable_create_balance(2600),
            quest_reward_instantiable_create_credibility(4),
        ),
    )


def _create_linked_quest_additional_input_fields():
    return (
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        (
            quest_requirement_serialisable_create_duration(3600 * 24 * 3),
            quest_requirement_serialisable_create_expiration(
                DateTime(2016, 5, 14, tzinfo = TimeZone.utc) + TimeDelta(seconds = 3600 * 24 * 3)
            ),
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 1000, 0),
        ),
        (
            quest_reward_serialisable_create_balance(2600),
            quest_reward_serialisable_create_credibility(4),
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
