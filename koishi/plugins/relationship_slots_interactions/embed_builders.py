__all__ = ()

from hata import Embed

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import NUMBER_TH_ENDINGS, NUMBER_TH_ENDING_DEFAULT


def build_failure_embed_max_relationship_slots_self():
    """
    Builds an embed for the case when the user reached the maximal amount of relationship slots.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Suffering from success',
        'You reached the maximum amount of relationship slots.',
    )


def build_failure_embed_max_relationship_slots_other(user, guild_id):
    """
    Builds an embed for the case when the targeted user reached the maximal amount of relationship slots.
    
    Parameters
    ----------
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Suffering from success',
        f'{user.name_at(guild_id)} reached their maximum amount of relationship slots.',
    )


def build_failure_embed_insufficient_balance_self(required_balance, new_relationship_slot_count):
    """
    Builds an embed for the case when the user has insufficient amount of balance.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient balance',
        (
            f'You do not have enough available hearts to buy more relationship slots.\n'
            f'You need {required_balance} {EMOJI__HEART_CURRENCY} to buy the {new_relationship_slot_count}'
            f'{NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)} slot.'
        ),
    )


def build_failure_embed_insufficient_balance_other(required_balance, new_relationship_slot_count, user, guild_id):
    """
    Builds an embed for the case when the user has insufficient amount of balance to buy relationship for someone else.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient balance',
        (
            f'You do not have enough available hearts to buy more relationship slots for {user.name_at(guild_id)}.\n'
            f'You need {required_balance} {EMOJI__HEART_CURRENCY} to buy the {new_relationship_slot_count}'
            f'{NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)} slot.'
        ),
    )


def build_question_embed_purchase_confirmation_self(required_balance, new_relationship_slot_count):
    """
    Builds an embed to question the user about their purchase. (self target)
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Confirm your purchase',
        (
            f'Are you sure you want to buy your {new_relationship_slot_count}'
            f'{NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)} relationship slot for '
            f'{required_balance} {EMOJI__HEART_CURRENCY}?'
        ),
    )


def build_question_embed_purchase_confirmation_other(required_balance, new_relationship_slot_count, user, guild_id):
    """
    Builds an embed to question the user about their purchase. (other target)
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Confirm your purchase',
        (
            f'Are you sure you want to buy {user.name_at(guild_id)}\'s {new_relationship_slot_count}'
            f'{NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)} relationship slot for '
            f'{required_balance} {EMOJI__HEART_CURRENCY}?'
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
        'The relationship slot purchase has been cancelled.',
    )


def build_success_embed_purchase_completed_self(required_balance, new_relationship_slot_count):
    """
    Builds embed for the case when the user successfully purchased their new relationship slot.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Purchase successful',
        (
            f'You bought your {new_relationship_slot_count}'
            f'{NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)} relationship slot for '
            f'{required_balance} {EMOJI__HEART_CURRENCY}.'
        ),
    )


def build_success_embed_purchase_completed_other(required_balance, new_relationship_slot_count, user, guild_id):
    """
    Builds embed for the case when the user successfully purchased a new relationship slot of someone else.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Purchase successful',
        (
            f'You bought {user.name_at(guild_id)}\'s {new_relationship_slot_count}'
            f'{NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)} relationship slot for '
            f'{required_balance} {EMOJI__HEART_CURRENCY}.'
        ),
    )
