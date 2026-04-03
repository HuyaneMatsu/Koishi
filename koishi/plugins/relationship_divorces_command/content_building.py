__all__ = ()

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from ..balance_rendering import produce_modification_description

from .constants import NUMBER_TH_ENDINGS, NUMBER_TH_ENDING_DEFAULT


def produce_burn_divorce_papers_confirmation_description(
    relationship_divorces,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces buy relationship slot confirmation description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The amount of divorces the user has.
    
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
    yield 'Are you sure to hire ninjas to locate and burn '
    
    if (target_user is None):
        yield 'your'
    else:
        yield target_user.name_at(guild_id)
        yield '\'s'
    
    yield ' '
    yield str(relationship_divorces)
    yield NUMBER_TH_ENDINGS.get(relationship_divorces, NUMBER_TH_ENDING_DEFAULT)
    yield ' divorce papers?\n\nIt will cost you '
    yield str(required_balance)
    yield ' '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield '.'


def produce_burn_divorce_papers_success_description(
    relationship_divorces,
    current_balance,
    required_balance,
    target_user,
    guild_id,
):
    """
    Produces burn divorce papers notification.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The amount of divorces the user has.
    
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
    yield 'The hired ninjas successfully located and burnt '
    
    if (target_user is None):
        yield 'your'
    else:
        yield target_user.name_at(guild_id)
        yield '\'s'
        
    yield ' '
    yield str(relationship_divorces)
    yield NUMBER_TH_ENDINGS.get(relationship_divorces, NUMBER_TH_ENDING_DEFAULT)
    yield ' divorce papers.\n\nYour '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ':\n'
    yield from produce_modification_description(current_balance, -required_balance)


def produce_burn_divorce_papers_notification_description(
    relationship_divorces,
    source_user,
    guild_id,
):
    """
    Produces burn divorce papers notification.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The amount of divorces the user has.
    
    source_user : `ClientUserBase``
        The purchasing user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield source_user.name_at(guild_id)
    yield ' hired ninjas to locate and burn your '
    yield str(relationship_divorces)
    yield NUMBER_TH_ENDINGS.get(relationship_divorces, NUMBER_TH_ENDING_DEFAULT)
    yield ' divorce papers.'
