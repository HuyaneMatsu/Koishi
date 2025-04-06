__all__ = ('HEARTS_FIELD_CHOICES', 'HEARTS_FIELD_NAME_SHORT', 'HEARTS_FIELD_NAME_TO_RESPONSE_BUILDER')

from hata import ClientUserBase
from hata.ext.slash import InteractionResponse

from .embed_building import (
    build_daily_embed_extended, build_daily_embed_short, build_stats_embed, build_vote_embed_extended
)
from .queries import get_generic_heart_fields, get_generic_vote_fields, get_stat_fields


async def build_response_daily_short(interaction_event, target_user):
    """
    Creates a daily (short) response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        the targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    balance, streak, ready_to_claim = await get_generic_heart_fields(target_user.id)
    return InteractionResponse(
        embed = build_daily_embed_short(interaction_event, target_user, balance, streak, ready_to_claim),
        allowed_mentions = None,
    )
    


async def build_response_daily_extended(interaction_event, target_user):
    """
    Creates a daily (extended) response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        the targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    balance, streak, ready_to_claim = await get_generic_heart_fields(target_user.id)
    return InteractionResponse(
        embed = build_daily_embed_extended(interaction_event, target_user, balance, streak, ready_to_claim),
        allowed_mentions = None,
    )


async def build_response_vote_extended(interaction_event, target_user):
    """
    Creates a vote (extended) response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        the targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    balance, streak, ready_to_vote = await get_generic_vote_fields(target_user.id)
    return InteractionResponse(
        embed = build_vote_embed_extended(interaction_event, target_user, balance, streak, ready_to_vote),
        allowed_mentions = None,
    )


async def build_response_heart_stats(interaction_event, target_user):
    """
    Creates a heart stats response.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : ``ClientUserBase``
        the targeted user.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    (
        balance,
        streak,
        count_daily_self,
        count_daily_by_related,
        count_daily_for_related,
        count_top_gg_vote,
    ) = await get_stat_fields(target_user.id)
    
    return InteractionResponse(
        embed = build_stats_embed(
            interaction_event,
            target_user,
            balance,
            streak,
            count_daily_self,
            count_daily_by_related,
            count_daily_for_related,
            count_top_gg_vote,
        ),
        allowed_mentions = None,
    )


HEARTS_FIELD_NAME_SHORT = 'short'
HEARTS_FIELD_NAME_DAILY_EXTENDED = 'daily-extended'
HEARTS_FIELD_NAME_VOTE_EXTENDED = 'vote-extended'
HEARTS_FIELD_NAME_STATS = 'stats'

HEARTS_FIELD_CHOICES = [
    HEARTS_FIELD_NAME_SHORT,
    HEARTS_FIELD_NAME_DAILY_EXTENDED,
    HEARTS_FIELD_NAME_VOTE_EXTENDED,
    HEARTS_FIELD_NAME_STATS,
]

HEARTS_FIELD_NAME_TO_RESPONSE_BUILDER = {
    HEARTS_FIELD_NAME_SHORT: build_response_daily_short,
    HEARTS_FIELD_NAME_DAILY_EXTENDED: build_response_daily_extended,
    HEARTS_FIELD_NAME_VOTE_EXTENDED: build_response_vote_extended,
    HEARTS_FIELD_NAME_STATS: build_response_heart_stats,
}
