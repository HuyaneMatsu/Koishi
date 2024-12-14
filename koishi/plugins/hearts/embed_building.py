__all__ = ()

from hata import Embed

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY
from ...bot_utils.daily import REWARDS_DAILY, REWARDS_VOTE

from .constants import (
    EMOJI_COUNT_DAILY_BY_WAIFU, EMOJI_COUNT_DAILY_FOR_WAIFU, EMOJI_COUNT_DAILY_SELF, EMOJI_COUNT_TOP_GG_VOTE,
    EMOJI_DAILY_STREAK
)
from .rendering import (
    render_hearts_extended_description, render_hearts_short_description, render_hearts_short_title, render_int_block
)


def build_daily_embed_short(interaction_event, target_user, balance, streak, ready_to_claim):
    """
    Builds a daily embed (short).
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak.
    
    ready_to_claim : `bool`
        Whether the user is ready to claim their daily.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        render_hearts_short_title(interaction_event, target_user, balance),
        render_hearts_short_description(
            interaction_event, target_user, balance, streak, ready_to_claim, 'claim your daily'
        ),
        color = COLOR__GAMBLING,
    )


def build_daily_embed_extended(interaction_event, target_user, balance, streak, ready_to_claim):
    """
    Builds a daily embed (extended).
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak.
    
    ready_to_claim : `bool`
        Whether the user is ready to claim their daily.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = build_daily_embed_short(interaction_event, target_user, balance, streak, ready_to_claim)
    embed.add_field(
        'Daily reward calculation:',
        render_hearts_extended_description(interaction_event, target_user, REWARDS_DAILY, streak),
    )
    return embed


def build_vote_embed_short(interaction_event, target_user, balance, streak, ready_to_vote):
    """
    Builds a vote embed (short).
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak.
    
    ready_to_vote : `bool`
        Whether the user is ready to vote.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        render_hearts_short_title(interaction_event, target_user, balance),
        render_hearts_short_description(
            interaction_event, target_user, balance, streak, ready_to_vote, 'vote'
        ),
        color = COLOR__GAMBLING,
    )


def build_vote_embed_extended(interaction_event, target_user, balance, streak, ready_to_vote):
    """
    Builds a vote embed (extended).
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak.
    
    ready_to_vote : `bool`
        Whether the user is ready to vote.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = build_vote_embed_short(interaction_event, target_user, balance, streak, ready_to_vote)
    embed.add_field(
        'Vote reward calculation:',
        render_hearts_extended_description(interaction_event, target_user, REWARDS_VOTE, streak),
    )
    return embed


def build_stats_embed(
    interaction_event,
    target_user,
    balance,
    streak,
    count_daily_self,
    count_daily_by_waifu,
    count_daily_for_waifu,
    count_top_gg_vote,
):
    """
    Renders a stats embed.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    balance : `int`
        The user's balance.
    
    streak : `int`
        The user's streak.
    
    count_daily_self : `int`
        The amount the user claimed their own daily.
    
    count_daily_by_waifu : `int`
        The amount the user's daily has been claimed.
    
    count_daily_for_waifu : `int`
        The amount the user claimed other's daily.
    
    count_top_gg_vote : `int`
        The amount the user voted on top.gg.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        color = COLOR__GAMBLING
    ).add_author(
        f'Heart stats for {target_user.name_at(interaction_event.guild)}',
        target_user.avatar_url_at(interaction_event.guild),
    ).add_field(
        f'{EMOJI__HEART_CURRENCY} Hearts',
        render_int_block(balance),
        inline = True,
    ).add_field(
        f'{EMOJI_DAILY_STREAK} Streak',
        render_int_block(streak),
        inline = True,
    ).add_field(
        f'{EMOJI_COUNT_DAILY_SELF} Claimed dailies',
        render_int_block(count_daily_self),
        inline = True,
    ).add_field(
        f'{EMOJI_COUNT_DAILY_FOR_WAIFU} Claimed for waifus',
        render_int_block(count_daily_for_waifu),
        inline = True,
    ).add_field(
        f'{EMOJI_COUNT_DAILY_BY_WAIFU} Claimed by waifu',
        render_int_block(count_daily_by_waifu),
        inline = True,
    ).add_field(
        f'{EMOJI_COUNT_TOP_GG_VOTE} Top.gg votes',
        render_int_block(count_top_gg_vote),
        inline = True,
    )
