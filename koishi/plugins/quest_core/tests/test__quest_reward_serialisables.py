import vampytest

from ..quest_reward_serialisables import (
    QUEST_REWARD_SERIALISABLE_BEHAVIOUR_BALANCE, QUEST_REWARD_SERIALISABLE_BEHAVIOUR_CREDIBILITY,
    QUEST_REWARD_SERIALISABLE_BEHAVIOUR_ITEM_EXACT, quest_reward_serialisable_create_balance,
    quest_reward_serialisable_create_credibility, quest_reward_serialisable_create_item_exact
)
from ..quest_reward_types import (
    QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_ITEM_EXACT
)


def test__quest_reward_serialisable_create_balance():
    balance = 3600
    
    serialisable = quest_reward_serialisable_create_balance(
        balance,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REWARD_TYPE_BALANCE,
    )
    vampytest.assert_eq(
        serialisable.configuration.balance,
        balance,
    )


def test__deserialise_balance():
    balance = 3600
    
    data = balance.to_bytes(8, 'little')
    start_index = 0
    
    serialisable, end_index = QUEST_REWARD_SERIALISABLE_BEHAVIOUR_BALANCE.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REWARD_TYPE_BALANCE,
    )
    vampytest.assert_eq(
        serialisable.configuration.balance,
        balance,
    )
    
    vampytest.assert_eq(end_index, 8)


def test__serialise_balance():
    balance = 3600
    
    serialisable = quest_reward_serialisable_create_balance(
        balance,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        balance.to_bytes(8, 'little'),
    )


def test__quest_reward_serialisable_create_credibility():
    credibility = 3600
    
    serialisable = quest_reward_serialisable_create_credibility(
        credibility,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REWARD_TYPE_CREDIBILITY,
    )
    vampytest.assert_eq(
        serialisable.configuration.credibility,
        credibility,
    )


def test__deserialise_credibility():
    credibility = 3600
    
    data = credibility.to_bytes(8, 'little')
    start_index = 0
    
    serialisable, end_index = QUEST_REWARD_SERIALISABLE_BEHAVIOUR_CREDIBILITY.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REWARD_TYPE_CREDIBILITY,
    )
    vampytest.assert_eq(
        serialisable.configuration.credibility,
        credibility,
    )
    
    vampytest.assert_eq(end_index, 8)


def test__serialise_credibility():
    credibility = 3600
    
    serialisable = quest_reward_serialisable_create_credibility(
        credibility,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        credibility.to_bytes(8, 'little'),
    )


def test__quest_reward_serialisable_create_item_exact():
    item_id = 4
    amount_given = 5
    
    serialisable = quest_reward_serialisable_create_item_exact(
        item_id,
        amount_given,
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REWARD_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_given,
        amount_given,
    )


def test__deserialise_item_exact():
    item_id = 4
    amount_given = 5
    
    data = b''.join([
        item_id.to_bytes(4, 'little'),
        amount_given.to_bytes(8, 'little'),
    ])
    start_index = 0
    
    serialisable, end_index = QUEST_REWARD_SERIALISABLE_BEHAVIOUR_ITEM_EXACT.deserialise(
        memoryview(data), start_index
    )
    
    vampytest.assert_eq(
        serialisable.behaviour.type,
        QUEST_REWARD_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        serialisable.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        serialisable.configuration.amount_given,
        amount_given,
    )
    
    vampytest.assert_eq(end_index, 12)


def test__serialise_item_exact():
    item_id = 4
    amount_given = 5
    
    serialisable = quest_reward_serialisable_create_item_exact(
        item_id,
        amount_given,
    )
    
    output = b''.join([*serialisable.behaviour.serialise(
        serialisable.configuration,
    )])
    
    vampytest.assert_eq(
        output,
        b''.join([
            item_id.to_bytes(4, 'little'),
            amount_given.to_bytes(8, 'little'),
        ])
    )
