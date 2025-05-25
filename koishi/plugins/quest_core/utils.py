__all__ = ('get_adventurer_level_name', 'get_current_batch_id', 'get_quest_template')

from datetime import datetime as DateTime, timezone as TimeZone
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
