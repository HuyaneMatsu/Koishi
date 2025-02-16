__all__ = ()

from hata import Embed

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import NUMBER_TH_ENDINGS, NUMBER_TH_ENDING_DEFAULT


def build_failure_embed_no_relationship_divorces_self():
    """
    Builds an embed for the case when the user has no relationship divorces.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Suffering from success',
        'You have no divorces.',
    )


def build_failure_embed_no_relationship_divorces_other(user, guild_id):
    """
    Builds an embed for the case when the targeted user has no relationship divorces.
    
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
        f'{user.name_at(guild_id)} has no divorces.',
    )


def build_failure_embed_insufficient_balance_self(required_balance, relationship_divorce_count):
    """
    Builds an embed for the case when the user has insufficient amount of balance.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The relationship divorce count.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Insufficient balance',
        (
            f'You do not have enough available hearts to hire ninjas to locate and burn the divorce papers.\n'
            f'You need {required_balance} {EMOJI__HEART_CURRENCY} to locate and burn your {relationship_divorce_count}'
            f'{NUMBER_TH_ENDINGS.get(relationship_divorce_count, NUMBER_TH_ENDING_DEFAULT)} divorce papers.'
        ),
    )



def build_failure_embed_insufficient_balance_other(required_balance, relationship_divorce_count, user, guild_id):
    """
    Builds an embed for the case when the user has insufficient amount of balance to decrement the relationship
    divorce counter of someone else.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The relationship divorce count.
    
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
            f'You do not have enough available hearts to hire ninjas to locate and burn the divorce papers of '
            f'{user.name_at(guild_id)}.\n'
            f'You need {required_balance} {EMOJI__HEART_CURRENCY} to locate and burn the {relationship_divorce_count}'
            f'{NUMBER_TH_ENDINGS.get(relationship_divorce_count, NUMBER_TH_ENDING_DEFAULT)} divorce papers.'
        ),
    )


def build_question_embed_purchase_confirmation_self(required_balance, relationship_divorce_count):
    """
    Builds an embed to question the user about their purchase. (self target)
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The relationship divorce count.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Confirm your purchase',
        (
            f'Are you sure you want to hire ninjas to locate and burn your {relationship_divorce_count}'
            f'{NUMBER_TH_ENDINGS.get(relationship_divorce_count, NUMBER_TH_ENDING_DEFAULT)} divorce papers for '
            f'{required_balance} {EMOJI__HEART_CURRENCY}?'
        ),
    )


def build_question_embed_purchase_confirmation_other(required_balance, relationship_divorce_count, user, guild_id):
    """
    Builds an embed to question the user about their purchase. (other target)
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The current relationship divorce count.
    
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
            f'Are you sure you want to hire ninjas to locate and burn {user.name_at(guild_id)}\'s '
            f'{relationship_divorce_count}'
            f'{NUMBER_TH_ENDINGS.get(relationship_divorce_count, NUMBER_TH_ENDING_DEFAULT)} divorce papers for '
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
        'Hiring ninjas to locate and burn divorce papers was aborted.',
    )


def build_success_embed_purchase_completed_self(required_balance, relationship_divorce_count):
    """
    Builds embed for the case when the user successfully purchased relationship divorce decrement.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The current relationship divorce count.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        'Purchase successful',
        (
            f'You sent out your hired ninjas to locate and burn your {relationship_divorce_count}'
            f'{NUMBER_TH_ENDINGS.get(relationship_divorce_count, NUMBER_TH_ENDING_DEFAULT)} divorce '
            f'papers for {required_balance} {EMOJI__HEART_CURRENCY}.\n'
            f'They completed the task splendid; the case is cool even in the summer.'
        ),
    )


def build_success_embed_purchase_completed_other(required_balance, relationship_divorce_count, user, guild_id):
    """
    Builds embed for the case when the user successfully purchased a relationship divorce decrement for someone else.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to locate and burn the divorce papers.
    
    relationship_divorce_count : `int`
        The current relationship divorce count.
    
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
            f'You sent out your hired ninjas to locate and burn {user.name_at(guild_id)}\'s '
            f'{relationship_divorce_count}'
            f'{NUMBER_TH_ENDINGS.get(relationship_divorce_count, NUMBER_TH_ENDING_DEFAULT)} divorce '
            f'papers for {required_balance} {EMOJI__HEART_CURRENCY}.\n'
            f'They completed the task splendid; the case is cool even in the summer.'
        ),
    )


def build_notification_embed_other(relationship_divorce_count, source_user, guild_id):
    """
    Builds a notification when the user's divorce counter was decremented by someone else.
    
    Parameters
    ----------
    relationship_divorce_count : `int`
        The current relationship divorce count.
    
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
            f'{source_user.name_at(guild_id)} sent out their hired ninjas to locate and burn your '
            f'{relationship_divorce_count}'
            f'{NUMBER_TH_ENDINGS.get(relationship_divorce_count, NUMBER_TH_ENDING_DEFAULT)} divorce papers.\n'
            f'The task was completed splendid; now you cannot hide and seek with them.'
        ),
    )
