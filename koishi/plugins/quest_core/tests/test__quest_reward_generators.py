from random import Random

import vampytest

from ..quest_reward_generators import (
    quest_reward_generator_create_balance, quest_reward_generator_create_credibility,
    quest_reward_generator_create_credibility_fix, quest_reward_generator_create_item_exact,
    quest_reward_generator_create_item_exact_fix
)
from ..quest_reward_types import (
    QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_CREDIBILITY_FIX,
    QUEST_REWARD_TYPE_ITEM_EXACT, QUEST_REWARD_TYPE_ITEM_EXACT_FIX
)


def test__quest_reward_generator_create_balance():
    balance_base = 3600
    balance_require_multiple_of = 100
    balance_variance_percentage_lower_threshold = 80
    balance_variance_percentage_upper_threshold = 120
    
    generator = quest_reward_generator_create_balance(
        balance_base,
        balance_require_multiple_of,
        balance_variance_percentage_lower_threshold,
        balance_variance_percentage_upper_threshold,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REWARD_TYPE_BALANCE,
    )
    vampytest.assert_eq(
        generator.configuration.balance_base,
        balance_base,
    )
    vampytest.assert_eq(
        generator.configuration.balance_require_multiple_of,
        balance_require_multiple_of,
    )
    vampytest.assert_eq(
        generator.configuration.balance_variance_percentage_lower_threshold,
        balance_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        generator.configuration.balance_variance_percentage_upper_threshold,
        balance_variance_percentage_upper_threshold,
    )


def test__generate_with_diversion_balance():
    balance_base = 3600
    balance_require_multiple_of = 100
    balance_variance_percentage_lower_threshold = 80
    balance_variance_percentage_upper_threshold = 120
    
    generator = quest_reward_generator_create_balance(
        balance_base,
        balance_require_multiple_of,
        balance_variance_percentage_lower_threshold,
        balance_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = generator.behaviour.generate_with_diversion(
        generator.configuration,
        random_number_generator,
        accumulated_diversion,
    )
    
    vampytest.assert_eq(
        generated.behaviour.type,
        QUEST_REWARD_TYPE_BALANCE,
    )
    vampytest.assert_eq(generated.configuration.balance, 7600)
    
    vampytest.assert_eq(diversion, 0.9473684210526315)


def test__quest_reward_generator_create_credibility():
    credibility_base = 3600
    
    generator = quest_reward_generator_create_credibility(
        credibility_base,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REWARD_TYPE_CREDIBILITY,
    )
    vampytest.assert_eq(
        generator.configuration.credibility_base,
        credibility_base,
    )


def test__generate_with_diversion_credibility():
    credibility_base = 3600
    
    generator = quest_reward_generator_create_credibility(
        credibility_base,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = generator.behaviour.generate_with_diversion(
        generator.configuration,
        random_number_generator,
        accumulated_diversion,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REWARD_TYPE_CREDIBILITY)
    vampytest.assert_eq(generated.configuration.credibility, 7200)
    
    vampytest.assert_eq(diversion, 1.0)


def test__quest_reward_generator_create_credibility_fix():
    credibility_base = 3600
    
    generator = quest_reward_generator_create_credibility_fix(
        credibility_base,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REWARD_TYPE_CREDIBILITY_FIX,
    )
    vampytest.assert_eq(
        generator.configuration.credibility_base,
        credibility_base,
    )


def test__generate_with_diversion_credibility_fix():
    credibility_base = 3600
    
    generator = quest_reward_generator_create_credibility_fix(
        credibility_base,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = generator.behaviour.generate_with_diversion(
        generator.configuration,
        random_number_generator,
        accumulated_diversion,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REWARD_TYPE_CREDIBILITY)
    vampytest.assert_eq(generated.configuration.credibility, credibility_base)
    
    vampytest.assert_eq(diversion, 1.0)


def test__quest_reward_generator_create_item_exact():
    item_id = 4
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_reward_generator_create_item_exact(
        item_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REWARD_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        generator.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        generator.configuration.amount_base,
        amount_base,
    )
    vampytest.assert_eq(
        generator.configuration.amount_require_multiple_of,
        amount_require_multiple_of,
    )
    vampytest.assert_eq(
        generator.configuration.amount_variance_percentage_lower_threshold,
        amount_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        generator.configuration.amount_variance_percentage_upper_threshold,
        amount_variance_percentage_upper_threshold,
    )


def test__generate_with_diversion_item_exact():
    item_id = 4
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_reward_generator_create_item_exact(
        item_id,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = generator.behaviour.generate_with_diversion(
        generator.configuration,
        random_number_generator,
        accumulated_diversion,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REWARD_TYPE_ITEM_EXACT)
    vampytest.assert_eq(generated.configuration.item_id, item_id)
    vampytest.assert_eq(generated.configuration.amount_given, 7600)
    
    vampytest.assert_eq(diversion, 0.9473684210526315)


def test__quest_reward_generator_create_item_exact_fix():
    item_id = 4
    amount_base = 3600
    
    generator = quest_reward_generator_create_item_exact_fix(
        item_id,
        amount_base,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REWARD_TYPE_ITEM_EXACT_FIX,
    )
    vampytest.assert_eq(
        generator.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        generator.configuration.amount_base,
        amount_base,
    )


def test__generate_with_diversion_item_exact_fix():
    item_id = 4
    amount_base = 3600
    
    generator = quest_reward_generator_create_item_exact_fix(
        item_id,
        amount_base,
    )
    
    random_number_generator = Random(5)
    accumulated_diversion = 2.0
    
    generated, diversion = generator.behaviour.generate_with_diversion(
        generator.configuration,
        random_number_generator,
        accumulated_diversion,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REWARD_TYPE_ITEM_EXACT)
    vampytest.assert_eq(generated.configuration.item_id, item_id)
    vampytest.assert_eq(generated.configuration.amount_given, amount_base)
    
    vampytest.assert_eq(diversion, 1.0)
