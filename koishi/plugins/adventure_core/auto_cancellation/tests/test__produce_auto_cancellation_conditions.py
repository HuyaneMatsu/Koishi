import vampytest

from ..auto_cancellation import AutoCancellation
from ..auto_cancellation_condition import AutoCancellationCondition
from ..auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_EQUAL, AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL
)
from ..utils import produce_auto_cancellation_conditions


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
        'none',
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
        'inventory >= 0.056 kg',
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
        'inventory >= 56 %',
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
        'health >= 56',
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
        'health >= 56 %',
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
        'energy >= 56',
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
        'energy >= 56 %',
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
        'health >= 20 or energy >= 56',
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
        'health == 20',
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
        'health > 20',
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
        'health <= 20',
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
        'health < 20',
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
        'health != 20',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def tets__produce_auto_cancellation_conditions(auto_cancellation):
    """
    Tests whether ``produce_auto_cancellation_conditions`` works as intended.
    
    Parameters
    ----------
    auto_cancellation : ``AutoCancellation``
        Auto cancellation.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_auto_cancellation_conditions(auto_cancellation)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
