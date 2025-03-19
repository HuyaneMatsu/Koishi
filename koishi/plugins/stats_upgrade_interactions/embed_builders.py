__all__ = ()

from hata import Embed

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..stats_core import get_stat_name_full_for_index
from ..balance_rendering import add_self_balance_modification_embed_field


def build_failure_embed_insufficient_available_balance_self(
    required_balance, available_balance, stat_index, stat_value_after
):
    """
    Builds a failure embed for the case when available balance is lower than the required.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    available_balance : `int`
        Available balance.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient available balance',
        (
            f'You cannot upgrade your {get_stat_name_full_for_index(stat_index)} to {stat_value_after} '
            f'because you have only {available_balance} available {EMOJI__HEART_CURRENCY} which is lower than the '
            f'required {required_balance} {EMOJI__HEART_CURRENCY}.'
        ),
    )


def build_failure_embed_insufficient_available_balance_other(
    required_balance, available_balance, stat_index, stat_value_after, user, guild_id
):
    """
    Builds a failure embed for the case when available balance is lower than the required when purchasing for someone
    else.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    available_balance : `int`
        Available balance.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The current guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient available balance',
        (
            f'You cannot upgrade {user.name_at(guild_id)}\'s {get_stat_name_full_for_index(stat_index)} to '
            f'{stat_value_after} because you have only {available_balance} available {EMOJI__HEART_CURRENCY} which is '
            f'lower than the required {required_balance} {EMOJI__HEART_CURRENCY}.'
        ),
    )


def build_question_embed_purchase_confirmation_self(required_balance, stat_index, stat_value_after):
    """
    Questions the user about their purchase.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Stat upgrade',
        (
            f'Are you sure to upgrade your {get_stat_name_full_for_index(stat_index)} to {stat_value_after} for '
            f'{required_balance} {EMOJI__HEART_CURRENCY}?'
        ),
    )


def build_question_embed_purchase_confirmation_other(required_balance, stat_index, stat_value_after, user, guild_id):
    """
    Questions the user about their purchase targeting an other user.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The current guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Stat upgrade',
        (
            f'Are you sure to upgrade {user.name_at(guild_id)}\'s {get_stat_name_full_for_index(stat_index)} to '
            f'{stat_value_after} for {required_balance} {EMOJI__HEART_CURRENCY}?'
        ),
    )


def build_success_embed_purchase_cancelled():
    """
    Builds embed to show when the user successfully cancelled their purchase.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Purchase cancelled',
    )


def build_success_embed_purchase_completed_self(balance_before, required_balance, stat_index, stat_value_after):
    """
    Builds embed for the case when the user successfully upgraded their stats.
    
    Parameters
    ----------
    balance_before : `int`
        The user's balance before its purchase.
    
    required_balance : `int`
        The required amount of balance for the purchase.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Purchase successful',
        f'You upgraded your {get_stat_name_full_for_index(stat_index)} to {stat_value_after}.',
    )
    return add_self_balance_modification_embed_field(embed, balance_before, -required_balance)


def build_success_embed_purchase_completed_other(
    balance_before, required_balance, stat_index, stat_value_after, user, guild_id
):
    """
    Builds embed for the case when the user successfully upgraded someone else's stats.
    
    Parameters
    ----------
    balance_before : `int`
        The user's balance before its purchase.
    
    required_balance : `int`
        The required amount of balance for the purchase.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The current guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Purchase successful',
        f'You upgraded {user.name_at(guild_id)}\'s {get_stat_name_full_for_index(stat_index)} to {stat_value_after}.',
    )
    
    return add_self_balance_modification_embed_field(embed, balance_before, -required_balance)


def build_notification_embed_other(stat_index, stat_value_after, source_user, guild_id):
    """
    Builds a notification when the user's stats were upgraded.
    
    Parameters
    ----------
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    source_user : `ClientUserBase``
        The user who bought the role.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Love is in the air',
        (
            f'{source_user.name_at(guild_id)} upgraded your {get_stat_name_full_for_index(stat_index)} to '
            f'{stat_value_after}.'
        ),
    )
