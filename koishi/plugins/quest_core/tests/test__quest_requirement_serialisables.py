import vampytest

from ...unit_core import AMOUNT_TYPE_VALUE

from ..quest_requirement_serialisables import (
    QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_DURATION,
    QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_EXPIRATION, QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_CATEGORY,
    QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_EXACT, QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_GROUP,
    quest_requirement_serialisable_create_duration,
    quest_requirement_serialisable_create_expiration, quest_requirement_serialisable_create_item_category,
    quest_requirement_serialisable_create_item_exact, quest_requirement_serialisable_create_item_group
)
from ..quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)


def test__quest_requirement_serialisable_create_duration():
    duration = 3600
    
    serialisable = quest_requirement_serialisable_create_duration(
        duration,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_DURATION,
    )
    vampytest.assert_eq(
        serialisable.configuration.duration,
        duration,
    )


def test__deserialise_duration():
    duration = 3600
    
    data = duration.to_bytes(8, 'little')
    start_index = 0
    
    serialisable, end_index = QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_DURATION.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_DURATION,
    )
    vampytest.assert_eq(
        serialisable.configuration.duration,
        duration,
    )
    
    vampytest.assert_eq(end_index, 8)


def test__serialise_duration():
    duration = 3600
    
    serialisable = quest_requirement_serialisable_create_duration(
        duration,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        duration.to_bytes(8, 'little'),
    )


def test__quest_requirement_serialisable_create_expiration():
    expiration = 1000000
    
    serialisable = quest_requirement_serialisable_create_expiration(
        expiration,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_EXPIRATION,
    )
    vampytest.assert_eq(
        serialisable.configuration.expiration,
        expiration,
    )


def test__deserialise_expiration():
    expiration = 1000000
    
    data = expiration.to_bytes(8, 'little')
    start_index = 0
    
    serialisable, end_index = QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_EXPIRATION.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_EXPIRATION,
    )
    vampytest.assert_eq(
        serialisable.configuration.expiration,
        expiration,
    )
    
    vampytest.assert_eq(end_index, 8)


def test__serialise_expiration():
    expiration = 1000000
    
    serialisable = quest_requirement_serialisable_create_expiration(
        expiration,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        expiration.to_bytes(8, 'little'),
    )


def test__quest_requirement_serialisable_create_item_category():
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    serialisable = quest_requirement_serialisable_create_item_category(
        item_flags,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_flags,
        item_flags,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_required,
        amount_required,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_submitted,
        amount_submitted,
    )


def test__deserialise_item_category():
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    data = b''.join([
        item_flags.to_bytes(8, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required.to_bytes(8, 'little'),
        amount_submitted.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    serialisable, end_index = QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_CATEGORY.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_flags,
        item_flags,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_required,
        amount_required,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_submitted,
        amount_submitted,
    )
    
    vampytest.assert_eq(end_index, 25)


def test__serialise_item_category():
    item_flags = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    serialisable = quest_requirement_serialisable_create_item_category(
        item_flags,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        b''.join([
            item_flags.to_bytes(8, 'little'),
            amount_type.to_bytes(1, 'little'),
            amount_required.to_bytes(8, 'little'),
            amount_submitted.to_bytes(8, 'little'),
        ])
    )


def test__quest_requirement_serialisable_create_item_exact():
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    serialisable = quest_requirement_serialisable_create_item_exact(
        item_id,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_required,
        amount_required,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_submitted,
        amount_submitted,
    )


def test__deserialise_item_exact():
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    data = b''.join([
        item_id.to_bytes(4, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required.to_bytes(8, 'little'),
        amount_submitted.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    serialisable, end_index = QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_EXACT.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_required,
        amount_required,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_submitted,
        amount_submitted,
    )
    
    vampytest.assert_eq(end_index, 21)


def test__serialise_item_exact():
    item_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    serialisable = quest_requirement_serialisable_create_item_exact(
        item_id,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        b''.join([
            item_id.to_bytes(4, 'little'),
            amount_type.to_bytes(1, 'little'),
            amount_required.to_bytes(8, 'little'),
            amount_submitted.to_bytes(8, 'little'),
        ])
    )


def test__quest_requirement_serialisable_create_item_group():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    serialisable = quest_requirement_serialisable_create_item_group(
        item_group_id,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_group_id,
        item_group_id,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_required,
        amount_required,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_submitted,
        amount_submitted,
    )


def test__deserialise_item_group():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    data = b''.join([
        item_group_id.to_bytes(4, 'little'),
        amount_type.to_bytes(1, 'little'),
        amount_required.to_bytes(8, 'little'),
        amount_submitted.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    serialisable, end_index = QUEST_REQUIREMENT_SERIALISABLE_BEHAVIOUR_ITEM_GROUP.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_group_id,
        item_group_id,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_type,
        amount_type,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_required,
        amount_required,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_submitted,
        amount_submitted,
    )
    
    vampytest.assert_eq(end_index, 21)


def test__serialise_item_group():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_VALUE
    amount_required = 5
    amount_submitted = 4
    
    serialisable = quest_requirement_serialisable_create_item_group(
        item_group_id,
        amount_type,
        amount_required,
        amount_submitted,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        b''.join([
            item_group_id.to_bytes(4, 'little'),
            amount_type.to_bytes(1, 'little'),
            amount_required.to_bytes(8, 'little'),
            amount_submitted.to_bytes(8, 'little'),
        ])
    )
