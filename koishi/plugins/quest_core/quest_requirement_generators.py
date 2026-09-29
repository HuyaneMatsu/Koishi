__all__ = ()

from scarletio import RichAttributeErrorBaseType, copy_docs

from .generation_helpers import get_random_value_and_diversity_with_variance
from .quest_requirement_instantiables import (
    quest_requirement_instantiable_create_duration,
    quest_requirement_instantiable_create_expiration, quest_requirement_instantiable_create_item_category,
    quest_requirement_instantiable_create_item_exact, quest_requirement_instantiable_create_item_group
)
from .quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_CHOICE, QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION,
    QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY, QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
)
from .quest_sub_type_generator_bases import (
    QuestSubTypeGeneratorConfiguration, generate_base, generate_with_diversion_base,
    quest_sub_type_generator_behaviour_create, quest_sub_type_generator_create
)


@copy_docs(generate_base)
def generate_duration(configuration, random_number_generator):
    duration, diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        configuration.duration_base,
        configuration.duration_require_multiple_of,
        configuration.duration_variance_percentage_lower_threshold,
        configuration.duration_variance_percentage_upper_threshold,
    )
    
    return (
        quest_requirement_instantiable_create_duration(duration),
        (1.0 / diversion),
    )


@copy_docs(generate_base)
def generate_expiration(configuration, random_number_generator):
    return (
        quest_requirement_instantiable_create_expiration(configuration.expiration),
        1.0,
    )


@copy_docs(generate_base)
def generate_choice(configuration, random_number_generator):
    options = configuration.options
    total_weight = sum(option.weight for option in options)
    value = total_weight * random_number_generator.random()
    
    cumulative = 0.0
    for option in options:
        cumulative += option.weight
        if cumulative >= value:
            break
    
    generator = option.generator
    return generator.behaviour.generate(generator.configuration, random_number_generator)


@copy_docs(generate_base)
def generate_item_category(configuration, random_number_generator):
    amount, diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        configuration.amount_base,
        configuration.amount_require_multiple_of,
        configuration.amount_variance_percentage_lower_threshold,
        configuration.amount_variance_percentage_upper_threshold,
    )
    
    return (
        quest_requirement_instantiable_create_item_category(
            configuration.item_flags,
            configuration.amount_type,
            amount,
        ),
        diversion,
    )


@copy_docs(generate_base)
def generate_item_exact(configuration, random_number_generator):
    amount, diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        configuration.amount_base,
        configuration.amount_require_multiple_of,
        configuration.amount_variance_percentage_lower_threshold,
        configuration.amount_variance_percentage_upper_threshold,
    )
    
    return (
        quest_requirement_instantiable_create_item_exact(
            configuration.item_id,
            configuration.amount_type,
            amount,
        ),
        diversion,
    )


@copy_docs(generate_base)
def generate_item_group(configuration, random_number_generator):
    
    amount, diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        configuration.amount_base,
        configuration.amount_require_multiple_of,
        configuration.amount_variance_percentage_lower_threshold,
        configuration.amount_variance_percentage_upper_threshold,
    )
    
    return (
        quest_requirement_instantiable_create_item_group(
            configuration.item_group_id,
            configuration.amount_type,
            amount,
        ),
        diversion,
    )

QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_CHOICE = quest_sub_type_generator_behaviour_create(
    QUEST_REQUIREMENT_TYPE_CHOICE,
    generate_choice,
    generate_with_diversion_base,
)

QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_DURATION = quest_sub_type_generator_behaviour_create(
    QUEST_REQUIREMENT_TYPE_DURATION,
    generate_duration,
    generate_with_diversion_base,
)

QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_EXPIRATION = quest_sub_type_generator_behaviour_create(
    QUEST_REQUIREMENT_TYPE_EXPIRATION,
    generate_expiration,
    generate_with_diversion_base,
)

QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_ITEM_CATEGORY = quest_sub_type_generator_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    generate_item_category,
    generate_with_diversion_base,
)

QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_ITEM_EXACT = quest_sub_type_generator_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    generate_item_exact,
    generate_with_diversion_base,
)

QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_ITEM_GROUP = quest_sub_type_generator_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    generate_item_group,
    generate_with_diversion_base,
)


class QuestRequirementGeneratorConfigurationChoice(QuestSubTypeGeneratorConfiguration):
    """
    Requirement generator choice configuration.
    
    Attributes
    ----------
    options : ``tuple<QuestRequirementGeneratorChoiceOption>``
        Options to choose from.
    """
    __slots__ = ('options',)


class QuestRequirementGeneratorConfigurationDuration(QuestSubTypeGeneratorConfiguration):
    """
    Requirement generator duration configuration.
    
    Attributes
    ----------
    duration_base : `int`
        The quest's duration in seconds.
    
    duration_require_multiple_of : `int`
        Value to require the duration to be multiple of.
    
    duration_variance_percentage_lower_threshold : `int`
        Lower threshold of for duration variance in percentage.
    
    duration_variance_percentage_upper_threshold : `int`
        Upper threshold of for duration variance in percentage.
    """
    __slots__ = (
        'duration_base', 'duration_require_multiple_of', 'duration_variance_percentage_lower_threshold',
        'duration_variance_percentage_upper_threshold',
    )


class QuestRequirementGeneratorConfigurationExpiration(QuestSubTypeGeneratorConfiguration):
    """
    Requirement generator expiration configuration.
    
    Attributes
    ----------
    expiration : `DateTime`
        When the quest expires.
    """
    __slots__ = ('expiration',)


class QuestRequirementGeneratorConfigurationItemCategory(QuestSubTypeGeneratorConfiguration):
    """
    Requirement generator item category configuration.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items required by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_type : `int`
        The amount's type.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    item_flags : `int`
        The required item flags the items should have.
    """
    __slots__ = (
        'amount_base', 'amount_require_multiple_of', 'amount_type', 'amount_variance_percentage_lower_threshold',
        'amount_variance_percentage_upper_threshold', 'item_flags'
    )


class QuestRequirementGeneratorConfigurationItemExact(QuestSubTypeGeneratorConfiguration):
    """
    Requirement generator item exact configuration.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items required by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_type : `int`
        The amount's type.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    item_id : `int`
        The required item's identifier.
    """
    __slots__ = (
        'amount_base', 'amount_require_multiple_of', 'amount_type', 'amount_variance_percentage_lower_threshold',
        'amount_variance_percentage_upper_threshold', 'item_id'
    )


class QuestRequirementGeneratorConfigurationItemGroup(QuestSubTypeGeneratorConfiguration):
    """
    Requirement generator item group configuration.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items required by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_type : `int`
        The amount's type.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    item_group_id : `int`
        The required item's identifier.
    """
    __slots__ = (
        'amount_base', 'amount_require_multiple_of', 'amount_type', 'amount_variance_percentage_lower_threshold',
        'amount_variance_percentage_upper_threshold', 'item_group_id'
    )


class QuestRequirementGeneratorChoiceOption(RichAttributeErrorBaseType):
    """
    Option of a requirement choice generator.
    
    Attributes
    ----------
    generator : ``QuestSubTypeGenerator``
        The wrapped generator.
    
    weight : `int`
        The weight of the option to be chosen.
    """
    __slots__ = ('generator', 'weight')


def quest_requirement_generator_choice_option_create(generator, weight):
    """
    Creates a new choice option.

    Parameters
    ----------
    generator : ``QuestSubTypeGenerator``
        The wrapped generator.
    
    weight : `int`
        The weight of the option to be chosen.
    
    Returns
    -------
    option : ``QuestRequirementGeneratorChoiceOption``
    """
    option = object.__new__(QuestRequirementGeneratorChoiceOption)
    option.generator = generator
    option.weight = weight
    return option


def quest_requirement_generator_create_choice(
    options
):
    """
    Creates a choice requirement.
    
    Parameters
    ----------
    options : ``tuple<QuestRequirementGeneratorChoiceOption>``
        Options to choose from.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRequirementGeneratorConfigurationChoice)
    configuration.options = options
    
    return quest_sub_type_generator_create(QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_CHOICE, configuration)


def quest_requirement_generator_create_duration(
    duration_base,
    duration_require_multiple_of,
    duration_variance_percentage_lower_threshold,
    duration_variance_percentage_upper_threshold,
):
    """
    Creates a duration requirement.
    
    Parameters
    ----------
    duration_base : `int`
        The quest's duration in seconds.
    
    duration_require_multiple_of : `int`
        Value to require the duration to be multiple of.
    
    duration_variance_percentage_lower_threshold : `int`
        Lower threshold of for duration variance in percentage.
    
    duration_variance_percentage_upper_threshold : `int`
        Upper threshold of for duration variance in percentage.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRequirementGeneratorConfigurationDuration)
    configuration.duration_base = duration_base
    configuration.duration_require_multiple_of = duration_require_multiple_of
    configuration.duration_variance_percentage_lower_threshold = duration_variance_percentage_lower_threshold
    configuration.duration_variance_percentage_upper_threshold = duration_variance_percentage_upper_threshold

    return quest_sub_type_generator_create(QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_DURATION, configuration)


def quest_requirement_generator_create_expiration(
    expiration,
):
    """
    Creates a expiration requirement.
    
    Parameters
    ----------
    expiration : `DateTime`
        When the quest expires.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRequirementGeneratorConfigurationExpiration)
    configuration.expiration = expiration

    return quest_sub_type_generator_create(QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_EXPIRATION, configuration)


def quest_requirement_generator_create_item_category(
    item_flags,
    amount_type,
    amount_base,
    amount_require_multiple_of,
    amount_variance_percentage_lower_threshold,
    amount_variance_percentage_upper_threshold,
):
    """
    Creates a item category requirement.
    
    Parameters
    ----------
    item_flags : `int`
        The required item flags the items should have.
    
    amount_type : `int`
        The amount's type.
    
    amount_base : `int`
        The amount of items required by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRequirementGeneratorConfigurationItemCategory)
    configuration.amount_base = amount_base
    configuration.amount_require_multiple_of = amount_require_multiple_of
    configuration.amount_type = amount_type
    configuration.amount_variance_percentage_lower_threshold = amount_variance_percentage_lower_threshold
    configuration.amount_variance_percentage_upper_threshold = amount_variance_percentage_upper_threshold
    configuration.item_flags = item_flags

    return quest_sub_type_generator_create(QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_ITEM_CATEGORY, configuration)


def quest_requirement_generator_create_item_exact(
    item_id,
    amount_type,
    amount_base,
    amount_require_multiple_of,
    amount_variance_percentage_lower_threshold,
    amount_variance_percentage_upper_threshold,
):
    """
    Creates a item exact requirement.
    
    Parameters
    ----------
    item_id : `int`
        The required item's identifier.
    
    amount_type : `int`
        The amount's type.
    
    amount_base : `int`
        The amount of items required by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRequirementGeneratorConfigurationItemExact)
    configuration.amount_base = amount_base
    configuration.amount_require_multiple_of = amount_require_multiple_of
    configuration.amount_type = amount_type
    configuration.amount_variance_percentage_lower_threshold = amount_variance_percentage_lower_threshold
    configuration.amount_variance_percentage_upper_threshold = amount_variance_percentage_upper_threshold
    configuration.item_id = item_id

    return quest_sub_type_generator_create(QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_ITEM_EXACT, configuration)


def quest_requirement_generator_create_item_group(
    item_group_id,
    amount_type,
    amount_base,
    amount_require_multiple_of,
    amount_variance_percentage_lower_threshold,
    amount_variance_percentage_upper_threshold,
):
    """
    Creates a item group requirement.
    
    Parameters
    ----------
    item_group_id : `int`
        The required item's identifier.
    
    amount_type : `int`
        The amount's type.
    
    amount_base : `int`
        The amount of items required by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRequirementGeneratorConfigurationItemGroup)
    configuration.amount_base = amount_base
    configuration.amount_require_multiple_of = amount_require_multiple_of
    configuration.amount_type = amount_type
    configuration.amount_variance_percentage_lower_threshold = amount_variance_percentage_lower_threshold
    configuration.amount_variance_percentage_upper_threshold = amount_variance_percentage_upper_threshold
    configuration.item_group_id = item_group_id

    return quest_sub_type_generator_create(QUEST_REQUIREMENT_GENERATOR_BEHAVIOUR_ITEM_GROUP, configuration)
