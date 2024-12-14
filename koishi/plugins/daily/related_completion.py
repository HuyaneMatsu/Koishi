__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from re import compile as re_compile

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import elapsed_time

from ...bot_utils.user_getter import get_users_unordered

from ..marriage import get_related_ids
from ..user_balance import get_user_balances


WAIFU_WITH_COMMENT_RP = re_compile('(.*?)(?:\\s*\\(.*\\)\\s*)?')


async def get_related_with_name(user_id, guild_id, name):
    """
    Gets the related user with the given name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        Use id to query for.
    
    guild_id : `int`
        Respective guild's identifier to extend matching for.
    
    name : `str`
        Name to filter for.
    
    Returns
    -------
    related_user : `None | ClientUserBase`
    """
    match = WAIFU_WITH_COMMENT_RP.fullmatch(name)
    if (match is not None):
        name = match.group(1)
    
    related_user_ids = await get_related_ids(user_id)
    related_users = await get_users_unordered(related_user_ids)
    
    for user in related_users:
        if user.has_name_like_at(name, guild_id):
            return user


async def get_related_users_with_name_and_next_daily(user_id, guild_id, value):
    """
    Gets the related users matching the given value and when they can claim their daily at.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        Use id to query for.
    
    guild_id : `int`
        Respective guild's identifier to extend matching for.
    
    value : `None | str`
        Value to match.
    
    Returns
    -------
    related_users : `dict<ClientUserBase, DateTime>`
    """
    if (value is not None):
        match = WAIFU_WITH_COMMENT_RP.fullmatch(value)
        if (match is not None):
            value = match.group(1)
    
    related_user_ids = await get_related_ids(user_id)
    related_users = await get_users_unordered(related_user_ids)
    
    if (value is not None):
        related_users = [user for user in related_users if user.has_name_like_at(value, guild_id)]
    
    user_balances = await get_user_balances(user.id for user in related_users)
    
    return {user: user_balances[user.id].daily_can_claim_at for user in related_users}


def get_related_sort_key_and_suggestion(related_user, guild_id, now, daily_can_claim_at):
    """
    Gets sort key for the related user and builds a suggestion for them.
    
    Parameters
    ----------
    related_user : ``ClientUserBase``
        The related user.
    
    guild_id : `int`
        Respective guild's identifier to extend naming for.
    
    now : ``DateTime`
        Current time.
    
    daily_can_claim_at : `DateTime`
        When the user can claim their daily.
    
    Returns
    -------
    sort_key : `DateTime`
    suggestion : `str`
    """
    if daily_can_claim_at <= now:
        comment = None
        sort_key = now
    
    else:
        comment = elapsed_time(RelativeDelta(daily_can_claim_at, now))
        sort_key = daily_can_claim_at
    
    suggestion = related_user.name_at(guild_id)
    if (comment is not None):
        suggestion = f'{suggestion} ({comment})'
    
    return sort_key, suggestion


async def autocomplete_related_name(interaction_event, value):
    """
    Auto-completes a related user's name.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The targeted user's name if any.
    
    Returns
    -------
    suggestions : `list<str>`
    """
    related_users_and_next_daily = await get_related_users_with_name_and_next_daily(
        interaction_event.user_id, interaction_event.guild_id, value
    )
    now = DateTime.now(TimeZone.utc)
    
    return [
        item[1] for item in sorted(
            get_related_sort_key_and_suggestion(user, interaction_event.guild_id, now, daily_can_claim_at)
            for user, daily_can_claim_at in related_users_and_next_daily.items()
        )
    ]
