from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_EXPIRATION

from ..expiration import QuestRequirementSerialisableExpiration


def _assert_fields_set(quest_requirement_serialisable_expiration):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_serialisable_expiration : ``QuestRequirementSerialisableExpiration``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_serialisable_expiration, QuestRequirementSerialisableExpiration)
    vampytest.assert_eq(quest_requirement_serialisable_expiration.TYPE, QUEST_REQUIREMENT_TYPE_EXPIRATION)
    vampytest.assert_instance(quest_requirement_serialisable_expiration.expiration, DateTime)


def test__QuestRequirementSerialisableExpiration__new():
    """
    Tests whether ``QuestRequirementSerialisableExpiration.__new__`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_serialisable_expiration = QuestRequirementSerialisableExpiration(
        expiration,
    )
    _assert_fields_set(quest_requirement_serialisable_expiration)


def test__QuestRequirementSerialisableExpiration__repr():
    """
    Tests whether ``QuestRequirementSerialisableExpiration.__repr__`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_serialisable_expiration = QuestRequirementSerialisableExpiration(
        expiration,
    )
    
    output = repr(quest_requirement_serialisable_expiration)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    
    yield (
        (
            expiration,
        ),
        (
            expiration,
        ),
        True,
    )
    
    yield (
        (
            expiration,
        ),
        (
            DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementSerialisableExpiration__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementSerialisableExpiration.__eq__`` works as intended.
    
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
    quest_requirement_serialisable_expiration_0 = QuestRequirementSerialisableExpiration(*position_parameters_0)
    quest_requirement_serialisable_expiration_1 = QuestRequirementSerialisableExpiration(*position_parameters_1)
    
    output = quest_requirement_serialisable_expiration_0 == quest_requirement_serialisable_expiration_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementSerialisableExpiration__deserialise():
    """
    Tests whether ``QuestRequirementSerialisableExpiration.deserialise`` works as as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    data = b''.join([
        int(expiration.timestamp()).to_bytes(8, 'little'),
    ])
    start_index = 0
    
    quest_requirement_serialisable_expiration, end_index = QuestRequirementSerialisableExpiration.deserialise(
        data, start_index
    )
    
    _assert_fields_set(quest_requirement_serialisable_expiration)
    vampytest.assert_eq(end_index, 8)
    
    vampytest.assert_eq(quest_requirement_serialisable_expiration.expiration, expiration)


def test__QuestRequirementSerialisableExpiration__serialise():
    """
    Tests whether ``QuestRequirementSerialisableExpiration.serialise`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_serialisable_expiration = QuestRequirementSerialisableExpiration(
        expiration,
    )
    
    output = [*quest_requirement_serialisable_expiration.serialise()]
    
    for element in output:
        vampytest.assert_instance(element, bytes)
    
    vampytest.assert_eq(
        b''.join(output),
        b''.join([
            int(expiration.timestamp()).to_bytes(8, 'little'),
        ]),
    )
