__all__ = ('quest_sub_type_instantiable_create_base',)

from scarletio import RichType

from .quest_sub_type_serialisable_bases import quest_sub_type_serialisable_create_base


def instantiate_base(quest_sub_type_instantiable_configuration):
    """
    Instantiates the configuration.
    
    Parameters
    ----------
    quest_sub_type_instantiable_configuration : ``QuestSubTypeInstantiableConfigurationBase``
        Configuration for the instantiator.
    
    Returns
    -------
    serialisable : ``quest_sub_type_serialisable_create_base``
    """
    return quest_sub_type_serialisable_create_base()


class QuestSubTypeInstantiableBehaviour(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base type for quest requirement and rewards which can instantiate.
    
    Attributes
    ----------
    instantiate : `Function`
        Instantiable function.
    
    type : `int`
        The instantiable's type.
    """
    __slots__ = ('instantiate', 'type')


def quest_sub_type_instantiable_behaviour_create(sub_type_type, instantiate):
    """
    Creates a quest requirement or reward instantiable behaviour.
    
    Parameters
    ----------
    sub_type_type : `int`
        The instantiable's type.
    
    instantiate : `Function`
        Instantiable function.
    
    Returns
    -------
    behaviour : ``QuestSubTypeInstantiableBehaviour``
    """
    behaviour = object.__new__(QuestSubTypeInstantiableBehaviour)
    behaviour.instantiate = instantiate
    behaviour.type = sub_type_type
    return behaviour


QUEST_SUB_TYPE_INSTANTIABLE_BEHAVIOUR_BASE = quest_sub_type_instantiable_behaviour_create(
    0,
    instantiate_base,
)


class QuestSubTypeInstantiable(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Quest requirement or reward.
    
    Attributes
    ----------
    behaviour : ``QuestSubTypeInstantiableBehaviour``
        Behaviour of instantiable.
    
    configuration : ``QuestSubTypeInstantiableConfiguration``
        Configuration to pass to instantiator.
    """
    __slots__ = ('behaviour', 'configuration')


def quest_sub_type_instantiable_create(behaviour, configuration):
    """
    Creates a quest requirement or reward instantiable.
    
    Parameters
    ----------
    behaviour : ``QuestSubTypeInstantiableBehaviour``
        Behaviour of instantiable.
    
    configuration : ``QuestSubTypeInstantiableConfiguration``
        Configuration to pass to instantiator.
    
    Returns
    -------
    instantiable : ``QuestSubTypeInstantiable``
    """
    instantiable = object.__new__(QuestSubTypeInstantiable)
    instantiable.behaviour = behaviour
    instantiable.configuration = configuration
    return instantiable


def quest_sub_type_instantiable_create_base():
    """
    Creates a base sub_type.
    
    Returns
    -------
    quest_sub_type_instantiable : ``QuestSubTypeInstantiable``
    """
    configuration = object.__new__(QuestSubTypeInstantiableConfiguration)
    
    return quest_sub_type_instantiable_create(QUEST_SUB_TYPE_INSTANTIABLE_BEHAVIOUR_BASE, configuration)


class QuestSubTypeInstantiableConfiguration(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base type for quest requirement or reward configurations.
    """
    __slots__ = ()
