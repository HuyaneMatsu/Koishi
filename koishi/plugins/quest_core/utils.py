__all__ = (
    'calculate_received_reward_credibility', 'get_adventurer_level_name', 'get_current_batch_id',
    'get_quest_board_resets_at', 'get_linked_quest_abandon_credibility_penalty', 'get_linked_quest_completion_ratio',
    'instantiate_quest', 'reset_linked_quest'
)

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from math import floor

from .constants import UNIX_EPOCH
from .linked_quest import LinkedQuest
from .linked_quest_completion_states import LINKED_QUEST_COMPLETION_STATE_ACTIVE
from .quest_requirement_serialisables import QuestRequirementSerialisableExpiration
from .quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)


def get_current_batch_id():
    """
    Returns the current batch identifier.
    
    Returns
    -------
    batch_id : `int`
    """
    return floor((DateTime.now(TimeZone.utc) - UNIX_EPOCH).total_seconds()) // 86400


def get_adventurer_level_name(level):
    """
    Returns the adventurer level's name.
    
    Parameters
    ----------
    level : `int`
        Adventurer level.
    
    Returns
    -------
    name : `str`
    """
    if level < 8:
        name = chr(b'H'[0] - level)
    
    elif level == 8:
        name = 'S'
    
    else:
        name = 'S' + '+' * (level - 8)
    
    return name


def calculate_received_reward_credibility(reward_credibility, quest_rank, entity_rank):
    """
    Calculates the reward credibility.
    
    Parameters
    ----------
    reward_credibility : `int`
        The amount of credibility to be rewarded.
    
    quest_rank : `int`
        The quest's rank.
    
    entity_rank : `int`
        The entity's rank to be rewarded.
    
    Returns
    -------
    received_reward_credibility : `int`
    """
    if quest_rank >= entity_rank:
        return reward_credibility
    
    return max(floor(reward_credibility * 3 / (3 + entity_rank - quest_rank)), 1)


def get_quest_board_resets_at():
    """
    Gets the time when the quest board will reset at.
    
    returns
    -------
    quest_board_resets_at : ``DateTime``
    """
    return DateTime.now(TimeZone.utc).replace(hour = 0, minute = 0, second = 0, microsecond = 0) + TimeDelta(days = 1)


def get_linked_quest_completion_ratio(linked_quest):
    """
    Returns in what ratio is the quest completed at.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        inked quest to get ratio of.
    
    Returns
    -------
    completion_ratio : `float`
    """
    accumulated = 0.0
    count = 0
    
    requirements = linked_quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            requirement_type = requirement.TYPE
            
            # Since they have different structure, check them separately.
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
                amount_submitted = requirement.amount_submitted
                amount_required = requirement.amount_required
            
            elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
                amount_submitted = requirement.amount_submitted
                amount_required = requirement.amount_required
            
            elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
                amount_submitted = requirement.amount_submitted
                amount_required = requirement.amount_required
            
            else:
                # No other cases.
                continue
            
            accumulated += min(amount_submitted / amount_required, 1.0)
            count += 1
            continue
    
    if not count:
        return 1.0
    
    return (accumulated / count)


def get_linked_quest_abandon_credibility_penalty(reward_credibility, quest_rank, entity_rank, completion_ratio):
    """
    Calculates abandon credibility penalty.
    
    Parameters
    ----------
    reward_credibility : `int`
        The amount of credibility to be rewarded.
    
    quest_rank : `int`
        The quest's rank.
    
    entity_rank : `int`
        The entity's rank to be rewarded.
    
    Returns
    -------
    quest_abandon_penalty : `int`
    """
    if not reward_credibility:
        return 0
    
    if quest_rank >= entity_rank:
        rank_difference = 0
    else:
        rank_difference = entity_rank - quest_rank
    
    return floor(reward_credibility * (3 + rank_difference) / (1.5 * (1.0 + completion_ratio)))


def instantiate_quest(user_id, guild_id, batch_id, quest):
    """
    Instantiates a quest.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to bind to.
    
    guild_id : `int`
        The respective guild's identifier.
    
    batch_id : `int`
        The identifier of the batch. Used for deduplication.
    
    quest : ``Quest``
        Quest to instantiate.
    
    Returns
    -------
    linked_quest : ``LinkedQuest``
    """
    # requirements
    requirement_instantiables = quest.requirements
    if requirement_instantiables is None:
        requirement_serialisables = None
    else:
        requirement_serialisables = []
        
        for requirement_instantiable in requirement_instantiables:
            requirement_serialisables.append(requirement_instantiable.instantiate())
            
            if requirement_instantiable.TYPE != QUEST_REQUIREMENT_TYPE_DURATION:
                continue
            
            requirement_serialisables.append(QuestRequirementSerialisableExpiration(
                DateTime.now(TimeZone.utc) + TimeDelta(seconds = requirement_instantiable.duration)
            ))
            continue
        
        requirement_serialisables = tuple(requirement_serialisables)
    
    # rewards
    reward_instantiables = quest.rewards
    if reward_instantiables is None:
        reward_serialisables = None
    else:
        reward_serialisables = []
        
        for reward_instantiable in reward_instantiables:
            reward_serialisables.append(reward_instantiable.instantiate())
            
            if reward_instantiable.TYPE != QUEST_REQUIREMENT_TYPE_DURATION:
                continue
            
            reward_serialisables.append(QuestRequirementSerialisableExpiration(
                DateTime.now(TimeZone.utc) + TimeDelta(seconds = reward_instantiable.duration)
            ))
            continue
        
        reward_serialisables = tuple(reward_serialisables)
    
    return LinkedQuest(user_id, guild_id, batch_id, quest.template_id, requirement_serialisables, reward_serialisables)
    

def reset_linked_quest(linked_quest):
    """
    Resets the linked quest.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to reset.
    """
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_ACTIVE
    duration = -1
    
    requirements = linked_quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            requirement_type = requirement.TYPE
            if requirement_type == QUEST_REQUIREMENT_TYPE_DURATION:
                duration = requirement.duration
                continue
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_EXPIRATION:
                if duration != -1:
                    requirement.expiration = DateTime.now(TimeZone.utc) + TimeDelta(seconds = duration)
                continue
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
                requirement.amount_submitted = 0
                continue
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
                requirement.amount_submitted = 0
                continue
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
                requirement.amount_submitted = 0
                continue
            
            # No other cases
            continue
