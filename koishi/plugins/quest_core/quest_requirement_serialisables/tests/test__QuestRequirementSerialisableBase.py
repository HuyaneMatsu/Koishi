import vampytest

from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_NONE

from ..base import QuestRequirementSerialisableBase


def _assert_fields_set(quest_requirement_serialisable_base):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_serialisable_base : ``QuestRequirementSerialisableBase``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_serialisable_base, QuestRequirementSerialisableBase)
    vampytest.assert_eq(quest_requirement_serialisable_base.TYPE, QUEST_REQUIREMENT_TYPE_NONE)


def test__QuestRequirementSerialisableBase__new():
    """
    Tests whether ``QuestRequirementSerialisableBase.__new__`` works as intended.
    """
    quest_requirement_serialisable_base = QuestRequirementSerialisableBase()
    _assert_fields_set(quest_requirement_serialisable_base)


def test__QuestRequirementSerialisableBase__repr():
    """
    Tests whether ``QuestRequirementSerialisableBase.__repr__`` works as intended.
    """
    quest_requirement_serialisable_base = QuestRequirementSerialisableBase()
    
    output = repr(quest_requirement_serialisable_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementSerialisableBase__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementSerialisableBase.__eq__`` works as intended.
    
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
    quest_requirement_serialisable_base_0 = QuestRequirementSerialisableBase(*position_parameters_0)
    quest_requirement_serialisable_base_1 = QuestRequirementSerialisableBase(*position_parameters_1)
    
    output = quest_requirement_serialisable_base_0 == quest_requirement_serialisable_base_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementSerialisableBase__deserialise():
    """
    Tests whether ``QuestRequirementSerialisableBase.deserialise`` works as as intended.
    """
    data = b''
    start_index = 0
    
    quest_requirement_serialisable_base, end_index = QuestRequirementSerialisableBase.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_requirement_serialisable_base)
    vampytest.assert_eq(end_index, 0)


def test__QuestRequirementSerialisableBase__serialise():
    """
    Tests whether ``QuestRequirementSerialisableBase.serialise`` works as intended.
    """
    quest_requirement_serialisable_base = QuestRequirementSerialisableBase()
    
    output = [*quest_requirement_serialisable_base.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b'',
    )
