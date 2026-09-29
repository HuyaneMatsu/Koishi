from types import FunctionType

import vampytest

from ..quest_sub_type_serialisable_bases import (
    QUEST_SUB_TYPE_SERIALISABLE_BEHAVIOUR_BASE, QuestSubTypeSerialisable, QuestSubTypeSerialisableBehaviour,
    QuestSubTypeSerialisableConfiguration, deserialise_base, quest_sub_type_serialisable_behaviour_create,
    quest_sub_type_serialisable_create, quest_sub_type_serialisable_create_base, serialise_base
)


def test__quest_sub_type_serialisable_behaviour_create():
    sub_type_type = 0
    deserialise = deserialise_base
    serialise = serialise_base
    
    behaviour = quest_sub_type_serialisable_behaviour_create(
        sub_type_type,
        deserialise,
        serialise,
    )
    
    vampytest.assert_instance(behaviour, QuestSubTypeSerialisableBehaviour)
    vampytest.assert_instance(behaviour.deserialise, FunctionType)
    vampytest.assert_instance(behaviour.serialise, FunctionType)
    vampytest.assert_instance(behaviour.type, int)
    
    vampytest.assert_is(behaviour.deserialise, deserialise)
    vampytest.assert_is(behaviour.serialise, serialise)
    vampytest.assert_eq(behaviour.type, sub_type_type)


def test__quest_sub_type_serialisable_create():
    behaviour = quest_sub_type_serialisable_behaviour_create(
        0,
        deserialise_base,
        serialise_base,
    )
    
    configuration = object.__new__(QuestSubTypeSerialisableConfiguration)
    
    serialisable = quest_sub_type_serialisable_create(
        behaviour,
        configuration,
    )
    
    vampytest.assert_instance(serialisable, QuestSubTypeSerialisable)
    vampytest.assert_is(serialisable.behaviour, behaviour)
    vampytest.assert_is(serialisable.configuration, configuration)


def test__deserialise_base():
    data = b''
    start_index = 0
    
    quest_sub_type_serialisable, end_index = QUEST_SUB_TYPE_SERIALISABLE_BEHAVIOUR_BASE.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        quest_sub_type_serialisable.behaviour.type,
        0,
    )
    
    vampytest.assert_eq(end_index, 0)


def test__serialise_base():
    quest_sub_type_serialisable = quest_sub_type_serialisable_create_base()
    
    output = b''.join([*quest_sub_type_serialisable.behaviour.serialise(
        quest_sub_type_serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        b'',
    )
