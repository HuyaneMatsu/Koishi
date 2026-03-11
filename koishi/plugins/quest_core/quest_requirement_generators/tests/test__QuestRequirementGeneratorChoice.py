from random import Random

import vampytest

from ...quest_requirement_instantiables import QuestRequirementInstantiableDuration
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_NONE

from ..choice import QuestRequirementGeneratorChoice
from ..choice_option import QuestRequirementGeneratorChoiceOption
from ..duration import QuestRequirementGeneratorDuration


def _assert_fields_set(quest_requirement_generator_choice):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_generator_choice : ``QuestRequirementGeneratorChoice``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_generator_choice, QuestRequirementGeneratorChoice)
    vampytest.assert_eq(quest_requirement_generator_choice.TYPE, QUEST_REQUIREMENT_TYPE_NONE)
    vampytest.assert_instance(quest_requirement_generator_choice.options, tuple)


def test__QuestRequirementGeneratorChoice__new():
    """
    Tests whether ``QuestRequirementGeneratorChoice.__new__`` works as intended.
    """
    options = (
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(3600, 100, 100, 100),
            2.0,
        ),
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(1800, 100, 100, 100),
            1.0,
        ),
    )
    
    quest_requirement_generator_choice = QuestRequirementGeneratorChoice(
        options,
    )
    _assert_fields_set(quest_requirement_generator_choice)
    
    vampytest.assert_eq(quest_requirement_generator_choice.options, options)


def test__QuestRequirementGeneratorChoice__repr():
    """
    Tests whether ``QuestRequirementGeneratorChoice.__repr__`` works as intended.
    """
    options = (
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(3600, 100, 100, 100),
            2.0,
        ),
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(1800, 100, 100, 100),
            1.0,
        ),
    )
    
    quest_requirement_generator_choice = QuestRequirementGeneratorChoice(
        options,
    )
    
    output = repr(quest_requirement_generator_choice)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    options = (
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(3600, 100, 100, 100),
            2.0,
        ),
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(1800, 100, 100, 100),
            1.0,
        ),
    )
    
    yield (
        (
            options,
        ),
        (
            options,
        ),
        True,
    )
    
    yield (
        (
            options,
        ),
        (
            (
                QuestRequirementGeneratorChoiceOption(
                    QuestRequirementGeneratorDuration(3600, 100, 100, 100),
                    3.0,
                ),
                QuestRequirementGeneratorChoiceOption(
                    QuestRequirementGeneratorDuration(1800, 100, 100, 100),
                    1.0,
                ),
            ),
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementGeneratorChoice__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementGeneratorChoice.__eq__`` works as intended.
    
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
    quest_requirement_generator_choice_0 = QuestRequirementGeneratorChoice(*position_parameters_0)
    quest_requirement_generator_choice_1 = QuestRequirementGeneratorChoice(*position_parameters_1)
    
    output = quest_requirement_generator_choice_0 == quest_requirement_generator_choice_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementGeneratorChoice__generate():
    """
    Tests whether ``QuestRequirementGeneratorChoice.generate`` works as intended.
    """
    options = (
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(3600, 100, 100, 100),
            2.0,
        ),
        QuestRequirementGeneratorChoiceOption(
            QuestRequirementGeneratorDuration(1800, 100, 100, 100),
            1.0,
        ),
    )
    
    quest_requirement_generator_choice = QuestRequirementGeneratorChoice(
        options,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_requirement_generator_choice.generate(random_number_generator)
    
    vampytest.assert_eq(
        generated,
        QuestRequirementInstantiableDuration(
            3600,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        1.0,
    )
