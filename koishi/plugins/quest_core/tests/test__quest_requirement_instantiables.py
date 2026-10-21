import vampytest

from ...unit_core import AMOUNT_TYPE_VALUE

from ..quest_requirement_instantiables import (
    quest_requirement_instantiable_create_duration, quest_requirement_instantiable_create_expiration,
    quest_requirement_instantiable_create_item_category, quest_requirement_instantiable_create_item_exact,
    quest_requirement_instantiable_create_item_group
)
from ..quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)


def test__quest_requirement_instantiable_create_duration():
    duration = 3600
    
    instantiable = quest_requirement_instantiable_create_duration(
        duration,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_DURATION,
    )
    vampytest.assert_eq(
        instantiable.configuration.duration,
        duration,
    )


def test__instantiate_duration():
    duration = 3600
    
    instantiable = quest_requirement_instantiable_create_duration(
        duration,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REQUIREMENT_TYPE_DURATION,
    )
    vampytest.assert_eq(
        instantiated.configuration.duration,
        duration,
    )


def test__quest_requirement_instantiable_create_expiration():
    expiration = 1000000
    
    instantiable = quest_requirement_instantiable_create_expiration(
        expiration,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_EXPIRATION,
    )
    vampytest.assert_eq(
        instantiable.configuration.expiration,
        expiration,
    )


def test__instantiate_expiration():
    expiration = 1000000
    
    instantiable = quest_requirement_instantiable_create_expiration(
        expiration,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REQUIREMENT_TYPE_EXPIRATION,
    )
    vampytest.assert_eq(
        instantiated.configuration.expiration,
        expiration,
    )


def test__quest_requirement_instantiable_create_item_category():
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    instantiable = quest_requirement_instantiable_create_item_category(
        item_flags,
        amount_type,
        amount_required,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    )
    vampytest.assert_eq(
        instantiable.configuration.item_flags,
        item_flags,
    )
    vampytest.assert_eq(
        instantiable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        instantiable.configuration.amount_required,
        amount_required,
    )


def test__instantiate_item_category():
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    instantiable = quest_requirement_instantiable_create_item_category(
        item_flags,
        amount_type,
        amount_required,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    )
    vampytest.assert_eq(
        instantiated.configuration.item_flags,
        item_flags,
    )
    vampytest.assert_eq(
        instantiated.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        instantiated.configuration.amount_required,
        amount_required,
    )


def test__quest_requirement_instantiable_create_item_exact():
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    instantiable = quest_requirement_instantiable_create_item_exact(
        item_id,
        amount_type,
        amount_required,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        instantiable.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        instantiable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        instantiable.configuration.amount_required,
        amount_required,
    )


def test__instantiate_item_exact():
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    instantiable = quest_requirement_instantiable_create_item_exact(
        item_id,
        amount_type,
        amount_required,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        instantiated.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        instantiated.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        instantiated.configuration.amount_required,
        amount_required,
    )


def test__quest_requirement_instantiable_create_item_group():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    instantiable = quest_requirement_instantiable_create_item_group(
        item_group_id,
        amount_type,
        amount_required,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    )
    vampytest.assert_eq(
        instantiable.configuration.item_group_id,
        item_group_id,
    )
    vampytest.assert_eq(
        instantiable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        instantiable.configuration.amount_required,
        amount_required,
    )


def test__instantiate_item_group():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    
    instantiable = quest_requirement_instantiable_create_item_group(
        item_group_id,
        amount_type,
        amount_required,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    )
    vampytest.assert_eq(
        instantiated.configuration.item_group_id,
        item_group_id,
    )
    vampytest.assert_eq(
        instantiated.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        instantiated.configuration.amount_required,
        amount_required,
    )
