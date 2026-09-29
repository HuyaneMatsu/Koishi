__all__ = (
    'quest_reward_serialisable_create_balance', 'quest_reward_serialisable_create_credibility',
    'quest_reward_serialisable_create_item_exact'
)

from struct import Struct

from scarletio import copy_docs

from .quest_reward_types import (
    QUEST_REWARD_TYPE_BALANCE, QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_ITEM_EXACT
)
from .quest_sub_type_serialisable_bases import (
    QuestSubTypeSerialisableConfiguration, deserialise_base, quest_sub_type_serialisable_behaviour_create,
    quest_sub_type_serialisable_create, serialise_base
)


QUEST_REWARD_COMPLETION_STATE_ITEM_EXACT_STRUCT = Struct('<LQ')


@copy_docs(deserialise_base)
def deserialise_balance(data, start_index):
    end_index = start_index + 8
    
    if len(data) < end_index:
        return None
    
    return (
        quest_reward_serialisable_create_balance(
            int.from_bytes(data[start_index : end_index], 'little'),
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_balance(configuration):
    yield configuration.balance.to_bytes(8, 'little')


@copy_docs(deserialise_base)
def deserialise_credibility(data, start_index):
    end_index = start_index + 8
    
    if len(data) < end_index:
        return None
    
    return (
        quest_reward_serialisable_create_credibility(
            int.from_bytes(data[start_index : end_index], 'little'),
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_credibility(configuration):
    yield configuration.credibility.to_bytes(8, 'little')


@copy_docs(deserialise_base)
def deserialise_item_exact(data, start_index):
    end_index = start_index + 12
    
    if len(data) < end_index:
        return None
    
    return (
        quest_reward_serialisable_create_item_exact(
            *QUEST_REWARD_COMPLETION_STATE_ITEM_EXACT_STRUCT.unpack(data[start_index : end_index])
        ),
        end_index,
    )


@copy_docs(serialise_base)
def serialise_item_exact(configuration):
    yield QUEST_REWARD_COMPLETION_STATE_ITEM_EXACT_STRUCT.pack(
        configuration.item_id,
        configuration.amount_given,
    )


QUEST_REWARD_SERIALISABLE_BEHAVIOUR_BALANCE = quest_sub_type_serialisable_behaviour_create(
    QUEST_REWARD_TYPE_BALANCE,
    deserialise_balance,
    serialise_balance,
)

QUEST_REWARD_SERIALISABLE_BEHAVIOUR_CREDIBILITY = quest_sub_type_serialisable_behaviour_create(
    QUEST_REWARD_TYPE_CREDIBILITY,
    deserialise_credibility,
    serialise_credibility,
)

QUEST_REWARD_SERIALISABLE_BEHAVIOUR_ITEM_EXACT = quest_sub_type_serialisable_behaviour_create(
    QUEST_REWARD_TYPE_ITEM_EXACT,
    deserialise_item_exact,
    serialise_item_exact,
)

class QuestRewardSerialisableConfigurationBalance(QuestSubTypeSerialisableConfiguration):
    """
    Quest reward serialisable representing balance.
    
    Attributes
    ----------
    balance : `int`
        Balance given by the quest.
    """
    __slots__ = ('balance',)


class QuestRewardSerialisableConfigurationCredibility(QuestSubTypeSerialisableConfiguration):
    """
    Quest reward serialisable representing credibility.
    
    Attributes
    ----------
    credibility : `int`
        Credibility reward.
    """
    __slots__ = ('credibility',)


class QuestRewardSerialisableConfigurationItemExact(QuestSubTypeSerialisableConfiguration):
    """
    Quest reward serialisable representing item exact.
    
    Attributes
    ----------
    amount_given : `int`
        The given amount.
    
    item_id : `int`
        The given item's identifier.
    """
    __slots__ = ('amount_given', 'item_id')


def quest_reward_serialisable_create_balance(balance):
    """
    Creates an serialisable balance quest reward.
    
    Parameters
    ----------
    balance : `int`
        Balance given by the quest.
    
    Returns
    -------
    quest_reward_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRewardSerialisableConfigurationBalance)
    configuration.balance = balance
    
    return quest_sub_type_serialisable_create(QUEST_REWARD_SERIALISABLE_BEHAVIOUR_BALANCE, configuration)


def quest_reward_serialisable_create_credibility(credibility):
    """
    Creates an serialisable credibility quest reward.
    
    Parameters
    ----------
    credibility : `int`
        Credibility reward.
    
    Returns
    -------
    quest_reward_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRewardSerialisableConfigurationCredibility)
    configuration.credibility = credibility
    
    return quest_sub_type_serialisable_create(QUEST_REWARD_SERIALISABLE_BEHAVIOUR_CREDIBILITY, configuration)


def quest_reward_serialisable_create_item_exact(item_id, amount_given):
    """
    Creates an serialisable item exact quest reward.
    
    Parameters
    ----------
    item_id : `int`
        The given item's identifier.
    
    amount_given : `int`
        The given amount.
    
    Returns
    -------
    quest_reward_serialisable : ``QuestRSubTypeSerialisable``
    """
    configuration = object.__new__(QuestRewardSerialisableConfigurationItemExact)
    configuration.item_id = item_id
    configuration.amount_given = amount_given
    
    return quest_sub_type_serialisable_create(QUEST_REWARD_SERIALISABLE_BEHAVIOUR_ITEM_EXACT, configuration)
