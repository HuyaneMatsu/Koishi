__all__ = (
    'STAT_CHOICES', 'get_user_stat_name_full_for_index', 'get_user_stat_value_for_index',
    'set_user_stat_value_for_index'
)

from .constants import (
    USER_STAT_NAME_FULL_BEDROOM, USER_STAT_NAME_FULL_CHARM, USER_STAT_NAME_FULL_CUTENESS,
    USER_STAT_NAME_FULL_HOUSEWIFE, USER_STAT_NAME_FULL_LOYALTY
)
from .user_stats import UserStats


STAT_CHOICES = (
    (USER_STAT_NAME_FULL_HOUSEWIFE, 0),
    (USER_STAT_NAME_FULL_CUTENESS, 1),
    (USER_STAT_NAME_FULL_BEDROOM, 2),
    (USER_STAT_NAME_FULL_CHARM, 3),
    (USER_STAT_NAME_FULL_LOYALTY, 4),
)


STAT_NAMES_LONG_BY_INDEX = {
    0 : USER_STAT_NAME_FULL_HOUSEWIFE,
    1 : USER_STAT_NAME_FULL_CUTENESS,
    2 : USER_STAT_NAME_FULL_BEDROOM,
    3 : USER_STAT_NAME_FULL_CHARM,
    4 : USER_STAT_NAME_FULL_LOYALTY,
}

USER_STAT_NAME_FULL_DEFAULT = STAT_NAMES_LONG_BY_INDEX[0]


STAT_DESCRIPTORS_BY_INDEX = {
    0 : UserStats.stat_housewife,
    1 : UserStats.stat_cuteness,
    2 : UserStats.stat_bedroom,
    3 : UserStats.stat_charm,
    4 : UserStats.stat_loyalty,
}

STAT_DESCRIPTOR_DEFAULT = STAT_DESCRIPTORS_BY_INDEX[0]


STAT_ATTRIBUTE_NAMES_BY_INDEX = {
    index : descriptor.__name__ for index, descriptor in STAT_DESCRIPTORS_BY_INDEX.items()
}

STAT_ATTRIBUTE_NAME_DEFAULT = STAT_ATTRIBUTE_NAMES_BY_INDEX[0]


def get_user_stat_name_full_for_index(stat_index):
    """
    Gets the stat name for the given index.
    
    Parameters
    ----------
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    stat_name : `str`
    """
    return STAT_NAMES_LONG_BY_INDEX.get(stat_index, USER_STAT_NAME_FULL_DEFAULT)


def get_user_stat_value_for_index(stats, stat_index):
    """
    Gets the stat by its index.
    
    Parameters
    ----------
    stats : ``UserStats``
        The stats of a user.
    
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    value : `int`
    """
    return STAT_DESCRIPTORS_BY_INDEX.get(stat_index, STAT_DESCRIPTOR_DEFAULT).__get__(stats, type(stats))


def set_user_stat_value_for_index(stats, stat_index, value):
    """
    Gets the stat by its index.
    
    Parameters
    ----------
    stats : ``UserStats``
        The stats of a user.
    
    stat_index : `int`
        The stat's index.
    
    value : `int`
        The value to set.
    
    Returns
    -------
    """
    stats.set(STAT_ATTRIBUTE_NAMES_BY_INDEX.get(stat_index, STAT_ATTRIBUTE_NAME_DEFAULT), value)
