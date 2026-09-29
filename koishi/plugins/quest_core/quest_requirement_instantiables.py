__all__ = (
    'quest_requirement_instantiable_create_duration', 'quest_requirement_instantiable_create_expiration',
    'quest_requirement_instantiable_create_item_category', 'quest_requirement_instantiable_create_item_exact',
    'quest_requirement_instantiable_create_item_group'
)

from scarletio import copy_docs

from .quest_requirement_serialisables import (
    quest_requirement_serialisable_create_duration,
    quest_requirement_serialisable_create_expiration, quest_requirement_serialisable_create_item_category,
    quest_requirement_serialisable_create_item_exact, quest_requirement_serialisable_create_item_group
)
from .quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)

from .quest_sub_type_instantiable_bases import (
    QuestSubTypeInstantiableConfiguration, instantiate_base, quest_sub_type_instantiable_behaviour_create,
    quest_sub_type_instantiable_create
)


@copy_docs(instantiate_base)
def instantiate_duration(configuration):
    return quest_requirement_serialisable_create_duration(
        configuration.duration,
    )


@copy_docs(instantiate_base)
def instantiate_expiration(configuration):
    return quest_requirement_serialisable_create_expiration(
        configuration.expiration,
    )


@copy_docs(instantiate_base)
def instantiate_item_category(configuration):
    return quest_requirement_serialisable_create_item_category(
        configuration.item_flags,
        configuration.amount_type,
        configuration.amount_required,
        0,
    )


@copy_docs(instantiate_base)
def instantiate_item_exact(configuration):
    return quest_requirement_serialisable_create_item_exact(
        configuration.item_id,
        configuration.amount_type,
        configuration.amount_required,
        0,
    )


@copy_docs(instantiate_base)
def instantiate_item_group(configuration):
    return quest_requirement_serialisable_create_item_group(
        configuration.item_group_id,
        configuration.amount_type,
        configuration.amount_required,
        0,
    )


QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_DURATION = quest_sub_type_instantiable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_DURATION,
    instantiate_duration,
)

QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_EXPIRATION = quest_sub_type_instantiable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_EXPIRATION,
    instantiate_expiration,
)

QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_ITEM_CATEGORY = quest_sub_type_instantiable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    instantiate_item_category,
)

QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_ITEM_EXACT = quest_sub_type_instantiable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    instantiate_item_exact,
)

QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_ITEM_GROUP = quest_sub_type_instantiable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    instantiate_item_group,
)


class QuestRequirementInstantiableConfigurationDuration(QuestSubTypeInstantiableConfiguration):
    """
    Quest requirement instantiable representing expiration duration.
    
    Attributes
    ----------
    duration : `int`
        After how much seconds the quest expires.
    """
    __slots__ = ('duration',)


class QuestRequirementInstantiableConfigurationExpiration(QuestSubTypeInstantiableConfiguration):
    """
    Quest requirement instantiable representing expiration.
    
    Attributes
    ----------
    expiration : `DateTime`
        When the quest expires.
    """
    __slots__ = ('expiration',)


class QuestRequirementInstantiableConfigurationItemCategory(QuestSubTypeInstantiableConfiguration):
    """
    Quest requirement instantiable representing item category.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_type : `int`
        The amount's type.
    
    item_flags : `int`
        The required item flags the item should have.
    """
    __slots__ = ('amount_required', 'amount_type', 'item_flags')


class QuestRequirementInstantiableConfigurationItemExact(QuestSubTypeInstantiableConfiguration):
    """
    Quest requirement instantiable representing item exact.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_type : `int`
        The amount's type.
    
    item_id : `int`
        The required item's identifier.
    """
    __slots__ = ('amount_required', 'amount_type', 'item_id')


class QuestRequirementInstantiableConfigurationItemGroup(QuestSubTypeInstantiableConfiguration):
    """
    Quest requirement instantiable representing item group.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_type : `int`
        The amount's type.
    
    item_group_id : `int`
        The required items' group's identifier.
    """
    __slots__ = ('amount_required', 'amount_type', 'item_group_id')


def quest_requirement_instantiable_create_duration(duration):
    """
    Creates an instantiable duration quest requirement.
    
    Parameters
    ----------
    duration : `int`
        After how much seconds the quest expires.
    
    Returns
    -------
    quest_requirement_instantiable : ``QuestRequirementInstantiable``
    """
    configuration = object.__new__(QuestRequirementInstantiableConfigurationDuration)
    configuration.duration = duration
    
    return quest_sub_type_instantiable_create(QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_DURATION, configuration)


def quest_requirement_instantiable_create_expiration(expiration):
    """
    Creates an instantiable expiration quest requirement.
    
    Parameters
    ----------
    expiration : `int`
        After how much seconds the quest expires.
    
    Returns
    -------
    quest_requirement_instantiable : ``QuestRequirementInstantiable``
    """
    configuration = object.__new__(QuestRequirementInstantiableConfigurationExpiration)
    configuration.expiration = expiration
    
    return quest_sub_type_instantiable_create(QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_EXPIRATION, configuration)


def quest_requirement_instantiable_create_item_category(item_flags, amount_type, amount_required):
    """
    Creates an instantiable item category quest requirement.
    
    Parameters
    ----------
    item_flags : `int`
        The required item flags the item should have.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The required amount.
    
    Returns
    -------
    quest_requirement_instantiable : ``QuestRequirementInstantiable``
    """
    configuration = object.__new__(QuestRequirementInstantiableConfigurationItemCategory)
    configuration.item_flags = item_flags
    configuration.amount_type = amount_type
    configuration.amount_required = amount_required
    
    return quest_sub_type_instantiable_create(QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_ITEM_CATEGORY, configuration)


def quest_requirement_instantiable_create_item_exact(item_id, amount_type, amount_required):
    """
    Creates an instantiable item exact quest requirement.
    
    Parameters
    ----------
    item_id : `int`
        The required item's identifier.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The required amount.
    
    Returns
    -------
    quest_requirement_instantiable : ``QuestRequirementInstantiable``
    """
    configuration = object.__new__(QuestRequirementInstantiableConfigurationItemExact)
    configuration.item_id = item_id
    configuration.amount_type = amount_type
    configuration.amount_required = amount_required
    
    return quest_sub_type_instantiable_create(QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_ITEM_EXACT, configuration)


def quest_requirement_instantiable_create_item_group(item_group_id, amount_type, amount_required):
    """
    Creates an instantiable item group quest requirement.
    
    Parameters
    ----------
    item_group_id : `int`
        The required items' group's identifier.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The required amount.
    
    Returns
    -------
    quest_requirement_instantiable : ``QuestRequirementInstantiable``
    """
    configuration = object.__new__(QuestRequirementInstantiableConfigurationItemGroup)
    configuration.item_group_id = item_group_id
    configuration.amount_type = amount_type
    configuration.amount_required = amount_required
    
    return quest_sub_type_instantiable_create(QUEST_REQUIREMENT_INSTANTIABLE_BEHAVIOUR_ITEM_GROUP, configuration)
