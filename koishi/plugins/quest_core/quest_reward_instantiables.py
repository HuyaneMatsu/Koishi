__all__ = (
    'quest_reward_instantiable_create_balance', 'quest_reward_instantiable_create_credibility',
    'quest_reward_instantiable_create_item_exact'
)

from scarletio import copy_docs

from .quest_reward_serialisables import (
    quest_reward_serialisable_create_balance, quest_reward_serialisable_create_credibility,
    quest_reward_serialisable_create_item_exact
)
from .quest_reward_types import (
    QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY,
    QUEST_REWARD_TYPE_ITEM_EXACT
)

from .quest_sub_type_instantiable_bases import (
    QuestSubTypeInstantiableConfiguration, instantiate_base, quest_sub_type_instantiable_behaviour_create,
    quest_sub_type_instantiable_create
)


@copy_docs(instantiate_base)
def instantiate_balance(configuration):
    return quest_reward_serialisable_create_balance(
        configuration.balance,
    )


@copy_docs(instantiate_base)
def instantiate_credibility(configuration):
    return quest_reward_serialisable_create_credibility(
        configuration.credibility,
    )


@copy_docs(instantiate_base)
def instantiate_item_exact(configuration):
    return quest_reward_serialisable_create_item_exact(
        configuration.item_id,
        configuration.amount_given,
    )


QUEST_REWARD_INSTANTIABLE_BEHAVIOUR_BALANCE = quest_sub_type_instantiable_behaviour_create(
    QUEST_REWARD_TYPE_BALANCE,
    instantiate_balance,
)

QUEST_REWARD_INSTANTIABLE_BEHAVIOUR_CREDIBILITY = quest_sub_type_instantiable_behaviour_create(
    QUEST_REWARD_TYPE_CREDIBILITY,
    instantiate_credibility,
)

QUEST_REWARD_INSTANTIABLE_BEHAVIOUR_ITEM_EXACT = quest_sub_type_instantiable_behaviour_create(
    QUEST_REWARD_TYPE_ITEM_EXACT,
    instantiate_item_exact,
)


class QuestRewardInstantiableConfigurationBalance(QuestSubTypeInstantiableConfiguration):
    """
    Quest reward instantiable representing balance.
    
    Attributes
    ----------
    balance : `int`
        Balance given by the quest.
    """
    __slots__ = ('balance',)


class QuestRewardInstantiableConfigurationCredibility(QuestSubTypeInstantiableConfiguration):
    """
    Quest reward instantiable representing credibility.
    
    Attributes
    ----------
    credibility : `int`
        Credibility reward.
    """
    __slots__ = ('credibility',)


class QuestRewardInstantiableConfigurationItemExact(QuestSubTypeInstantiableConfiguration):
    """
    Quest reward instantiable representing item exact.
    
    Attributes
    ----------
    amount_given : `int`
        The given amount.
    
    item_id : `int`
        The given item's identifier.
    """
    __slots__ = ('amount_given','item_id')


def quest_reward_instantiable_create_balance(balance):
    """
    Creates an instantiable balance quest reward.
    
    Parameters
    ----------
    balance : `int`
        Balance given by the quest.
    
    Returns
    -------
    quest_reward_instantiable : ``QuestRewardInstantiable``
    """
    configuration = object.__new__(QuestRewardInstantiableConfigurationBalance)
    configuration.balance = balance
    
    return quest_sub_type_instantiable_create(QUEST_REWARD_INSTANTIABLE_BEHAVIOUR_BALANCE, configuration)


def quest_reward_instantiable_create_credibility(credibility):
    """
    Creates an instantiable credibility quest reward.
    
    Parameters
    ----------
    credibility : `int`
        Credibility reward.
    
    Returns
    -------
    quest_reward_instantiable : ``QuestRewardInstantiable``
    """
    configuration = object.__new__(QuestRewardInstantiableConfigurationCredibility)
    configuration.credibility = credibility
    
    return quest_sub_type_instantiable_create(QUEST_REWARD_INSTANTIABLE_BEHAVIOUR_CREDIBILITY, configuration)


def quest_reward_instantiable_create_item_exact(item_id, amount_given):
    """
    Creates an instantiable item exact quest reward.
    
    Parameters
    ----------
    item_id : `int`
        The given item's identifier.
    
    amount_given : `int`
        The given amount.
    
    Returns
    -------
    quest_reward_instantiable : ``QuestRewardInstantiable``
    """
    configuration = object.__new__(QuestRewardInstantiableConfigurationItemExact)
    configuration.item_id = item_id
    configuration.amount_given = amount_given
    
    return quest_sub_type_instantiable_create(QUEST_REWARD_INSTANTIABLE_BEHAVIOUR_ITEM_EXACT, configuration)
