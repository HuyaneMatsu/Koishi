__all__ = ()

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..balance_rendering import produce_modification_description

from .constants import NUMBER_TH_ENDINGS, NUMBER_TH_ENDING_DEFAULT


def produce_buy_relationship_slot_confirmation_description(
    new_relationship_slot_count,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces buy relationship slot confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    new_relationship_slot_count : `int`
        The relationship slot count after purchase.
    
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
    yield 'Are you sure to buy the '
    yield str(new_relationship_slot_count)
    yield NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)
    yield ' relationship slot'
    
    if (target_user is not None):
        yield ' of '
        yield target_user.name_at(guild_id)
    
    yield '?\n\nIt will cost you '
    yield str(required_balance)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'


def produce_buy_relationship_slot_success_description(
    new_relationship_slot_count,
    current_balance,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces buy relationship slots notification.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    new_relationship_slot_count : `int`
        The relationship slot count after purchase.
    
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
    yield 'You purchased the '
    
    yield str(new_relationship_slot_count)
    yield NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)
    yield ' relationship slot'
    
    if (target_user is not None):
        yield ' of '
        yield target_user.name_at(guild_id)
   
    yield '.\n\nYour '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ':\n'
    yield from produce_modification_description(current_balance, -required_balance)


def produce_buy_relationship_slot_notification_description(
    new_relationship_slot_count,
    source_user,
    guild_id,
):
    """
    Produces buy relationship slots notification.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    new_relationship_slot_count : `int`
        The relationship slot count after purchase.
    
    source_user : `ClientUserBase``
        The purchasing user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' gifted you your '
    yield str(new_relationship_slot_count)
    yield NUMBER_TH_ENDINGS.get(new_relationship_slot_count, NUMBER_TH_ENDING_DEFAULT)
    yield ' relationship slot.'
