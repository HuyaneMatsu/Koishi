import vampytest

from ...quest_requirement_serialisables import QuestRequirementSerialisableBase
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_NONE

from ..base import QuestRequirementInstantiableBase


def _assert_fields_set(quest_requirement_instantiable_base):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_instantiable_base : ``QuestRequirementInstantiableBase``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_instantiable_base, QuestRequirementInstantiableBase)
    vampytest.assert_eq(quest_requirement_instantiable_base.TYPE, QUEST_REQUIREMENT_TYPE_NONE)


def test__QuestRequirementInstantiableBase__new():
    """
    Tests whether ``QuestRequirementInstantiableBase.__new__`` works as intended.
    """
    quest_requirement_instantiable_base = QuestRequirementInstantiableBase()
    _assert_fields_set(quest_requirement_instantiable_base)


def test__QuestRequirementInstantiableBase__repr():
    """
    Tests whether ``QuestRequirementInstantiableBase.__repr__`` works as intended.
    """
    quest_requirement_instantiable_base = QuestRequirementInstantiableBase()
    
    output = repr(quest_requirement_instantiable_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementInstantiableBase__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementInstantiableBase.__eq__`` works as intended.
    
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
    quest_requirement_instantiable_base_0 = QuestRequirementInstantiableBase(*position_parameters_0)
    quest_requirement_instantiable_base_1 = QuestRequirementInstantiableBase(*position_parameters_1)
    
    output = quest_requirement_instantiable_base_0 == quest_requirement_instantiable_base_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementInstantiableBase__instantiate():
    """
    Tests whether ``QuestRequirementInstantiableBase.instantiate`` works as intended.
    """
    quest_requirement_instantiable_base = QuestRequirementInstantiableBase()
    
    output = quest_requirement_instantiable_base.instantiate()
    
    vampytest.assert_eq(
        output,
        QuestRequirementSerialisableBase(),
    )
