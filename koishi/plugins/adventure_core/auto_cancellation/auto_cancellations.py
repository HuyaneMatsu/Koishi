__all__ = ('AUTO_CANCELLATIONS_ALLOWED',)

from ..adventure import LOOT_STATE_SUCCESS
from ..constants import AUTO_CANCELLATIONS

from .auto_cancellation import AutoCancellation
from .auto_cancellation_condition import AutoCancellationCondition
from .auto_cancellation_condition_functional import AutoCancellationConditionFunctional
from .auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, AUTO_CANCELLATION_CONDITION_ID_LESS_THAN
)
from .auto_cancellation_ids import (
    AUTO_CANCELLATION_ID_DEFAULT, AUTO_CANCELLATION_ID_LOOT_LOST_ONCE, AUTO_CANCELLATION_ID_LOW_ENERGY_OR_HEALTH,
    AUTO_CANCELLATION_ID_NEVER
)


AUTO_CANCELLATION_DEFAULT = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_DEFAULT] = \
AutoCancellation(
    AUTO_CANCELLATION_ID_DEFAULT,
    'Default',
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 1000),
    None,
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 50),
    None,
    None,
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 20),
    None,
)


AUTO_CANCELLATION_NEVER = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_NEVER] = \
AutoCancellation(
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
AutoCancellation(
    AUTO_CANCELLATION_ID_LOOT_LOST_ONCE,
    'Loot lost once',
    None,
    None,
    None,
    None,
    None,
    None,
    AutoCancellationConditionFunctional(
        'lost once',
        lambda looted_items : any(item[0] != LOOT_STATE_SUCCESS for item in looted_items)
    ),
)


AUTO_CANCELLATION_LOW_ENERGY_OR_HEALTH = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_LOW_ENERGY_OR_HEALTH] = \
AutoCancellation(
    AUTO_CANCELLATION_ID_LOW_ENERGY_OR_HEALTH,
    'Low energy or health',
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 1000),
    None,
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 25),
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 10),
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 15),
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 5),
    None,
)


AUTO_CANCELLATIONS_ALLOWED = (
    AUTO_CANCELLATION_DEFAULT,
    AUTO_CANCELLATION_LOW_ENERGY_OR_HEALTH,
    AUTO_CANCELLATION_LOOT_LOST_ONCE,
    AUTO_CANCELLATION_NEVER,
)
