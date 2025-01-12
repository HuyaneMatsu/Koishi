__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from re import compile as re_compile

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import elapsed_time

from ...bot_utils.user_getter import get_users_unordered

from ..relationships import get_relationship_listing_and_extend, iter_relationship_and_extend_user_ids_to_request
from ..user_balance import get_user_balances


USER_NAME_WITH_COMMENT_RP = re_compile('(.*?)(?:\\s*\\(.*\\)\\s*)?')


def remove_comment(target_user_name):
    """
    Removes the comment from after the name.
    
    Parameters
    ----------
    target_user_name : `str`
        The target user's name.
    
    Returns
    -------
    target_user_name : `str`
    """
    match = USER_NAME_WITH_COMMENT_RP.fullmatch(target_user_name)
    if (match is not None):
        target_user_name = match.group(1)
    
    return target_user_name


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
        value = remove_comment(value)
    
    relationship_listing, relationship_listing_extend = await get_relationship_listing_and_extend(user_id)
    if relationship_listing is None:
        return {}
    
    users = await get_users_unordered(
        iter_relationship_and_extend_user_ids_to_request(user_id, relationship_listing, relationship_listing_extend)
    )
    
    if (value is not None):
        users = [user for user in users if user.has_name_like_at(value, guild_id)]
    
    user_balances = await get_user_balances(user.id for user in users)
    
    return {user: user_balances[user.id].daily_can_claim_at for user in users}


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
