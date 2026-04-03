import vampytest

from ..base import QuestRequirementGeneratorBase
from ..duration import QuestRequirementGeneratorDuration
from ..choice_option import QuestRequirementGeneratorChoiceOption


def _assert_fields_set(quest_requirement_generator_choice_option):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_generator_choice_option : ``QuestRequirementGeneratorChoiceOption``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_generator_choice_option, QuestRequirementGeneratorChoiceOption)
    vampytest.assert_instance(quest_requirement_generator_choice_option.generator, QuestRequirementGeneratorBase)
    vampytest.assert_instance(quest_requirement_generator_choice_option.weight, int)


def test__QuestRequirementGeneratorChoiceOption__new():
    """
    Tests whether ``QuestRequirementGeneratorChoiceOption.__new__`` works as intended.
    """
    generator = QuestRequirementGeneratorDuration(3600, 100, 100, 100)
    weight = 5
    
    quest_requirement_generator_choice_option = QuestRequirementGeneratorChoiceOption(
        generator,
        weight,
    )
    _assert_fields_set(quest_requirement_generator_choice_option)
    
    vampytest.assert_eq(quest_requirement_generator_choice_option.generator, generator)
    vampytest.assert_eq(quest_requirement_generator_choice_option.weight, weight)


def test__QuestRequirementGeneratorChoiceOption__repr():
    """
    Tests whether ``QuestRequirementGeneratorChoiceOption.__repr__`` works as intended.
    """
    generator = QuestRequirementGeneratorDuration(3600, 100, 100, 100)
    weight = 5
    
    quest_requirement_generator_choice_option = QuestRequirementGeneratorChoiceOption(
        generator,
        weight,
    )
    
    output = repr(quest_requirement_generator_choice_option)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    generator = QuestRequirementGeneratorDuration(3600, 100, 100, 100)
    weight = 5
    
    yield (
        (
            generator,
            weight,
        ),
        (
            generator,
            weight,
        ),
        True,
    )
    
    yield (
        (
            generator,
            weight,
        ),
        (
            QuestRequirementGeneratorDuration(3600, 50, 100, 100),
            weight,
        ),
        False,
    )
    
    yield (
        (
            generator,
            weight,
        ),
        (
            generator,
            4,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementGeneratorChoiceOption__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementGeneratorChoiceOption.__eq__`` works as intended.
    
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
    quest_requirement_generator_choice_option_0 = QuestRequirementGeneratorChoiceOption(*position_parameters_0)
    quest_requirement_generator_choice_option_1 = QuestRequirementGeneratorChoiceOption(*position_parameters_1)
    
    output = quest_requirement_generator_choice_option_0 == quest_requirement_generator_choice_option_1
    vampytest.assert_instance(output, bool)
    return output
