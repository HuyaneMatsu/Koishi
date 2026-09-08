__all__ = ()

from math import log

from ..user_stats_core import (
    USER_STAT_NAME_FULL_BEDROOM, USER_STAT_NAME_FULL_CHARM, USER_STAT_NAME_FULL_CUTENESS, USER_STAT_NAME_FULL_HOUSEWIFE,
    USER_STAT_NAME_FULL_LOYALTY, user_stats_calculate
)

from ..unit_core import produce_speed, produce_weight


def _produce_stat_increase(name, stat_base, stat_calculated):
    """
    Produces a stat increase.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        The stat's name.
    
    stat_base : `int`
        The base of the stat.
    
    stat_calculated : `int`
        The calculated stats.
    
    Yields
    ------
    part : `str`
    """
    yield name
    yield ': '
    
    if stat_base == stat_calculated:
        yield str(stat_base)
    
    else:
        if stat_calculated > stat_base:
            sign = '+'
            difference = stat_calculated - stat_base
        else:
            sign = '-'
            difference = stat_base - stat_calculated
        
        yield str(stat_calculated)
        yield ' ('
        yield str(stat_base)
        yield ' '
        yield sign
        yield ' '
        yield str(difference)
        yield ')'


def produce_user_stats_primary_description(user_stats):
    """
    Produces user stats primary description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats
    
    Yields
    ------
    part : `str`
    """
    user_stats_calculated = user_stats_calculate(user_stats)
    yield from _produce_stat_increase(
        USER_STAT_NAME_FULL_HOUSEWIFE, user_stats.stat_housewife, user_stats_calculated.stat_housewife
    )
    yield '\n'
    yield from _produce_stat_increase(
        USER_STAT_NAME_FULL_CUTENESS, user_stats.stat_cuteness, user_stats_calculated.stat_cuteness
    )
    yield '\n'
    yield from _produce_stat_increase(
        USER_STAT_NAME_FULL_BEDROOM, user_stats.stat_bedroom, user_stats_calculated.stat_bedroom
    )
    yield '\n'
    yield from _produce_stat_increase(
        USER_STAT_NAME_FULL_CHARM, user_stats.stat_charm, user_stats_calculated.stat_charm
    )
    yield '\n'
    yield from _produce_stat_increase(
        USER_STAT_NAME_FULL_LOYALTY, user_stats.stat_loyalty, user_stats_calculated.stat_loyalty
    )


def _produce_stat_with_diminishing_multiplier(name, stat):
    """
    Produces a stat with diminishing multiplier.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        The stat's name.
    
    stat : `int`
        The stats' value.
    
    Yields
    ------
    part : `str`
    """
    yield name
    yield ': '
    yield str(stat)
    yield ' ('
    
    if stat > 1:
        multiplier = log(stat) / 2.302585092994046
    elif stat == 1:
        multiplier = 0.15
    else:
        multiplier = 0.05
    
    if multiplier >= 1.0:
        sign = '+'
        value = multiplier - 1.0
    else:
        sign = '-'
        value = 1.0 - multiplier
    
    value *= 100.0
    
    yield sign
    yield format(value, '.0f')
    yield '%)'


def produce_user_stats_secondary_description(user_stats):
    """
    Produces user stats secondary description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_stats : ``UserStats``
        The user's stats
    
    Yields
    ------
    part : `str`
    """
    user_stats_calculated = user_stats_calculate(user_stats)
    
    yield 'Health: '
    yield str(user_stats_calculated.extra_health)
    yield '\nEnergy: '
    yield str(user_stats_calculated.extra_energy)
    yield '\nMovement: '
    yield from produce_speed(user_stats_calculated.extra_movement)
    yield ' (m/s)\nInventory: '
    yield from produce_weight(user_stats_calculated.extra_inventory)
    yield ' (kg)\n\n'
    yield from _produce_stat_with_diminishing_multiplier('Butchering', user_stats_calculated.extra_butchering)
    yield '\n'
    yield from _produce_stat_with_diminishing_multiplier('Fishing', user_stats_calculated.extra_fishing)
    yield '\n'
    yield from _produce_stat_with_diminishing_multiplier('Foraging', user_stats_calculated.extra_foraging)
    yield '\n'
    yield from _produce_stat_with_diminishing_multiplier('Gardening', user_stats_calculated.extra_gardening)
    yield '\n'
    yield from _produce_stat_with_diminishing_multiplier('Hunting', user_stats_calculated.extra_hunting)
