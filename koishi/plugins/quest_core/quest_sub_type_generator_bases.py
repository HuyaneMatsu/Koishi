__all__ = ()

from scarletio import RichType

from .quest_sub_type_instantiable_bases import quest_sub_type_instantiable_create_base


def generate_base(quest_sub_type_configuration, random_number_generator):
    """
    Base quest requirement or reward generator.
    
    Parameters
    ----------
    configuration : ``quest_sub_type_configuration``
        Configuration to generate based on.
    
    random_number_generator : `random.Random`
        Random number generator to use.
    
    Returns
    -------
    generated_and_diversion : ``(QuestSubTypeInstantiable, float)``
    """
    return (
        quest_sub_type_instantiable_create_base(),
        1.0,
    )


def generate_with_diversion_base(quest_sub_type_configuration, random_number_generator, accumulated_diversion):
    """
    Base quest requirement or reward generator.
    
    Parameters
    ----------
    configuration : ``QuestSubTypeGeneratorConfiguration``
        Configuration to generate based on.
    
    random_number_generator : `random.Random`
        Random number generator to use.
    
    accumulated_diversion : `float`
        Already accumulated diversion.
    
    Returns
    -------
    generated_and_diversion : ``(QuestSubTypeInstantiable, float)``
    """
    return (
        quest_sub_type_instantiable_create_base(),
        1.0,
    )


class QuestSubTypeGeneratorBehaviour(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base type for quest requirements and rewards which can generate.
    
    Attributes
    ----------
    generate : `Function`
        Generator function.
    
    generate_with_diversion : `FunctionType`
        Generator which also respect already accumulated diversion.
    
    type : `int`
        The generator's type.
    """
    __slots__ = ('generate', 'generate_with_diversion', 'type')


def quest_sub_type_generator_behaviour_create(sub_type_type, generate, generate_with_diversion):
    """
    Creates a quest requirement or reward generator behaviour.
    
    Parameters
    ----------
    sub_type_type : `int`
        The generator's type.
    
    generate : `Function`
        Generator function.
    
    generate_with_diversion : `FunctionType`
        Generator which also respect already accumulated diversion.
    
    Returns
    -------
    behaviour : ``QuestSubTypeGeneratorBehaviour``
    """
    behaviour = object.__new__(QuestSubTypeGeneratorBehaviour)
    behaviour.generate = generate
    behaviour.generate_with_diversion = generate_with_diversion
    behaviour.type = sub_type_type
    return behaviour


QUEST_SUB_TYPE_GENERATOR_BEHAVIOUR_BASE = quest_sub_type_generator_behaviour_create(
    0,
    generate_base,
    generate_with_diversion_base,
)


class QuestSubTypeGenerator(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Quest requirement or reward.
    
    Attributes
    ----------
    behaviour : ``QuestSubTypeGeneratorBehaviour``
        Behaviour of generation.
    
    configuration : ``QuestSubTypeGeneratorConfiguration``
        Configuration to pass to generation.
    """
    __slots__ = ('behaviour', 'configuration')


def quest_sub_type_generator_create(behaviour, configuration):
    """
    Creates a quest requirement or reward generator.
    
    Parameters
    ----------
    behaviour : ``QuestSubTypeGeneratorBehaviour``
        Behaviour of generation.
    
    configuration : ``QuestSubTypeGeneratorConfiguration``
        Configuration to pass to generation.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    generator = object.__new__(QuestSubTypeGenerator)
    generator.behaviour = behaviour
    generator.configuration = configuration
    return generator


def quest_sub_type_generator_create_base():
    """
    Creates a base sub_type.
    
    Returns
    -------
    quest_sub_type_generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestSubTypeGeneratorConfiguration)
    
    return quest_sub_type_generator_create(QUEST_SUB_TYPE_GENERATOR_BEHAVIOUR_BASE, configuration)


class QuestSubTypeGeneratorConfiguration(metaclass = RichType, rich_type_feature_flags = ~0):
    """
    Base type for quest requirement or reward configurations.
    """
    __slots__ = ()
