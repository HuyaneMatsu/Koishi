from datetime import datetime as DateTime, timezone as TimeZone
from random import Random

import vampytest

from ...quest_requirement_instantiables import QuestRequirementInstantiableExpiration
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_EXPIRATION

from ..expiration import QuestRequirementGeneratorExpiration


def _assert_fields_set(quest_requirement_generator_expiration):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_generator_expiration : ``QuestRequirementGeneratorExpiration``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_generator_expiration, QuestRequirementGeneratorExpiration)
    vampytest.assert_eq(quest_requirement_generator_expiration.TYPE, QUEST_REQUIREMENT_TYPE_EXPIRATION)
    vampytest.assert_instance(quest_requirement_generator_expiration.expiration, DateTime)


def test__QuestRequirementGeneratorExpiration__new():
    """
    Tests whether ``QuestRequirementGeneratorExpiration.__new__`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_generator_expiration = QuestRequirementGeneratorExpiration(
        expiration,
    )
    _assert_fields_set(quest_requirement_generator_expiration)
    
    vampytest.assert_eq(quest_requirement_generator_expiration.expiration, expiration)


def test__QuestRequirementGeneratorExpiration__repr():
    """
    Tests whether ``QuestRequirementGeneratorExpiration.__repr__`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_generator_expiration = QuestRequirementGeneratorExpiration(
        expiration,
    )
    _assert_fields_set(quest_requirement_generator_expiration)
    
    output = repr(quest_requirement_generator_expiration)
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
def test__QuestRequirementGeneratorExpiration__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementGeneratorExpiration.__eq__`` works as intended.
    
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
    quest_requirement_generator_expiration_0 = QuestRequirementGeneratorExpiration(*position_parameters_0)
    quest_requirement_generator_expiration_1 = QuestRequirementGeneratorExpiration(*position_parameters_1)
    
    output = quest_requirement_generator_expiration_0 == quest_requirement_generator_expiration_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementGeneratorExpiration__generate():
    """
    Tests whether ``QuestRequirementGeneratorExpiration.generate`` works as intended.
    """
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    quest_requirement_generator_expiration = QuestRequirementGeneratorExpiration(
        expiration,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_requirement_generator_expiration.generate(random_number_generator)
    
    vampytest.assert_eq(
        generated,
        QuestRequirementInstantiableExpiration(
            expiration,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
