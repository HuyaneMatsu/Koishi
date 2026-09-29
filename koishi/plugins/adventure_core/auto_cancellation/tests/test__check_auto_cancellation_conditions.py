import vampytest

from ..auto_cancellation import auto_cancellation_create
from ..auto_cancellation_condition import auto_cancellation_condition_create
from ..auto_cancellation_condition_functional import auto_cancellation_condition_functional_create
from ..auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_EQUAL, AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL
)
from ..utils import check_auto_cancellation_conditions


def _iter_options():
    # none
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
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
        [],
        False,
    )
    
    # by condition
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
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
        [],
        True,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
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
        [],
        True,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
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
        [],
        True,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
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
        [],
        True,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        [],
        True,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        [],
        True,
    )
    
    # 2 conditions
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 20),
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        [],
        True,
    )
    
    # different signs
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_EQUAL, 20),
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
        [],
        False,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 20),
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
        [],
        True,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 20),
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
        [],
        False,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 20),
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
        [],
        False,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL, 20),
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
        [],
        True,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            None,
            None,
            None,
            auto_cancellation_condition_functional_create('shrimp', lambda looted_items : (True if looted_items else False)),
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        [],
        False,
    )
    
    yield (
        auto_cancellation_create(
            9999,
            '',
            None,
            None,
            None,
            None,
            None,
            None,
            auto_cancellation_condition_functional_create('shrimp', lambda looted_items : (True if looted_items else False)),
        ),
        100,
        0,
        100,
        0,
        100,
        0,
        [(1, 10, 300)],
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_auto_cancellation_conditions(
    auto_cancellation,
    inventory_total,
    inventory_exhausted,
    health_total,
    health_exhausted,
    energy_total,
    energy_exhausted,
    looted_items,
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
    
    looted_items : `list<(int, int, int)>`
        A list of tuple of 3 elements: loot state, item id and given amount.
    
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
        looted_items,
    )
    vampytest.assert_instance(output, bool)
    return output
