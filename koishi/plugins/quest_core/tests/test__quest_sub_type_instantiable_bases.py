from types import FunctionType

import vampytest

from ..quest_sub_type_instantiable_bases import (
    QuestSubTypeInstantiable, QuestSubTypeInstantiableBehaviour, QuestSubTypeInstantiableConfiguration,
    instantiate_base, quest_sub_type_instantiable_behaviour_create, quest_sub_type_instantiable_create,
    quest_sub_type_instantiable_create_base
)


def test__quest_sub_type_instantiable_behaviour_create():
    sub_type_type = 0
    instantiate = instantiate_base
    
    behaviour = quest_sub_type_instantiable_behaviour_create(
        sub_type_type,
        instantiate,
    )
    
    vampytest.assert_instance(behaviour, QuestSubTypeInstantiableBehaviour)
    vampytest.assert_instance(behaviour.instantiate, FunctionType)
    vampytest.assert_instance(behaviour.type, int)
    
    vampytest.assert_is(behaviour.instantiate, instantiate)
    vampytest.assert_eq(behaviour.type, sub_type_type)


def test__quest_sub_type_instantiable_create():
    behaviour = quest_sub_type_instantiable_behaviour_create(
        0,
        instantiate_base,
    )
    
    configuration = object.__new__(QuestSubTypeInstantiableConfiguration)
    
    instantiable = quest_sub_type_instantiable_create(
        behaviour,
        configuration,
    )
    
    vampytest.assert_instance(instantiable, QuestSubTypeInstantiable)
    vampytest.assert_is(instantiable.behaviour, behaviour)
    vampytest.assert_is(instantiable.configuration, configuration)


def test__instantiate_base():
    quest_sub_type_instantiable = quest_sub_type_instantiable_create_base()
    
    instantiated = quest_sub_type_instantiable.behaviour.instantiate(
        quest_sub_type_instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        0,
    )
