__all__ = ('STAT_CHOICES', 'get_stat_name_full_for_index', 'get_stat_value_for_index', 'set_stat_value_for_index')

from .constants import (
    STAT_NAME_FULL_BEDROOM, STAT_NAME_FULL_CHARM, STAT_NAME_FULL_CUTENESS, STAT_NAME_FULL_HOUSEWIFE,
    STAT_NAME_FULL_LOYALTY
)
from .stats import Stats


STAT_CHOICES = (
    (STAT_NAME_FULL_HOUSEWIFE, 0),
    (STAT_NAME_FULL_CUTENESS, 1),
    (STAT_NAME_FULL_BEDROOM, 2),
    (STAT_NAME_FULL_CHARM, 3),
    (STAT_NAME_FULL_LOYALTY, 4),
)


STAT_NAMES_LONG_BY_INDEX = {
    0 : STAT_NAME_FULL_HOUSEWIFE,
    1 : STAT_NAME_FULL_CUTENESS,
    2 : STAT_NAME_FULL_BEDROOM,
    3 : STAT_NAME_FULL_CHARM,
    4 : STAT_NAME_FULL_LOYALTY,
}

STAT_NAME_FULL_DEFAULT = STAT_NAMES_LONG_BY_INDEX[0]


STAT_DESCRIPTORS_BY_INDEX = {
    0 : Stats.stat_housewife,
    1 : Stats.stat_cuteness,
    2 : Stats.stat_bedroom,
    3 : Stats.stat_charm,
    4 : Stats.stat_loyalty,
}

STAT_DESCRIPTOR_DEFAULT = STAT_DESCRIPTORS_BY_INDEX[0]


STAT_ATTRIBUTE_NAMES_BY_INDEX = {
    index : descriptor.__name__ for index, descriptor in STAT_DESCRIPTORS_BY_INDEX.items()
}

STAT_ATTRIBUTE_NAME_DEFAULT = STAT_ATTRIBUTE_NAMES_BY_INDEX[0]


def get_stat_name_full_for_index(stat_index):
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
    return STAT_NAMES_LONG_BY_INDEX.get(stat_index, STAT_NAME_FULL_DEFAULT)


def get_stat_value_for_index(stats, stat_index):
    """
    Gets the stat by its index.
    
    Parameters
    ----------
    stats : ``Stats``
        The stats of a user.
    
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    value : `int`
    """
    return STAT_DESCRIPTORS_BY_INDEX.get(stat_index, STAT_DESCRIPTOR_DEFAULT).__get__(stats, type(stats))


def set_stat_value_for_index(stats, stat_index, value):
    """
    Gets the stat by its index.
    
    Parameters
    ----------
    stats : ``Stats``
        The stats of a user.
    
    stat_index : `int`
        The stat's index.
    
    value : `int`
        The value to set.
    
    Returns
    -------
    """
    stats.set(STAT_ATTRIBUTE_NAMES_BY_INDEX.get(stat_index, STAT_ATTRIBUTE_NAME_DEFAULT), value)
