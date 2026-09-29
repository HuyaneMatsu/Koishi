import vampytest

from ..auto_cancellation import AutoCancellation, auto_cancellation_create
from ..auto_cancellation_condition import AutoCancellationCondition, auto_cancellation_condition_create
from ..auto_cancellation_condition_functional import (
    AutoCancellationConditionFunctional, auto_cancellation_condition_functional_create
)
from ..auto_cancellation_condition_ids import AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN


def test__auto_cancellation_create():
    auto_cancellation_id = 999
    name = 'Pudding'
    inventory_flat = auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    inventory_percentage = auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    health_flat = auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    health_percentage = auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    energy_flat = auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    energy_percentage = auto_cancellation_condition_create(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    looted_items = auto_cancellation_condition_functional_create('yes', lambda looted_items : True)
    
    auto_cancellation = auto_cancellation_create(
        auto_cancellation_id,
        name,
        inventory_flat,
        inventory_percentage,
        health_flat,
        health_percentage,
        energy_flat,
        energy_percentage,
        looted_items,
    )
    
    vampytest.assert_instance(auto_cancellation, AutoCancellation)
    vampytest.assert_instance(auto_cancellation.energy_flat, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.energy_percentage, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.health_flat, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.health_percentage, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.id, int)
    vampytest.assert_instance(auto_cancellation.inventory_flat, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.inventory_percentage, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.looted_items, AutoCancellationConditionFunctional, nullable = True)
    vampytest.assert_instance(auto_cancellation.name, str)
    
    vampytest.assert_eq(auto_cancellation.id, auto_cancellation_id)
    vampytest.assert_eq(auto_cancellation.name, name)
    vampytest.assert_eq(auto_cancellation.energy_flat, energy_flat)
    vampytest.assert_eq(auto_cancellation.energy_percentage, energy_percentage)
    vampytest.assert_eq(auto_cancellation.health_flat, health_flat)
    vampytest.assert_eq(auto_cancellation.health_percentage, health_percentage)
    vampytest.assert_eq(auto_cancellation.inventory_flat, inventory_flat)
    vampytest.assert_eq(auto_cancellation.inventory_percentage, inventory_percentage)
    vampytest.assert_eq(auto_cancellation.looted_items, looted_items)
