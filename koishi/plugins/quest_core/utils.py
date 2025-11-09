__all__ = (
    'calculate_received_reward_credibility', 'get_adventurer_level_name', 'get_current_batch_id',
    'get_quest_board_resets_at', 'get_linked_quest_abandon_credibility_penalty', 'get_linked_quest_completion_ratio',
    'get_quest_template'
)

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from math import floor

from .constants import QUEST_TEMPLATES, UNIX_EPOCH


def get_quest_template(quest_template_id):
    """
    Returns the quest template with the given identifier.
    
    Parameters
    ----------
    quest_template_id : `int`
        The quest template's identifier.
    
    Returns
    -------
    quest_template : ``None | QuestTemplate``
    """
    return QUEST_TEMPLATES.get(quest_template_id, None)


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
        name = 'S+'
    
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
    return min(linked_quest.amount_submitted / linked_quest.amount_required, 1.0)


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
