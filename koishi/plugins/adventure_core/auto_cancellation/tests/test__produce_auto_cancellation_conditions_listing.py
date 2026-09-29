import vampytest

from ..auto_cancellation import auto_cancellation_create
from ..auto_cancellation_condition import auto_cancellation_condition_create
from ..auto_cancellation_condition_functional import auto_cancellation_condition_functional_create
from ..auto_cancellation_condition_ids import (
    AUTO_CANCELLATION_CONDITION_ID_EQUAL, AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL,
    AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL
)
from ..utils import produce_auto_cancellation_conditions_listing


def _iter_options():
    # none + indent
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        '        ',
        (
            '        - name: Shrimp'
        ),
    )
    
    # none - indent
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        None,
        (
            '- name: Shrimp'
        ),
    )
    
    # by condition
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
            None,
            None,
            None,
            None,
        ),
        '        ',
        (
            '        - name: Shrimp\n'
            '        - inventory >= 0.056 kg'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
            None,
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - inventory >= 56 %'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - health >= 56'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - health >= 56 %'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - energy >= 56'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - energy >= 56 %'
        ),
    )
    
    # 2 conditions
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 20),
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_OR_EQUAL, 56),
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - health >= 20 %\n'
            '        - energy >= 56'
        ),
    )
    
    # different signs
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_EQUAL, 21),
            None,
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - health == 21 %'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 22),
            None,
            None,
            None,
        ),
        '        ',
            
        (   
            '        - name: Shrimp\n'
            '        - health > 22 %'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_OR_EQUAL, 23),
            None,
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - health <= 23 %'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_LESS_THAN, 24),
            None,
            None,
            None,
        ),
        '        ',
        (   
            '        - name: Shrimp\n'
            '        - health < 24 %'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_NOT_EQUAL, 25),
            None,
            None,
            None,
        ),
        '        ',
        (
            '        - name: Shrimp\n'
            '        - health != 25 %'
        ),
    )
    
    yield (
        auto_cancellation_create(
            9999,
            'Shrimp',
            None,
            None,
            None,
            None,
            None,
            None,
            auto_cancellation_condition_functional_create('Shrimp', lambda looted_items : True),
        ),
        '        ',
        (
            '        - name: Shrimp\n'
            '        - looted items: Shrimp'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_auto_cancellation_conditions_listing(auto_cancellation, indent_prefix):
    output = [*produce_auto_cancellation_conditions_listing(auto_cancellation, indent_prefix)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
