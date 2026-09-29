from random import Random
from types import FunctionType

import vampytest

from ..quest_sub_type_generator_bases import (
    QuestSubTypeGenerator, QuestSubTypeGeneratorBehaviour, QuestSubTypeGeneratorConfiguration, generate_base,
    generate_with_diversion_base, quest_sub_type_generator_behaviour_create, quest_sub_type_generator_create,
    quest_sub_type_generator_create_base
)


def test__quest_sub_type_generator_behaviour_create():
    sub_type_type = 0
    generate = generate_base
    generate_with_diversion = generate_with_diversion_base
    
    behaviour = quest_sub_type_generator_behaviour_create(
        sub_type_type,
        generate,
        generate_with_diversion,
    )
    
    vampytest.assert_instance(behaviour, QuestSubTypeGeneratorBehaviour)
    vampytest.assert_instance(behaviour.generate, FunctionType)
    vampytest.assert_instance(behaviour.generate_with_diversion, FunctionType)
    vampytest.assert_instance(behaviour.type, int)
    
    vampytest.assert_is(behaviour.generate, generate)
    vampytest.assert_is(behaviour.generate_with_diversion, generate_with_diversion)
    vampytest.assert_eq(behaviour.type, sub_type_type)


def test__quest_sub_type_generator_create():
    behaviour = quest_sub_type_generator_behaviour_create(
        0,
        generate_base,
        generate_with_diversion_base,
    )
    
    configuration = object.__new__(QuestSubTypeGeneratorConfiguration)
    
    generator = quest_sub_type_generator_create(
        behaviour,
        configuration,
    )
    
    vampytest.assert_instance(generator, QuestSubTypeGenerator)
    vampytest.assert_is(generator.behaviour, behaviour)
    vampytest.assert_is(generator.configuration, configuration)


def test__generate_base():
    quest_sub_type_generator = quest_sub_type_generator_create_base()
    
    random_number_generator = Random(5)
    
    generated, diversion = quest_sub_type_generator.behaviour.generate(
        quest_sub_type_generator.configuration,
        random_number_generator,
    )
    
    vampytest.assert_eq(
        generated.behaviour.type,
        0,
    )
    
    vampytest.assert_eq(diversion, 1.0)


def test__generate_with_diversion_base():
    quest_sub_type_generator = quest_sub_type_generator_create_base()
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = quest_sub_type_generator.behaviour.generate_with_diversion(
        quest_sub_type_generator.configuration,
        random_number_generator,
        accumulated_diversion,
    )
    
    vampytest.assert_eq(
        generated.behaviour.type,
        0,
    )
    
    vampytest.assert_eq(diversion, 1.0)
