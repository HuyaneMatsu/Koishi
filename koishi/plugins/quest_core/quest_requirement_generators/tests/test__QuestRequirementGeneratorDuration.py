from random import Random

import vampytest

from ...quest_requirement_instantiables import QuestRequirementInstantiableDuration
from ...quest_requirement_types import QUEST_REQUIREMENT_TYPE_DURATION

from ..duration import QuestRequirementGeneratorDuration


def _assert_fields_set(quest_requirement_generator_duration):
    """
    Asserts whether the instance has all of its fields set.
    
    Parameters
    ----------
    quest_requirement_generator_duration : ``QuestRequirementGeneratorDuration``
        The instance to check.
    """
    vampytest.assert_instance(quest_requirement_generator_duration, QuestRequirementGeneratorDuration)
    vampytest.assert_eq(quest_requirement_generator_duration.TYPE, QUEST_REQUIREMENT_TYPE_DURATION)
    vampytest.assert_instance(quest_requirement_generator_duration.duration_base, int)
    vampytest.assert_instance(quest_requirement_generator_duration.duration_require_multiple_of, int)
    vampytest.assert_instance(quest_requirement_generator_duration.duration_variance_percentage_lower_threshold, int)
    vampytest.assert_instance(quest_requirement_generator_duration.duration_variance_percentage_upper_threshold, int)


def test__QuestRequirementGeneratorDuration__new():
    """
    Tests whether ``QuestRequirementGeneratorDuration.__new__`` works as intended.
    """
    duration_base = 3600
    duration_require_multiple_of = 100
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_duration = QuestRequirementGeneratorDuration(
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
    )
    _assert_fields_set(quest_requirement_generator_duration)
    
    vampytest.assert_eq(quest_requirement_generator_duration.duration_base, duration_base)
    vampytest.assert_eq(
        quest_requirement_generator_duration.duration_require_multiple_of,
        duration_require_multiple_of,
    )
    vampytest.assert_eq(
        quest_requirement_generator_duration.duration_variance_percentage_lower_threshold,
        duration_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        quest_requirement_generator_duration.duration_variance_percentage_upper_threshold,
        duration_variance_percentage_upper_threshold,
    )


def test__QuestRequirementGeneratorDuration__repr():
    """
    Tests whether ``QuestRequirementGeneratorDuration.__repr__`` works as intended.
    """
    duration_base = 3600
    duration_require_multiple_of = 100
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_duration = QuestRequirementGeneratorDuration(
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
    )
    
    output = repr(quest_requirement_generator_duration)
    vampytest.assert_instance(output, str)


def _iter_options__eq():
    duration_base = 3600
    duration_require_multiple_of = 100
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    
    yield (
        (
            duration_base,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        (
            duration_base,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        True,
    )
    
    yield (
        (
            duration_base,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        (
            7200,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            duration_base,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        (
            duration_base,
            200,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            duration_base,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        (
            duration_base,
            duration_require_multiple_of,
            100,
            duration_variance_percentage_upper_threshold,
        ),
        False,
    )
    
    yield (
        (
            duration_base,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            duration_variance_percentage_upper_threshold,
        ),
        (
            duration_base,
            duration_require_multiple_of,
            duration_variance_percentage_lower_threshold,
            100,
        ),
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__QuestRequirementGeneratorDuration__eq(position_parameters_0, position_parameters_1):
    """
    Tests whether ``QuestRequirementGeneratorDuration.__eq__`` works as intended.
    
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
    quest_requirement_generator_duration_0 = QuestRequirementGeneratorDuration(*position_parameters_0)
    quest_requirement_generator_duration_1 = QuestRequirementGeneratorDuration(*position_parameters_1)
    
    output = quest_requirement_generator_duration_0 == quest_requirement_generator_duration_1
    vampytest.assert_instance(output, bool)
    return output


def test__QuestRequirementGeneratorDuration__generate():
    """
    Tests whether ``QuestRequirementGeneratorDuration.generate`` works as intended.
    """
    duration_base = 3600
    duration_require_multiple_of = 100
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    
    quest_requirement_generator_duration = QuestRequirementGeneratorDuration(
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_requirement_generator_duration.generate(random_number_generator)
    
    vampytest.assert_eq(
        generated,
        QuestRequirementInstantiableDuration(
            3800,
        ),
    )
    
    vampytest.assert_eq(
        diversion,
        0.9473684210526315,
    )
