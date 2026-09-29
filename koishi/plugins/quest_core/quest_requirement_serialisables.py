__all__ = (
    'quest_requirement_serialisable_create_duration', 'quest_requirement_serialisable_create_expiration',
    'quest_requirement_serialisable_create_item_category', 'quest_requirement_serialisable_create_item_exact',
    'quest_requirement_serialisable_create_item_group'
)

from datetime import datetime as DateTime, timezone as TimeZone
from struct import Struct

from scarletio import copy_docs

from .quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)
from .quest_sub_type_serialisable_bases import (
    QuestSubTypeSerialisableConfiguration, deserialise_base, quest_sub_type_serialisable_behaviour_create,
    quest_sub_type_serialisable_create, serialise_base
)


QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_CATEGORY_STRUCT = Struct('<QBQQ')
QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_EXACT_STRUCT = Struct('<LBQQ')
QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_GROUP_STRUCT = Struct('<LBQQ')


@copy_docs(deserialise_base)
def deserialise_duration(data, start_index):
    end_index = start_index + 8
    
    if len(data) < end_index:
        return None
    
    return (
        quest_requirement_serialisable_create_duration(
            int.from_bytes(data[start_index : end_index], 'little'),
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_duration(configuration):
    yield configuration.duration.to_bytes(8, 'little')


@copy_docs(deserialise_base)
def deserialise_expiration(data, start_index):
    end_index = start_index + 8
    
    if len(data) < end_index:
        return None
    
    return (
        quest_requirement_serialisable_create_expiration(
            DateTime.fromtimestamp(int.from_bytes(data[start_index : end_index], 'little'), tz = TimeZone.utc),
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_expiration(configuration):
    yield int(configuration.expiration.timestamp()).to_bytes(8, 'little')


@copy_docs(deserialise_base)
def deserialise_item_category(data, start_index):
    end_index = start_index + 25
    
    if len(data) < end_index:
        return None
    
    return (
        quest_requirement_serialisable_create_item_category(
            *QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_CATEGORY_STRUCT.unpack(data[start_index : end_index])
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_item_category(configuration):
    yield QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_CATEGORY_STRUCT.pack(
        configuration.item_flags,
        configuration.amount_type,
        configuration.amount_required,
        configuration.amount_submitted,
    )


@copy_docs(deserialise_base)
def deserialise_item_exact(data, start_index):
    end_index = start_index + 21
    
    if len(data) < end_index:
        return None
    
    return (
        quest_requirement_serialisable_create_item_exact(
            *QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_EXACT_STRUCT.unpack(data[start_index : end_index])
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_item_exact(configuration):
    yield QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_EXACT_STRUCT.pack(
        configuration.item_id,
        configuration.amount_type,
        configuration.amount_required,
        configuration.amount_submitted,
    )


@copy_docs(deserialise_base)
def deserialise_item_group(data, start_index):
    end_index = start_index + 21
    
    if len(data) < end_index:
        return None
    
    return (
        quest_requirement_serialisable_create_item_group(
            *QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_GROUP_STRUCT.unpack(data[start_index : end_index])
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_item_group(configuration):
    yield QUEST_REQUIREMENT_COMPLETION_STATE_ITEM_GROUP_STRUCT.pack(
        configuration.item_group_id,
        configuration.amount_type,
        configuration.amount_required,
        configuration.amount_submitted,
    )


QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_DURATION = quest_sub_type_serialisable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_DURATION,
    deserialise_duration,
    serialise_duration,
)

QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_EXPIRATION = quest_sub_type_serialisable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_EXPIRATION,
    deserialise_expiration,
    serialise_expiration,
)

QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_CATEGORY = quest_sub_type_serialisable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    deserialise_item_category,
    serialise_item_category,
)

QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_EXACT = quest_sub_type_serialisable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    deserialise_item_exact,
    serialise_item_exact,
)

QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_GROUP = quest_sub_type_serialisable_behaviour_create(
    QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    deserialise_item_group,
    serialise_item_group,
)


class QuestRequirementSerialisableConfigurationDuration(QuestSubTypeSerialisableConfiguration):
    """
    Quest requirement serialisable representing expiration duration.
    
    Attributes
    ----------
    duration : `int`
        After how much seconds the quest expires.
    """
    __slots__ = ('duration',)


class QuestRequirementSerialisableConfigurationExpiration(QuestSubTypeSerialisableConfiguration):
    """
    Quest requirement serialisable representing expiration.
    
    Attributes
    ----------
    expiration : `DateTime`
        When the quest expires.
    """
    __slots__ = ('expiration',)


class QuestRequirementSerialisableConfigurationItemCategory(QuestSubTypeSerialisableConfiguration):
    """
    Quest requirement serialisable representing item category.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    amount_type : `int`
        The amount's type.
    
    item_flags : `int`
        The required item flags the item should have.
    """
    __slots__ = ('amount_required', 'amount_submitted', 'amount_type', 'item_flags')


class QuestRequirementSerialisableConfigurationItemExact(QuestSubTypeSerialisableConfiguration):
    """
    Quest requirement serialisable representing item exact.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    amount_type : `int`
        The amount's type.
    
    item_id : `int`
        The required item's identifier.
    """
    __slots__ = ('amount_required', 'amount_submitted', 'amount_type', 'item_id')


class QuestRequirementSerialisableConfigurationItemGroup(QuestSubTypeSerialisableConfiguration):
    """
    Quest requirement serialisable representing item group.
    
    Attributes
    ----------
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    amount_type : `int`
        The amount's type.
    
    item_group_id : `int`
        The required items' group's identifier.
    """
    __slots__ = ('amount_required', 'amount_submitted', 'amount_type', 'item_group_id')


def quest_requirement_serialisable_create_duration(duration):
    """
    Creates an serialisable duration quest requirement.
    
    Parameters
    ----------
    duration : `int`
        After how much seconds the quest expires.
    
    Returns
    -------
    quest_requirement_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRequirementSerialisableConfigurationDuration)
    configuration.duration = duration
    
    return quest_sub_type_serialisable_create(QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_DURATION, configuration)


def quest_requirement_serialisable_create_expiration(expiration):
    """
    Creates an serialisable expiration quest requirement.
    
    Parameters
    ----------
    expiration : `int`
        After how much seconds the quest expires.
    
    Returns
    -------
    quest_requirement_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRequirementSerialisableConfigurationExpiration)
    configuration.expiration = expiration
    
    return quest_sub_type_serialisable_create(QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_EXPIRATION, configuration)


def quest_requirement_serialisable_create_item_category(item_flags, amount_type, amount_required, amount_submitted):
    """
    Creates an serialisable item category quest requirement.
    
    Parameters
    ----------
    item_flags : `int`
        The required item flags the item should have.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    Returns
    -------
    quest_requirement_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRequirementSerialisableConfigurationItemCategory)
    configuration.item_flags = item_flags
    configuration.amount_type = amount_type
    configuration.amount_required = amount_required
    configuration.amount_submitted = amount_submitted
    
    return quest_sub_type_serialisable_create(QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_CATEGORY, configuration)


def quest_requirement_serialisable_create_item_exact(item_id, amount_type, amount_required, amount_submitted):
    """
    Creates an serialisable item exact quest requirement.
    
    Parameters
    ----------
    item_id : `int`
        The required item's identifier.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    Returns
    -------
    quest_requirement_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRequirementSerialisableConfigurationItemExact)
    configuration.item_id = item_id
    configuration.amount_type = amount_type
    configuration.amount_required = amount_required
    configuration.amount_submitted = amount_submitted
    
    return quest_sub_type_serialisable_create(QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_EXACT, configuration)


def quest_requirement_serialisable_create_item_group(item_group_id, amount_type, amount_required, amount_submitted):
    """
    Creates an serialisable item group quest requirement.
    
    Parameters
    ----------
    item_group_id : `int`
        The required items' group's identifier.
    
    amount_type : `int`
        The amount's type.
    
    amount_required : `int`
        The required amount.
    
    amount_submitted : `int`
        The submitted amount.
    
    Returns
    -------
    quest_requirement_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRequirementSerialisableConfigurationItemGroup)
    configuration.item_group_id = item_group_id
    configuration.amount_type = amount_type
    configuration.amount_required = amount_required
    configuration.amount_submitted = amount_submitted
    
    return quest_sub_type_serialisable_create(QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_GROUP, configuration)
