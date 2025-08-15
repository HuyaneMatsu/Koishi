import vampytest

from ..auto_cancellation import AutoCancellation
from ..auto_cancellation_condition import AutoCancellationCondition
from ..auto_cancellation_condition_ids import AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN


def _assert_fields_set(auto_cancellation):
    """
    Asserts whether the auto cancellation has all of its fields set.
    
    Parameters
    ----------
    auto_cancellation : ``AutoCancellation``
    """
    vampytest.assert_instance(auto_cancellation, AutoCancellation)
    vampytest.assert_instance(auto_cancellation.energy_flat, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.energy_percentage, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.health_flat, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.health_percentage, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.id, int)
    vampytest.assert_instance(auto_cancellation.inventory_flat, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.inventory_percentage, AutoCancellationCondition, nullable = True)
    vampytest.assert_instance(auto_cancellation.name, str)


def test__AutoCancellation__new():
    """
    Tests whether ``AutoCancellation.__new__`` works as intended.
    """
    auto_cancellation_id = 999
    name = 'Pudding'
    inventory_flat = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    inventory_percentage = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    health_flat = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    health_percentage = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    energy_flat = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    energy_percentage = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    
    auto_cancellation = AutoCancellation(
        auto_cancellation_id,
        name,
        inventory_flat,
        inventory_percentage,
        health_flat,
        health_percentage,
        energy_flat,
        energy_percentage,
    )
    
    vampytest.assert_eq(auto_cancellation.id, auto_cancellation_id)
    vampytest.assert_eq(auto_cancellation.name, name)
    vampytest.assert_eq(auto_cancellation.energy_flat, energy_flat)
    vampytest.assert_eq(auto_cancellation.energy_percentage, energy_percentage)
    vampytest.assert_eq(auto_cancellation.health_flat, health_flat)
    vampytest.assert_eq(auto_cancellation.health_percentage, health_percentage)
    vampytest.assert_eq(auto_cancellation.inventory_flat, inventory_flat)
    vampytest.assert_eq(auto_cancellation.inventory_percentage, inventory_percentage)


def test__AutoCancellation__repr():
    """
    Tests whether ``AutoCancellation.__repr__`` works as intended.
    """
    auto_cancellation_id = 999
    name = 'Pudding'
    inventory_flat = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    inventory_percentage = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    health_flat = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    health_percentage = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    energy_flat = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 2)
    energy_percentage = AutoCancellationCondition(AUTO_CANCELLATION_CONDITION_ID_GREATER_THAN, 3)
    
    auto_cancellation = AutoCancellation(
        auto_cancellation_id,
        name,
        inventory_flat,
        inventory_percentage,
        health_flat,
        health_percentage,
        energy_flat,
        energy_percentage,
    )
    
    output = repr(auto_cancellation)
    vampytest.assert_instance(output, str)
