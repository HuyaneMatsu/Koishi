__all__ = (
    'calculate_linked_quest_abandon_credibility_penalty', 'calculate_received_reward_credibility',
    'get_adventurer_level_name', 'get_current_batch_id', 'get_quest_board_resets_at',
    'get_linked_quest_abandon_credibility_penalty', 'get_linked_quest_completion_ratio', 'instantiate_quest',
    'reset_linked_quest'
)

from math import floor
from time import gmtime as unix_time_to_utc_time

from ...bot_utils.time import unix_time_seconds_get

from .helpers import get_quest_template_nullable
from .linked_quest import linked_quest_create
from .linked_quest_completion_states import LINKED_QUEST_COMPLETION_STATE_ACTIVE
from .quest_requirement_serialisables import quest_requirement_serialisable_create_expiration
from .quest_requirement_types import (
    QUEST_REQUIREMENT_TYPE_DURATION, QUEST_REQUIREMENT_TYPE_EXPIRATION, QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP
)
from .quest_reward_types import QUEST_REWARD_TYPE_CREDIBILITY


def _year_month_day_to_days(year, month, day):
    """
    Returns a days number from some epoch. Increments 1 every day.
    
    Parameters
    ----------
    year : `int`
        Year to convert.
    
    month : `int`
        Year to convert.
    
    day : `int`
        Year to convert.
    
    Returns
    -------
    days : `int`
    """
    days = day + (0, 28, 59, 89, 120, 150, 181, 212, 242, 273, 303)[month - 1]
    if (month > 2) and (not (year & 3)) and ((year % 100) or (not (year % 400))):
        days += 1
    
    year -= 1
    days += (year * 365) + (year >> 2) - (year // 100) + (year // 400)
    
    return days


UNIX_EPOCH_DAYS = _year_month_day_to_days(1970, 1, 1)


def get_current_batch_id():
    """
    Returns the current batch identifier.
    
    Returns
    -------
    batch_id : `int`
    """
    utc_time = unix_time_to_utc_time(unix_time_seconds_get())
    return _year_month_day_to_days(utc_time.tm_year, utc_time.tm_mon, utc_time.tm_mday) - UNIX_EPOCH_DAYS


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
    quest_board_resets_at : `int`
    """
    now = unix_time_seconds_get()
    utc_time = unix_time_to_utc_time(now)
    
    hour = utc_time.tm_hour
    minute = utc_time.tm_min
    second = utc_time.tm_sec
    
    return now - (hour * 3600) - (minute * 60) - second + 86400


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
            requirement_type = requirement.behaviour.type
            
            # Since they have different structure, check them separately.
            if requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY:
                amount_submitted = requirement.configuration.amount_submitted
                amount_required = requirement.configuration.amount_required
            
            elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_EXACT:
                amount_submitted = requirement.configuration.amount_submitted
                amount_required = requirement.configuration.amount_required
            
            elif requirement_type == QUEST_REQUIREMENT_TYPE_ITEM_GROUP:
                amount_submitted = requirement.configuration.amount_submitted
                amount_required = requirement.configuration.amount_required
            
            else:
                # No other cases.
                continue
            
            accumulated += min(amount_submitted / amount_required, 1.0)
            count += 1
            continue
    
    if not count:
        return 1.0
    
    return (accumulated / count)


def calculate_linked_quest_abandon_credibility_penalty(reward_credibility, quest_rank, entity_rank, completion_ratio):
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


def get_linked_quest_abandon_credibility_penalty(linked_quest, entity_rank):
    """
    Gets linked quest abandon credibility penalty.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to get the penalty for.
    
    entity_rank : `int`
        The entity's rank to be rewarded.
    
    Returns
    -------
    quest_abandon_penalty : `int`
    """
    while True:
        if linked_quest.created_at + 1800 > unix_time_seconds_get():
            credibility_penalty = 0
            break
        
        rewards = linked_quest.rewards
        if (rewards is None):
            credibility_penalty = 0
            break
        
        for reward in rewards:
            if reward.behaviour.type == QUEST_REWARD_TYPE_CREDIBILITY:
                break
        else:
            credibility_penalty = 0
            break
        
        quest_template = get_quest_template_nullable(linked_quest.template_id)
        credibility_penalty = calculate_linked_quest_abandon_credibility_penalty(
            reward.configuration.credibility,
            (0 if quest_template is None else quest_template.level),
            entity_rank,
            get_linked_quest_completion_ratio(linked_quest),
        )
        break
    
    return credibility_penalty


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
            requirement_serialisables.append(
                requirement_instantiable.behaviour.instantiate(requirement_instantiable.configuration)
            )
            
            if requirement_instantiable.behaviour.type != QUEST_REQUIREMENT_TYPE_DURATION:
                continue
            
            requirement_serialisables.append(quest_requirement_serialisable_create_expiration(
                unix_time_seconds_get() + requirement_instantiable.configuration.duration
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
            reward_serialisables.append(
                reward_instantiable.behaviour.instantiate(reward_instantiable.configuration)
            )
            
            if reward_instantiable.behaviour.type != QUEST_REQUIREMENT_TYPE_DURATION:
                continue
            
            reward_serialisables.append(quest_requirement_serialisable_create_expiration(
                unix_time_seconds_get() + reward_instantiable.configuration.duration
            ))
            continue
        
        reward_serialisables = tuple(reward_serialisables)
    
    return linked_quest_create(
        user_id, guild_id, batch_id, quest.template_id, requirement_serialisables, reward_serialisables
    )
    

def reset_linked_quest(linked_quest):
    """
    Resets the linked quest.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to reset.
    """
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_ACTIVE
    linked_quest.created_at = now = unix_time_seconds_get()
    duration = -1
    
    requirements = linked_quest.requirements
    if (requirements is not None):
        for requirement in requirements:
            requirement_type = requirement.behaviour.type
            if requirement_type == QUEST_REQUIREMENT_TYPE_DURATION:
                duration = requirement.configuration.duration
                continue
            
            if requirement_type == QUEST_REQUIREMENT_TYPE_EXPIRATION:
                if duration != -1:
                    requirement.configuration.expiration = now + duration
                continue
            
            if requirement_type in (
                QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
                QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
                QUEST_REQUIREMENT_TYPE_ITEM_CATEGORY,
            ):
                # At the case of over-submit, keep the extra.
                # Never go under 0 in case the requirement in fact was not fulfilled.
                requirement.configuration.amount_submitted = max(
                    0, requirement.configuration.amount_submitted - requirement.configuration.amount_required
                )
                continue
            
            # No other cases
            continue
