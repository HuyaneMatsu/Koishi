__all__ = ()

from scarletio import copy_docs

from .generation_helpers import get_random_value_and_diversity_with_variance
from .quest_reward_instantiables import (
    quest_reward_instantiable_create_balance, quest_reward_instantiable_create_credibility,
    quest_reward_instantiable_create_item_exact
)
from .quest_reward_types import (
    QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_CREDIBILITY_FIX,
    QUEST_REWARD_TYPE_ITEM_EXACT, QUEST_REWARD_TYPE_ITEM_EXACT_FIX
)
from .quest_sub_type_generator_bases import (
    QuestSubTypeGeneratorConfiguration, generate_base, generate_with_diversion_base,
    quest_sub_type_generator_behaviour_create, quest_sub_type_generator_create
)


@copy_docs(generate_with_diversion_base)
def generate_with_diversion_balance(configuration, random_number_generator, accumulated_diversion):
    balance, diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        round(configuration.balance_base * accumulated_diversion),
        configuration.balance_require_multiple_of,
        configuration.balance_variance_percentage_lower_threshold,
        configuration.balance_variance_percentage_upper_threshold,
    )
    
    return (
        quest_reward_instantiable_create_balance(balance),
        (1.0 / diversion),
    )


@copy_docs(generate_with_diversion_base)
def generate_with_diversion_credibility(configuration, random_number_generator, accumulated_diversion):
    credibility = round(configuration.credibility_base * accumulated_diversion)
    
    return (
        quest_reward_instantiable_create_credibility(credibility),
        1.0,
    )


@copy_docs(generate_with_diversion_base)
def generate_with_diversion_credibility_fix(configuration, random_number_generator, accumulated_diversion):
    return (
        quest_reward_instantiable_create_credibility(configuration.credibility_base),
        1.0,
    )


@copy_docs(generate_with_diversion_base)
def generate_with_diversion_item_exact(configuration, random_number_generator, accumulated_diversion):
    amount, diversion = get_random_value_and_diversity_with_variance(
        random_number_generator,
        round(configuration.amount_base * accumulated_diversion),
        configuration.amount_require_multiple_of,
        configuration.amount_variance_percentage_lower_threshold,
        configuration.amount_variance_percentage_upper_threshold,
    )
    
    return (
        quest_reward_instantiable_create_item_exact(configuration.item_id, amount),
        (1.0 / diversion),
    )


@copy_docs(generate_with_diversion_base)
def generate_with_diversion_item_exact_fix(configuration, random_number_generator, accumulated_diversion):
    return (
        quest_reward_instantiable_create_item_exact(configuration.item_id, configuration.amount_base),
        1.0,
    )


QUEST_REWARD_GENERATOR_BEHAVIOUR_BALANCE = quest_sub_type_generator_behaviour_create(
    QUEST_REWARD_TYPE_BALANCE,
    generate_base,
    generate_with_diversion_balance,
)

QUEST_REWARD_GENERATOR_BEHAVIOUR_CREDIBILITY = quest_sub_type_generator_behaviour_create(
    QUEST_REWARD_TYPE_CREDIBILITY,
    generate_base,
    generate_with_diversion_credibility,
)

QUEST_REWARD_GENERATOR_BEHAVIOUR_CREDIBILITY_FIX = quest_sub_type_generator_behaviour_create(
    QUEST_REWARD_TYPE_CREDIBILITY_FIX,
    generate_base,
    generate_with_diversion_credibility_fix,
)

QUEST_REWARD_GENERATOR_BEHAVIOUR_ITEM_EXACT = quest_sub_type_generator_behaviour_create(
    QUEST_REWARD_TYPE_ITEM_EXACT,
    generate_base,
    generate_with_diversion_item_exact,
)

QUEST_REWARD_GENERATOR_BEHAVIOUR_ITEM_EXACT_FIX = quest_sub_type_generator_behaviour_create(
    QUEST_REWARD_TYPE_ITEM_EXACT_FIX,
    generate_base,
    generate_with_diversion_item_exact_fix,
)


class QuestRewardGeneratorConfigurationBalance(QuestSubTypeGeneratorConfiguration):
    """
    Reward generator balance configuration.
    
    Attributes
    ----------
    balance_base : `int`
        The balance given by the quest.
    
    balance_require_multiple_of : `int`
        Value to require the balance to be multiple of.
    
    balance_variance_percentage_lower_threshold : `int`
        Lower threshold of for balance variance in percentage.
    
    balance_variance_percentage_upper_threshold : `int`
        Upper threshold of for balance variance in percentage.
    """
    __slots__ = (
        'balance_base', 'balance_require_multiple_of', 'balance_variance_percentage_lower_threshold',
        'balance_variance_percentage_upper_threshold',
    )


class QuestRewardGeneratorConfigurationCredibility(QuestSubTypeGeneratorConfiguration):
    """
    Reward generator credibility configuration.
    
    Attributes
    ----------
    credibility_base : `int`
        The credibility given by the quest.
    """
    __slots__ = ('credibility_base',)


class QuestRewardGeneratorConfigurationItemExact(QuestSubTypeGeneratorConfiguration):
    """
    Reward generator item exact configuration.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items given by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    item_id : `int`
        The required item's identifier.
    """
    __slots__ = (
        'amount_base', 'amount_require_multiple_of', 'amount_variance_percentage_lower_threshold',
        'amount_variance_percentage_upper_threshold', 'item_id'
    )


class QuestRewardGeneratorConfigurationItemExactFix(QuestSubTypeGeneratorConfiguration):
    """
    Reward generator item group configuration.
    
    Attributes
    ----------
    amount_base : `int`
        The amount of items given by the quest.
    
    item_id : `int`
        The required item's identifier.
    """
    __slots__ = ('amount_base', 'item_id')


def quest_reward_generator_create_balance(
    balance_base,
    balance_require_multiple_of,
    balance_variance_percentage_lower_threshold,
    balance_variance_percentage_upper_threshold,
):
    """
    Creates a balance reward.
    
    Parameters
    ----------
    balance_base : `int`
        The balance given by the quest.
    
    balance_require_multiple_of : `int`
        Value to require the balance to be multiple of.
    
    balance_variance_percentage_lower_threshold : `int`
        Lower threshold of for balance variance in percentage.
    
    balance_variance_percentage_upper_threshold : `int`
        Upper threshold of for balance variance in percentage.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRewardGeneratorConfigurationBalance)
    configuration.balance_base = balance_base
    configuration.balance_require_multiple_of = balance_require_multiple_of
    configuration.balance_variance_percentage_lower_threshold = balance_variance_percentage_lower_threshold
    configuration.balance_variance_percentage_upper_threshold = balance_variance_percentage_upper_threshold

    return quest_sub_type_generator_create(QUEST_REWARD_GENERATOR_BEHAVIOUR_BALANCE, configuration)


def quest_reward_generator_create_credibility(
    credibility_base,
):
    """
    Creates a credibility reward.
    
    Parameters
    ----------
    credibility_base : `int`
        The credibility given by the quest.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRewardGeneratorConfigurationCredibility)
    configuration.credibility_base = credibility_base

    return quest_sub_type_generator_create(QUEST_REWARD_GENERATOR_BEHAVIOUR_CREDIBILITY, configuration)


def quest_reward_generator_create_credibility_fix(
    credibility_base,
):
    """
    Creates a item credibility fix reward.
    
    Parameters
    ----------
    credibility_base : `int`
        The credibility given by the quest.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRewardGeneratorConfigurationCredibility)
    configuration.credibility_base = credibility_base

    return quest_sub_type_generator_create(QUEST_REWARD_GENERATOR_BEHAVIOUR_CREDIBILITY_FIX, configuration)


def quest_reward_generator_create_item_exact(
    item_id,
    amount_base,
    amount_require_multiple_of,
    amount_variance_percentage_lower_threshold,
    amount_variance_percentage_upper_threshold,
):
    """
    Creates a item exact reward.
    
    Parameters
    ----------
    item_id : `int`
        The required item's identifier.
    
    amount_base : `int`
        The amount of items given by the quest.
    
    amount_require_multiple_of : `int`
        Value to require the amount to be multiple of.
    
    amount_variance_percentage_lower_threshold : `int`
        Lower threshold of for amount variance in percentage.
    
    amount_variance_percentage_upper_threshold : `int`
        Upper threshold of for amount variance in percentage.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRewardGeneratorConfigurationItemExact)
    configuration.amount_base = amount_base
    configuration.amount_require_multiple_of = amount_require_multiple_of
    configuration.amount_variance_percentage_lower_threshold = amount_variance_percentage_lower_threshold
    configuration.amount_variance_percentage_upper_threshold = amount_variance_percentage_upper_threshold
    configuration.item_id = item_id

    return quest_sub_type_generator_create(QUEST_REWARD_GENERATOR_BEHAVIOUR_ITEM_EXACT, configuration)


def quest_reward_generator_create_item_exact_fix(
    item_id,
    amount_base,
):
    """
    Creates a item exact fix reward.
    
    Parameters
    ----------
    item_id : `int`
        The required item's identifier.
    
    amount_base : `int`
        The amount of items given by the quest.
    
    Returns
    -------
    generator : ``QuestSubTypeGenerator``
    """
    configuration = object.__new__(QuestRewardGeneratorConfigurationItemExactFix)
    configuration.amount_base = amount_base
    configuration.item_id = item_id

    return quest_sub_type_generator_create(QUEST_REWARD_GENERATOR_BEHAVIOUR_ITEM_EXACT_FIX, configuration)
