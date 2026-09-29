import vampytest

from ..quest_reward_instantiables import (
    quest_reward_instantiable_create_balance, quest_reward_instantiable_create_credibility,
    quest_reward_instantiable_create_item_exact,
)
from ..quest_reward_types import (
    QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_ITEM_EXACT
)


def test__quest_reward_instantiable_create_balance():
    balance = 3600
    
    instantiable = quest_reward_instantiable_create_balance(
        balance,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REWARD_TYPE_BALANCE,
    )
    vampytest.assert_eq(
        instantiable.configuration.balance,
        balance,
    )


def test__instantiate_balance():
    balance = 3600
    
    instantiable = quest_reward_instantiable_create_balance(
        balance,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REWARD_TYPE_BALANCE,
    )
    vampytest.assert_eq(
        instantiated.configuration.balance,
        balance,
    )


def test__quest_reward_instantiable_create_credibility():
    credibility = 3600
    
    instantiable = quest_reward_instantiable_create_credibility(
        credibility,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REWARD_TYPE_CREDIBILITY,
    )
    vampytest.assert_eq(
        instantiable.configuration.credibility,
        credibility,
    )


def test__instantiate_credibility():
    credibility = 3600
    
    instantiable = quest_reward_instantiable_create_credibility(
        credibility,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REWARD_TYPE_CREDIBILITY,
    )
    vampytest.assert_eq(
        instantiated.configuration.credibility,
        credibility,
    )


def test__quest_reward_instantiable_create_item_exact():
    item_id = 4
    amount_given = 5
    
    instantiable = quest_reward_instantiable_create_item_exact(
        item_id,
        amount_given,
    )
    
    vampytest.assert_eq(
        instantiable.behaviour.type,
        QUEST_REWARD_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        instantiable.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        instantiable.configuration.amount_given,
        amount_given,
    )


def test__instantiate_item_exact():
    item_id = 4
    amount_given = 5
    
    instantiable = quest_reward_instantiable_create_item_exact(
        item_id,
        amount_given,
    )
    
    instantiated = instantiable.behaviour.instantiate(
        instantiable.configuration,
    )
    
    vampytest.assert_eq(
        instantiated.behaviour.type,
        QUEST_REWARD_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        instantiated.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        instantiated.configuration.amount_given,
        amount_given,
    )
