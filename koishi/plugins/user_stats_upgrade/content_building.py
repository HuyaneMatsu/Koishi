__all__ = ()

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..balance_rendering import produce_modification_description
from ..user_stats_core import (
    USER_STAT_NAME_FULL_BEDROOM, USER_STAT_NAME_FULL_CHARM, USER_STAT_NAME_FULL_CUTENESS, USER_STAT_NAME_FULL_HOUSEWIFE,
    USER_STAT_NAME_FULL_LOYALTY
)


def _produce_stat_listing(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
):
    """
    Produces stat listing.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    Yields
    ------
    part : `str`
    """
    if modify_housewife_by:
        yield '- '
        yield USER_STAT_NAME_FULL_HOUSEWIFE
        yield ' '
        yield str(stat_housewife)
        yield ' -> '
        yield str(stat_housewife + modify_housewife_by)
        
        field_added = True
    else:
        field_added = False
    
    if modify_cuteness_by:
        if field_added:
            yield '\n'
        else:
            field_added = True
        
        yield '- '
        yield USER_STAT_NAME_FULL_CUTENESS
        yield ' '
        yield str(stat_cuteness)
        yield ' -> '
        yield str(stat_cuteness + modify_cuteness_by)
    
    if modify_bedroom_by:
        if field_added:
            yield '\n'
        else:
            field_added = True
        
        yield '- '
        yield USER_STAT_NAME_FULL_BEDROOM
        yield ' '
        yield str(stat_bedroom)
        yield ' -> '
        yield str(stat_bedroom + modify_bedroom_by)
    
    if modify_charm_by:
        if field_added:
            yield '\n'
        else:
            field_added = True
        
        yield '- '
        yield USER_STAT_NAME_FULL_CHARM
        yield ' '
        yield str(stat_charm)
        yield ' -> '
        yield str(stat_charm + modify_charm_by)
    
    if modify_loyalty_by:
        if field_added:
            yield '\n'
        
        yield '- '
        yield USER_STAT_NAME_FULL_LOYALTY
        yield ' '
        yield str(stat_loyalty)
        yield ' -> '
        yield str(stat_loyalty + modify_loyalty_by)


def produce_stat_upgrade_confirmation_description(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces stat upgrade confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'Are you sure to upgrade the following stats'
    
    if target_user is not None:
        yield ' of '
        yield target_user.name_at(guild_id)
    
    yield '?\n\n'
    
    yield from _produce_stat_listing(
        stat_housewife,
        stat_cuteness,
        stat_bedroom,
        stat_charm,
        stat_loyalty,
        modify_housewife_by,
        modify_cuteness_by,
        modify_bedroom_by,
        modify_charm_by,
        modify_loyalty_by,
    )
    
    yield '\n\nIt will cost you '
    yield str(required_balance)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'


def produce_stat_upgrade_success_description(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
    current_balance,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces stat upgrade confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    current_balance : `int`
        The user's current balance.
    
    required_balance : `int`
        The required balance for upgrading.
    
    target_user : ``None | ClientUserBase``
        The targeted user if any.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield 'You upgraded the following stats'
    
    if (target_user is not None):
        yield ' of '
        yield target_user.name_at(guild_id)
    
    yield ':\n\n'
    
    yield from _produce_stat_listing(
        stat_housewife,
        stat_cuteness,
        stat_bedroom,
        stat_charm,
        stat_loyalty,
        modify_housewife_by,
        modify_cuteness_by,
        modify_bedroom_by,
        modify_charm_by,
        modify_loyalty_by,
    )
    
    yield '\n\nYour '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ':\n'
    yield from produce_modification_description(current_balance, -required_balance)


def produce_stat_upgraded_notification_description(
    stat_housewife,
    stat_cuteness,
    stat_bedroom,
    stat_charm,
    stat_loyalty,
    modify_housewife_by,
    modify_cuteness_by,
    modify_bedroom_by,
    modify_charm_by,
    modify_loyalty_by,
    source_user,
    guild_id,
):
    """
    Produces stat upgrade confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    stat_housewife : `int`
        The user's current housewife stat.
    
    stat_cuteness : `int`
        The user's current cuteness stat.
    
    stat_bedroom : `int`
        The user's current bedroom stat.
    
    stat_charm : `int`
        The user's current charm stat.
    
    stat_loyalty : `int`
        The user's current loyalty stat.
    
    modify_housewife_by : `int`
        The amount to modify the housewife stat by.
    
    modify_cuteness_by : `int`
        The amount to modify the cuteness stat by.
    
    modify_bedroom_by : `int`
        The amount to modify the bedroom stat by.
    
    modify_charm_by : `int`
        The amount to modify the charm stat by.
    
    modify_loyalty_by : `int`
        The amount to modify the loyalty stat by.
    
    source_user : ``ClientUserBase``
        The user upgrading the stats.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' upgraded your stats:\n\n'
    
    yield from _produce_stat_listing(
        stat_housewife,
        stat_cuteness,
        stat_bedroom,
        stat_charm,
        stat_loyalty,
        modify_housewife_by,
        modify_cuteness_by,
        modify_bedroom_by,
        modify_charm_by,
        modify_loyalty_by,
    )
