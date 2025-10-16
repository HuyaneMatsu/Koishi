__all__ = (
    'calculate_received_reward_credibility', 'get_adventurer_level_name', 'get_current_batch_id',
    'get_quest_board_resets_at', 'get_quest_template'
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
