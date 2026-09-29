__all__ = ('QuestSubTypeSerialisable', 'quest_sub_type_serialisable_create_base',)

from scarletio import RichType


def deserialise_base(data, start_index):
    """
    Creates a new quest requirement completion state or reward from the given raw data.
    
    Parameters
    ----------
    data : `memoryview`
        Data to parse from.
    
    start_index : `int`
        Index to start parsing at.
    
    Returns
    -------
    serialisable_and_end_index : ``None | (QuestSubTypeSerialisable, int>)``
    """
    return (
        quest_sub_type_serialisable_create_base(),
        start_index,
    )


def serialise_base(configuration):
    """
    Serialises the quest requirement or reward serialisable configuration.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    configuration : ``QuestSubTypeSerialisableConfiguration``
        Configuration to serialise.
    
    Yields
    ------
    part : `bytes`
    """
    return
    yield


class QuestSubTypeSerialisableBehaviour(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base type for quest requirements and rewards which can deserialise.
    
    Attributes
    ----------
    deserialise : `Function`
        Deserialiser function.
    
    serialise : `FunctionType`
        Serialiser function.
    
    type : `int`
        The serialisable's type.
    """
    __slots__ = ('deserialise', 'serialise', 'type')


def quest_sub_type_serialisable_behaviour_create(sub_type_type, deserialise, serialise):
    """
    Creates a quest requirement or reward serialisable behaviour.
    
    Parameters
    ----------
    sub_type_type : `int`
        The serialisable's type.
    
    deserialise : `Function`
        Deserialiser function.
    
    serialise : `FunctionType`
        Serialiser function.
    
    Returns
    -------
    behaviour : ``QuestSubTypeSerialisableBehaviour``
    """
    behaviour = object.__new__(QuestSubTypeSerialisableBehaviour)
    behaviour.serialise = serialise
    behaviour.deserialise = deserialise
    behaviour.type = sub_type_type
    return behaviour


QUEST_SUB_TYPE_SERIALISABLE_BEHAVIOUR_BASE = quest_sub_type_serialisable_behaviour_create(
    0,
    deserialise_base,
    serialise_base,
)


class QuestSubTypeSerialisable(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Quest requirement or reward.
    
    Attributes
    ----------
    behaviour : ``QuestSubTypeSerialisableBehaviour``
        Behaviour of serialisation.
    
    configuration : ``QuestSubTypeSerialisableConfiguration``
        Configuration to pass to serialiser.
    """
    __slots__ = ('behaviour', 'configuration')


def quest_sub_type_serialisable_create(behaviour, configuration):
    """
    Creates a quest requirement or reward serialisable.
    
    Parameters
    ----------
    behaviour : ``QuestSubTypeSerialisableBehaviour``
        Behaviour of serialisation.
    
    configuration : ``QuestSubTypeSerialisableConfiguration``
        Configuration to pass to serialiser.
    
    Returns
    -------
    serialisable : ``QuestSubTypeSerialisable``
    """
    serialisable = object.__new__(QuestSubTypeSerialisable)
    serialisable.behaviour = behaviour
    serialisable.configuration = configuration
    return serialisable


def quest_sub_type_serialisable_create_base():
    """
    Creates a base sub_type.
    
    Returns
    -------
    quest_sub_type_serialisable : ``QuestSubTypeSerialisable``
    """
    configuration = object.__new__(QuestSubTypeSerialisableConfiguration)
    
    return quest_sub_type_serialisable_create(QUEST_SUB_TYPE_SERIALISABLE_BEHAVIOUR_BASE, configuration)


class QuestSubTypeSerialisableConfiguration(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base type for quest requirement or reward configurations.
    """
    __slots__ = ()
