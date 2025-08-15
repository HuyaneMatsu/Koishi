__all__ = ('AUTO_CANCELLATIONS_ALLOWED',)

from ..constants import AUTO_CANCELLATIONS

from .auto_cancellation import AutoCancellation
from .auto_cancellation_condition import AutoCancellationCondition
from .auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, AUTO_CANCELLATION_CONDITION_ID_LESS_THAN
)
from .auto_cancellation_ids import AUTO_CANCELLATION_ID_DEFAULT, AUTO_CANCELLATION_ID_NEVER


AUTO_CANCELLATION_DEFAULT = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_DEFAULT] = AutoCancellation(
    AUTO_CANCELLATION_ID_DEFAULT,
    'Default',
    None,
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 10),
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 50),
    None,
    None,
    AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 20),
)


AUTO_CANCELLATION_NEVER = AUTO_CANCELLATIONS[AUTO_CANCELLATION_ID_NEVER] = AutoCancellation(
    AUTO_CANCELLATION_ID_NEVER,
    'Never',
    None,
    None,
    None,
    None,
    None,
    None,
)

AUTO_CANCELLATIONS_ALLOWED = (
    AUTO_CANCELLATION_DEFAULT,
    AUTO_CANCELLATION_NEVER,
)
