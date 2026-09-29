from datetime import datetime as DateTime, timezone as TimeZone
from random import Random

import vampytest

from ...unit_core import AMOUNT_TYPE_WEIGHT

from ..quest_requirement_generators import (
    QUEST_REQUIREMENT_TYPE_CHOICE, QuestRequirementGeneratorChoiceOption,
    quest_requirement_generator_choice_option_create, quest_requirement_generator_create_choice,
    quest_requirement_generator_create_duration, quest_requirement_generator_create_expiration,
    quest_requirement_generator_create_item_category, quest_requirement_generator_create_item_exact,
    quest_requirement_generator_create_item_group
)
from ..quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)
from ..quest_sub_type_generator_bases import QuestSubTypeGenerator


def test__quest_requirement_generator_choice_option_create():
    generator = quest_requirement_generator_create_duration(3600, 100, 100, 100)
    weight = 5
    
    option = quest_requirement_generator_choice_option_create(
        generator,
        weight,
    )
    vampytest.assert_instance(option, QuestRequirementGeneratorChoiceOption)
    vampytest.assert_instance(option.generator, QuestSubTypeGenerator)
    vampytest.assert_instance(option.weight, int)
    
    vampytest.assert_eq(option.generator, generator)
    vampytest.assert_eq(option.weight, weight)


def test__quest_requirement_generator_create_choice():
    options = (
        quest_requirement_generator_choice_option_create(
            quest_requirement_generator_create_duration(3600, 100, 100, 100),
            2.0,
        ),
        quest_requirement_generator_choice_option_create(
            quest_requirement_generator_create_duration(1800, 100, 100, 100),
            1.0,
        ),
    )
    
    generator = quest_requirement_generator_create_choice(
        options,
    )
    vampytest.assert_eq(generator.behaviour.type, QUEST_REQUIREMENT_TYPE_CHOICE)
    vampytest.assert_eq(generator.configuration.options, options)


def test__generate_choice():
    options = (
        quest_requirement_generator_choice_option_create(
            quest_requirement_generator_create_duration(3600, 100, 100, 100),
            2.0,
        ),
        quest_requirement_generator_choice_option_create(
            quest_requirement_generator_create_duration(1800, 100, 100, 100),
            1.0,
        ),
    )
    
    generator = quest_requirement_generator_create_choice(
        options,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = generator.behaviour.generate(
        generator.configuration,
        random_number_generator,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REQUIREMENT_TYPE_DURATION)
    vampytest.assert_eq(generated.configuration.duration, 3600)
    
    vampytest.assert_eq(diversion, 1.0)


def test__quest_requirement_generator_create_duration():
    duration_base = 3600
    duration_require_multiple_of = 100
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_duration(
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REQUIREMENT_TYPE_DURATION,
    )
    vampytest.assert_eq(
        generator.configuration.duration_base,
        duration_base,
    )
    vampytest.assert_eq(
        generator.configuration.duration_require_multiple_of,
        duration_require_multiple_of,
    )
    vampytest.assert_eq(
        generator.configuration.duration_variance_percentage_lower_threshold,
        duration_variance_percentage_lower_threshold,
    )
    vampytest.assert_eq(
        generator.configuration.duration_variance_percentage_upper_threshold,
        duration_variance_percentage_upper_threshold,
    )


def test__generate_duration():
    duration_base = 3600
    duration_require_multiple_of = 100
    duration_variance_percentage_lower_threshold = 80
    duration_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_duration(
        duration_base,
        duration_require_multiple_of,
        duration_variance_percentage_lower_threshold,
        duration_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = generator.behaviour.generate(
        generator.configuration,
        random_number_generator,
    )
    
    vampytest.assert_eq(
        generated.behaviour.type,
        QUEST_REQUIREMENT_TYPE_DURATION,
    )
    vampytest.assert_eq(generated.configuration.duration, 3800)
    
    vampytest.assert_eq(diversion, 0.9473684210526315)


def test__quest_requirement_generator_create_expiration():
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    generator = quest_requirement_generator_create_expiration(
        expiration,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REQUIREMENT_TYPE_EXPIRATION,
    )
    vampytest.assert_eq(
        generator.configuration.expiration,
        expiration,
    )


def test__generate_expiration():
    expiration = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    generator = quest_requirement_generator_create_expiration(
        expiration,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = generator.behaviour.generate(
        generator.configuration,
        random_number_generator,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REQUIREMENT_TYPE_EXPIRATION)
    vampytest.assert_eq(generated.configuration.expiration, expiration)
    
    vampytest.assert_eq(diversion, 1.0)


def test__quest_requirement_generator_create_item_category():
    item_flags = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_item_category(
        item_flags,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    )
    vampytest.assert_eq(
        generator.configuration.item_flags,
        item_flags,
    )
    vampytest.assert_eq(
        generator.configuration.amount_type,
        amount_type,
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


def test__generate_item_category():
    item_flags = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_item_category(
        item_flags,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = generator.behaviour.generate(
        generator.configuration,
        random_number_generator,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY)
    vampytest.assert_eq(generated.configuration.item_flags, item_flags)
    vampytest.assert_eq(generated.configuration.amount_type, amount_type)
    vampytest.assert_eq(generated.configuration.amount_required, 3800)
    
    vampytest.assert_eq(diversion, 1.0555555555555556)


def test__quest_requirement_generator_create_item_exact():
    item_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_item_exact(
        item_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    )
    vampytest.assert_eq(
        generator.configuration.item_id,
        item_id,
    )
    vampytest.assert_eq(
        generator.configuration.amount_type,
        amount_type,
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


def test__generate_item_exact():
    item_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_item_exact(
        item_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = generator.behaviour.generate(
        generator.configuration,
        random_number_generator,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REQUIREMENT_TYPE_ITEM_EXACT)
    vampytest.assert_eq(generated.configuration.item_id, item_id)
    vampytest.assert_eq(generated.configuration.amount_type, amount_type)
    vampytest.assert_eq(generated.configuration.amount_required, 3800)
    
    vampytest.assert_eq(diversion, 1.0555555555555556)



def test__quest_requirement_generator_create_item_group():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_item_group(
        item_group_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    vampytest.assert_eq(
        generator.behaviour.type,
        QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    )
    vampytest.assert_eq(
        generator.configuration.item_group_id,
        item_group_id,
    )
    vampytest.assert_eq(
        generator.configuration.amount_type,
        amount_type,
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


def test__generate_item_group():
    item_group_id = 4
    amount_type = AMOUNT_TYPE_WEIGHT
    amount_base = 3600
    amount_require_multiple_of = 100
    amount_variance_percentage_lower_threshold = 80
    amount_variance_percentage_upper_threshold = 120
    
    generator = quest_requirement_generator_create_item_group(
        item_group_id,
        amount_type,
        amount_base,
        amount_require_multiple_of,
        amount_variance_percentage_lower_threshold,
        amount_variance_percentage_upper_threshold,
    )
    
    random_number_generator = Random(5)
    
    generated, diversion = generator.behaviour.generate(
        generator.configuration,
        random_number_generator,
    )
    
    vampytest.assert_eq(generated.behaviour.type, QUEST_REQUIREMENT_TYPE_ITEM_GROUP)
    vampytest.assert_eq(generated.configuration.item_group_id, item_group_id)
    vampytest.assert_eq(generated.configuration.amount_type, amount_type)
    vampytest.assert_eq(generated.configuration.amount_required, 3800)
    
    vampytest.assert_eq(diversion, 1.0555555555555556)
