from random import Random

import vampytest

from ...quest_requirement_instantiables import QuestRequirementInstantiableBase
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_NONE

from ..base import QuestRequirementGeneratorBase


def _assert_fields_set(quest_requirement_generator_base):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_generator_base : ``QuestRequirementGeneratorBase``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_generator_base, QuestRequirementGeneratorBase)
    vampytest.assert_eq(quest_requirement_generator_base.TYPE, QUEST_REQUIREMENT_TYPE_NONE)


def test__QuestRequirementGeneratorBase__new():
    """
    Tests whether ``QuestRequirementGeneratorBase.__new__`` works as intended.
    """
    quest_requirement_generator_base = QuestRequirementGeneratorBase()
    _assert_fields_set(quest_requirement_generator_base)


def test__QuestRequirementGeneratorBase__repr():
    """
    Tests whether ``QuestRequirementGeneratorBase.__repr__`` works as intended.
    """
    quest_requirement_generator_base = QuestRequirementGeneratorBase()
    
    output = repr(quest_requirement_generator_base)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    yield (
        (),
        (),
        True,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementGeneratorBase__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementGeneratorBase.__eq__`` works as intended.
    
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
    quest_requirement_generator_base_0 = QuestRequirementGeneratorBase(*position_parameters_0)
    quest_requirement_generator_base_1 = QuestRequirementGeneratorBase(*position_parameters_1)
    
    output = quest_requirement_generator_base_0 == quest_requirement_generator_base_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementGeneratorBase__generate():
    """
    Tests whether ``QuestRequirementGeneratorBase.generate`` works as intended.
    """
    quest_requirement_generator_base = QuestRequirementGeneratorBase()
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_requirement_generator_base.generate(random_number_generator)
    
    vampytest.assert_eq(
        generated,
        QuestRequirementInstantiableBase(),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
