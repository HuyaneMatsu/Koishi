from types import FunctionType

import vampytest

from ....unit_core import AMOUNT_TYPE_COUNT

from ...action import ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION
from ...adventure import LOOT_STATE_SUCCESS, adventure_action_create, adventure_create, loot_data_build
from ...location import LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS
from ...target import TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION

from ..goal import (
    GOAL_BEHAVIOUR_DEFAULT, GOAL_BEHAVIOUR_ITEM_EXACT, GOAL_TYPE_ITEM_EXACT, GOAL_TYPE_NONE, Goal, GoalBehaviour,
    GoalConfigurationBase, check_default, deserialise_default, goal_behaviour_create, goal_create, goal_create_default,
    goal_create_item_exact, serialise_default
)


def test__goal_behaviour_create():
    goal_type = GOAL_TYPE_NONE
    deserialise = deserialise_default
    serialise = serialise_default
    check = check_default
    
    behaviour = goal_behaviour_create(
        goal_type,
        deserialise,
        serialise,
        check,
    )
    
    vampytest.assert_instance(behaviour, GoalBehaviour)
    vampytest.assert_instance(behaviour.type, int)
    vampytest.assert_instance(behaviour.deserialise, FunctionType)
    vampytest.assert_instance(behaviour.serialise, FunctionType)
    vampytest.assert_instance(behaviour.check, FunctionType)
    
    vampytest.assert_eq(behaviour.type, goal_type)
    vampytest.assert_is(behaviour.deserialise, deserialise)
    vampytest.assert_is(behaviour.serialise, serialise)
    vampytest.assert_is(behaviour.check, check)


def test__goal_create():
    behaviour = GOAL_BEHAVIOUR_DEFAULT
    configuration = object.__new__(GoalConfigurationBase)
    
    goal = goal_create(
        behaviour,
        configuration,
    )
    
    vampytest.assert_instance(goal, Goal)
    vampytest.assert_instance(goal.behaviour, GoalBehaviour)
    vampytest.assert_instance(goal.configuration, GoalConfigurationBase)
    
    vampytest.assert_is(goal.behaviour, behaviour)
    vampytest.assert_is(goal.configuration, configuration)


def test__goal_create_default():
    goal = goal_create_default()
    
    vampytest.assert_eq(goal.behaviour.type, GOAL_TYPE_NONE)


def test__goal_create_item_exact():
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required = 12
    
    goal = goal_create_item_exact(
        item_id,
        amount_type,
        amount_required,
    )
    
    vampytest.assert_eq(goal.behaviour.type, GOAL_TYPE_ITEM_EXACT)
    vampytest.assert_eq(goal.configuration.item_id, item_id)
    vampytest.assert_eq(goal.configuration.amount_type, amount_type)
    vampytest.assert_eq(goal.configuration.amount_required, amount_required)


def test__check_default():
    adventure = adventure_create(
        202609190000,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    
    goal = goal_create_default()
    
    output = goal.behaviour.check(goal.configuration, adventure)
    
    vampytest.assert_eq(output, False)


def test__serialise_default():
    goal = goal_create_default()
    
    output = b''.join([*goal.behaviour.serialise(goal.configuration)])
    
    vampytest.assert_eq(output, b'')


def test__deserialise_default():
    data = b''
    start_index = 0
    
    output = GOAL_BEHAVIOUR_DEFAULT.deserialise(memoryview(data), start_index)
    
    vampytest.assert_is_not(output, None)
    goal, end_index = output
    vampytest.assert_eq(goal.behaviour.type, GOAL_TYPE_NONE)
    vampytest.assert_eq(end_index, 0)


def test__check_item_exact__false():
    adventure = adventure_create(
        2026091900001,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    
    
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required = 12
    
    goal = goal_create_item_exact(
        item_id,
        amount_type,
        amount_required,
    )
    
    output = goal.behaviour.check(goal.configuration, adventure)
    
    vampytest.assert_eq(output, False)


def test__check_item_exact__true():
    adventure_action_0 = adventure_action_create(
        ACTION_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        1463184000,
        None,
        loot_data_build([
            (LOOT_STATE_SUCCESS, TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION, 20),
        ]),
        0,
        10,
    )
    
    adventure = adventure_create(
        2026091900002,
        LOCATION_ID_HUMAN_VILLAGE_OUTSKIRTS,
        TARGET_ID_HUMAN_VILLAGE_OUTSKIRTS_GARDENING_SCARLET_ONION,
        0,
        0,
        None,
        0,
        100,
        100,
    )
    adventure.action_listing = [adventure_action_0]
    
    
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required = 12
    
    goal = goal_create_item_exact(
        item_id,
        amount_type,
        amount_required,
    )
    
    output = goal.behaviour.check(goal.configuration, adventure)
    
    vampytest.assert_eq(output, False)


def test__serialise_item_exact():
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required = 12
    
    goal = goal_create_item_exact(
        item_id,
        amount_type,
        amount_required,
    )
    output = b''.join([*goal.behaviour.serialise(goal.configuration)])
    
    vampytest.assert_eq(
        output,
        b''.join([
            item_id.to_bytes(4, 'little'),
            amount_type.to_bytes(1, 'little'),
            amount_required.to_bytes(8, 'little'),
        ]),
    )


def test__deserialise_item_exact():
    item_id = 5
    amount_type = AMOUNT_TYPE_COUNT
    amount_required = 12
    
    data = b''.join([
        item_id.to_bytes(4, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    output = GOAL_BEHAVIOUR_ITEM_EXACT.deserialise(memoryview(data), start_index)
    
    vampytest.assert_is_not(output, None)
    goal, end_index = output
    vampytest.assert_eq(goal.behaviour.type, GOAL_TYPE_ITEM_EXACT)
    vampytest.assert_eq(goal.configuration.item_id, item_id)
    vampytest.assert_eq(goal.configuration.amount_type, amount_type)
    vampytest.assert_eq(goal.configuration.amount_required, amount_required)
    vampytest.assert_eq(end_index, 13)
