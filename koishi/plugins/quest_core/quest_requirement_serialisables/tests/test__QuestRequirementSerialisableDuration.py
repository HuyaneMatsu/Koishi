import vampytest

from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_DURATION

from ..duration import QuestRequirementSerialisableDuration


def _assert_fields_set(quest_requirement_serialisable_duration):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_serialisable_duration : ``QuestRequirementSerialisableDuration``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_serialisable_duration, QuestRequirementSerialisableDuration)
    vampytest.assert_eq(quest_requirement_serialisable_duration.TYPE, QUEST_REQUIREMENT_TYPE_DURATION)
    vampytest.assert_instance(quest_requirement_serialisable_duration.duration, int)


def test__QuestRequirementSerialisableDuration__new():
    """
    Tests whether ``QuestRequirementSerialisableDuration.__new__`` works as intended.
    """
    duration = 3600
    
    quest_requirement_serialisable_duration = QuestRequirementSerialisableDuration(
        duration,
    )
    _assert_fields_set(quest_requirement_serialisable_duration)


def test__QuestRequirementSerialisableDuration__repr():
    """
    Tests whether ``QuestRequirementSerialisableDuration.__repr__`` works as intended.
    """
    duration = 3600
    
    quest_requirement_serialisable_duration = QuestRequirementSerialisableDuration(
        duration,
    )
    
    output = repr(quest_requirement_serialisable_duration)
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
def test__QuestRequirementSerialisableDuration__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementSerialisableDuration.__eq__`` works as intended.
    
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
    quest_requirement_serialisable_duration_0 = QuestRequirementSerialisableDuration(*position_parameters_0)
    quest_requirement_serialisable_duration_1 = QuestRequirementSerialisableDuration(*position_parameters_1)
    
    output = quest_requirement_serialisable_duration_0 == quest_requirement_serialisable_duration_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementSerialisableDuration__deserialise():
    """
    Tests whether ``QuestRequirementSerialisableDuration.deserialise`` works as as intended.
    """
    duration = 3600
    
    data = b''.join([
        duration.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    quest_requirement_serialisable_duration, end_index = QuestRequirementSerialisableDuration.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_requirement_serialisable_duration)
    vampytest.assert_eq(end_index, 8)
    
    vampytest.assert_eq(quest_requirement_serialisable_duration.duration, duration)


def test__QuestRequirementSerialisableDuration__serialise():
    """
    Tests whether ``QuestRequirementSerialisableDuration.serialise`` works as intended.
    """
    duration = 3600
    
    quest_requirement_serialisable_duration = QuestRequirementSerialisableDuration(
        duration,
    )
    
    output = [*quest_requirement_serialisable_duration.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b''.join([
            duration.to_bytes(8, 'little'),
        ]),
    )
