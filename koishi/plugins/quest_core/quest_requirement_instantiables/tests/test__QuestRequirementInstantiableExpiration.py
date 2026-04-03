from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...quest_requirement_serialisables import QuestRequirementSerialisableExpiration
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_EXPIRATION

from ..expiration import QuestRequirementInstantiableExpiration


def _assert_fields_set(quest_requirement_instantiable_expiration):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_instantiable_expiration : ``QuestRequirementInstantiableExpiration``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_instantiable_expiration, QuestRequirementInstantiableExpiration)
    vampytest.assert_eq(quest_requirement_instantiable_expiration.TYPE, QUEST_REQUIREMENT_TYPE_EXPIRATION)
    vampytest.assert_instance(quest_requirement_instantiable_expiration.expiration, DateTime)


def test__QuestRequirementInstantiableExpiration__new():
    """
    Tests whether ``QuestRequirementInstantiableExpiration.__new__`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_instantiable_expiration = QuestRequirementInstantiableExpiration(
        expiration,
    )
    _assert_fields_set(quest_requirement_instantiable_expiration)
    
    vampytest.assert_eq(quest_requirement_instantiable_expiration.expiration, expiration)


def test__QuestRequirementInstantiableExpiration__repr():
    """
    Tests whether ``QuestRequirementInstantiableExpiration.__repr__`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_instantiable_expiration = QuestRequirementInstantiableExpiration(
        expiration,
    )
    
    output = repr(quest_requirement_instantiable_expiration)
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
def test__QuestRequirementInstantiableExpiration__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementInstantiableExpiration.__eq__`` works as intended.
    
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
    quest_requirement_instantiable_expiration_0 = QuestRequirementInstantiableExpiration(*position_parameters_0)
    quest_requirement_instantiable_expiration_1 = QuestRequirementInstantiableExpiration(*position_parameters_1)
    
    output = quest_requirement_instantiable_expiration_0 == quest_requirement_instantiable_expiration_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementInstantiableExpiration__instantiate():
    """
    Tests whether ``QuestRequirementInstantiableExpiration.instantiate`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_instantiable_expiration = QuestRequirementInstantiableExpiration(
        expiration,
    )
    
    output = quest_requirement_instantiable_expiration.instantiate()
    
    vampytest.assert_instance(output, QuestRequirementSerialisableExpiration)
    vampytest.assert_eq(output.expiration, expiration)
