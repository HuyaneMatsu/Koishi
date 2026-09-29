__all__ = ('AUTO_CANCELLATIONS_ALLOWED',)

from ..adventure import LOOT_STATE_SUCCESS
from ..constants import AUTO_CANCELLATIONS

from .auto_cancellation import auto_cancellation_create
from .auto_cancellation_condition import auto_cancellation_condition_create
from .auto_cancellation_condition_functional import auto_cancellation_condition_functional_create
from .auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, AUTO_CANCELLATION_CONDITION_ID_LESS_THAN
)
from .auto_cancellation_ids import (
    AUTO_CANCELLATION_ID_DEFAULT, AUTO_CANCELLATION_ID_LOOT_LOST_ONCE, AUTO_CANCELLATION_ID_LOW_ENERGY_OR_HEALTH,
    AUTO_CANCELLATION_ID_NEVER
)


AUTO_CANCELLATION_DEFAULT = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_DEFAULT] = \
auto_cancellation_create(
    AUTO_CANCELLATION_ID_DEFAULT,
    'Default',
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 1000),
    None,
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 50),
    None,
    None,
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 20),
    None,
)


AUTO_CANCELLATION_NEVER = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_NEVER] = \
auto_cancellation_create(
    AUTO_CANCELLATION_ID_NEVER,
    'Never',
    None,
    None,
    None,
    None,
    None,
    None,
    None,
)


AUTO_CANCELLATION_LOOT_LOST_ONCE = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_LOOT_LOST_ONCE] = \
auto_cancellation_create(
    AUTO_CANCELLATION_ID_LOOT_LOST_ONCE,
    'Loot lost once',
    None,
    None,
    None,
    None,
    None,
    None,
    auto_cancellation_condition_functional_create(
        'lost once',
        lambda looted_items : any(item[0] != LOOT_STATE_SUCCESS for item in looted_items)
    ),
)


AUTO_CANCELLATION_LOW_ENERGY_OR_HEALTH = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_LOW_ENERGY_OR_HEALTH] = \
auto_cancellation_create(
    AUTO_CANCELLATION_ID_LOW_ENERGY_OR_HEALTH,
    'Low energy or health',
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 1000),
    None,
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 25),
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 10),
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 15),
    auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 5),
    None,
)


AUTO_CANCELLATIONS_ALLOWED = (
    AUTO_CANCELLATION_DEFAULT,
    AUTO_CANCELLATION_LOW_ENERGY_OR_HEALTH,
    AUTO_CANCELLATION_LOOT_LOST_ONCE,
    AUTO_CANCELLATION_NEVER,
)
