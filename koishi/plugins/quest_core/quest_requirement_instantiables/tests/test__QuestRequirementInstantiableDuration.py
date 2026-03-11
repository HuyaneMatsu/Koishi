import vampytest

from ...quest_requirement_serialisables import QuestRequirementSerialisableDuration
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_DURATION

from ..duration import QuestRequirementInstantiableDuration


def _assert_fields_set(quest_requirement_instantiable_duration):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_instantiable_duration : ``QuestRequirementInstantiableDuration``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_instantiable_duration, QuestRequirementInstantiableDuration)
    vampytest.assert_eq(quest_requirement_instantiable_duration.TYPE, QUEST_REQUIREMENT_TYPE_DURATION)
    vampytest.assert_instance(quest_requirement_instantiable_duration.duration, int)


def test__QuestRequirementInstantiableDuration__new():
    """
    Tests whether ``QuestRequirementInstantiableDuration.__new__`` works as intended.
    """
    duration = 3600
    
    quest_requirement_instantiable_duration = QuestRequirementInstantiableDuration(
        duration,
    )
    _assert_fields_set(quest_requirement_instantiable_duration)
    vampytest.assert_eq(quest_requirement_instantiable_duration.duration, duration)


def test__QuestRequirementInstantiableDuration__repr():
    """
    Tests whether ``QuestRequirementInstantiableDuration.__repr__`` works as intended.
    """
    duration = 3600
    
    quest_requirement_instantiable_duration = QuestRequirementInstantiableDuration(
        duration,
    )
    
    output = repr(quest_requirement_instantiable_duration)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    duration = 3600
    
    yield (
        (
            duration,
        ),
        (
            duration,
        ),
        True,
    )
    
    yield (
        (
            duration,
        ),
        (
            7200,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementInstantiableDuration__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementInstantiableDuration.__eq__`` works as intended.
    
    Parameters
    ----------
    position_parameters_0 : `tuple<object>`
        Positional parameters to create instance form.
    
    position_parameters_1 : `tuple<object>`
        Positional parameters to create instance form.
    
    Returns
    -------
    output : `bool`
    """
    quest_requirement_instantiable_duration_0 = QuestRequirementInstantiableDuration(*position_parameters_0)
    quest_requirement_instantiable_duration_1 = QuestRequirementInstantiableDuration(*position_parameters_1)
    
    output = quest_requirement_instantiable_duration_0 == quest_requirement_instantiable_duration_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementInstantiableDuration__instantiate():
    """
    Tests whether ``QuestRequirementInstantiableDuration.instantiate`` works as intended.
    """
    duration = 3600
    
    quest_requirement_instantiable_duration = QuestRequirementInstantiableDuration(
        duration,
    )
    
    output = quest_requirement_instantiable_duration.instantiate()
    
    vampytest.assert_instance(output, QuestRequirementSerialisableDuration)
    vampytest.assert_eq(output.duration, duration)
