import vampytest

from ..auto_cancellation import AutoCancellation
from ..auto_cancellation_condition import AutoCancellationCondition
from ..auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_EQUAL, AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL
)
from ..utils import check_auto_cancellation_conditions


def _iter_options():
    # none
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        False,
    )
    
    # by condition
    
    yield (
        AutoCancellation(
            9999,
            '',
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
            None,
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    # 2 conditions
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 20),
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    # different signs
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_EQUAL, 20),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        False,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 20),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 20),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        False,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 20),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        False,
    )
    
    yield (
        AutoCancellation(
            9999,
            '',
            None,
            None,
            None,
            AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL, 20),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def tets__check_auto_cancellation_conditions(
    auto_cancellation,
    inventory_total,
    inventory_exhausted,
    health_total,
    health_exhausted,
    energy_total,
    energy_exhausted,
):
    """
    Tests whether ``check_auto_cancellation_conditions`` works as intended.
    
    Parameters
    ----------
    auto_cancellation : ``AutoCancellation``
        Auto cancellation.
    
    inventory_total : `int`
        The total inventory of the user.
    
    inventory_exhausted : `int`
        The exhausted inventory of the user.
    
    health_total : `int`
        The total health of the user.
    
    health_exhausted : `int`
        The exhausted health of the user.
    
    energy_total : `int`
        The total energy of the user.
    
    energy_exhausted : `int`
        The exhausted energy of the user.
    
    Returns
    -------
    output : `bool`
    """
    output = check_auto_cancellation_conditions(
        auto_cancellation,
        inventory_total,
        inventory_exhausted,
        health_total,
        health_exhausted,
        energy_total,
        energy_exhausted,
    )
    vampytest.assert_instance(output, bool)
    return output
