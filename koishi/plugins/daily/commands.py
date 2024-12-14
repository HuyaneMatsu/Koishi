__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from math import floor

from hata import DiscordException
from hata.ext.slash import Button, P, abort

from ...bot_utils.constants import WAIFU_COST_DEFAULT
from ...bot_utils.daily import DAILY_INTERVAL, calculate_daily_for, refresh_streak
from ...bot_utils.utils import send_embed_to
from ...bots import FEATURE_CLIENTS

from ..marriage import are_related
from ..user_balance import get_user_balance, get_user_balances
from ..user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE, get_one_user_settings, get_preferred_client_for_user
)

from .embed_builders import (
    build_embed_already_claimed_other, build_embed_already_claimed_self, build_embed_daily_claimed_other,
    build_embed_daily_claimed_other_notification, build_embed_daily_claimed_self, build_embed_not_related
)
from .helpers import should_top_gg_notify
from .related_completion import autocomplete_related_name, get_related_with_name


async def claim_daily_for_yourself(client, interaction_event):
    """
    Claims daily for yourself.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Yields
    ------
    embed : ``Embed``
    """
    user = interaction_event.user
    
    user_balance = await get_user_balance(user.id)
    daily_can_claim_at = user_balance.daily_can_claim_at
    
    now = DateTime.now(TimeZone.utc)
    if daily_can_claim_at > now:
        yield build_embed_already_claimed_self(daily_can_claim_at)
        return
    
    streak = user_balance.streak
    streak_new = refresh_streak(streak, daily_can_claim_at, now)
    received = calculate_daily_for(user, streak_new)
    streak_new += 1
    balance_new = user_balance.balance + received
    
    user_balance.set('balance', balance_new)
    user_balance.set('streak', streak_new)
    user_balance.set('daily_can_claim_at', now + DAILY_INTERVAL)
    user_balance.set('count_daily_self', user_balance.count_daily_self + 1)
    user_balance.set('daily_reminded', False)
    await user_balance.save()
    
    top_gg_notify = should_top_gg_notify(user_balance.count_top_gg_vote, user_balance.top_gg_voted_at, now)
    
    yield build_embed_daily_claimed_self(received, balance_new, streak, streak_new, top_gg_notify)
    return


async def claim_daily_for_other(client, interaction_event, target_user):
    """
    Claims daily for someone else.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : `ClientUserBase``
        The targeted user.
    
    Yields
    ------
    embed : ``Embed``
    """
    source_user = interaction_event.user
    
    if not (await are_related(source_user.id, target_user.id)):
        yield build_embed_not_related(target_user, interaction_event.guild_id)
        return
    
    user_balances = await get_user_balances((source_user.id, target_user.id),)
    source_user_balance = user_balances[source_user.id]
    target_user_balance = user_balances[target_user.id]

    now = DateTime.now(TimeZone.utc)
    
    target_daily_can_claim_at = target_user_balance.daily_can_claim_at
    
    if target_daily_can_claim_at > now:
        yield build_embed_already_claimed_other(target_daily_can_claim_at, target_user, interaction_event.guild_id)
        return
    
    streak = target_user_balance.streak
    streak_new = refresh_streak(streak, target_daily_can_claim_at, now)
    
    received = calculate_daily_for(target_user, streak)
    balance_new = target_user_balance.balance + received
    
    streak_new += 1
    waifu_cost_increase = 1 + floor(received * 0.01)
    
    new_waifu_cost = (source_user_balance.waifu_cost or WAIFU_COST_DEFAULT) + waifu_cost_increase
    source_user_balance.set('waifu_cost', new_waifu_cost)
    source_user_balance.set('count_daily_for_waifu', source_user_balance.count_daily_for_waifu + 1)
    await source_user_balance.save()
    
    new_waifu_cost = (target_user_balance.waifu_cost or WAIFU_COST_DEFAULT) + waifu_cost_increase
    target_user_balance.set('balance', balance_new)
    target_user_balance.set('daily_can_claim_at', now + DAILY_INTERVAL)
    target_user_balance.set('streak', streak_new)
    target_user_balance.set('waifu_cost', new_waifu_cost)
    target_user_balance.set('count_daily_by_waifu', target_user_balance.count_daily_by_waifu + 1)
    target_user_balance.set('daily_reminded', False)
    await target_user_balance.save()
    
    yield build_embed_daily_claimed_other(
        received, balance_new, streak, streak_new, target_user, interaction_event.guild_id
    )
    
    if (not target_user.bot):
        target_user_settings = await get_one_user_settings(target_user.id)
        if target_user_settings.notification_daily_by_waifu:
            await send_embed_to(
                get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                target_user.id,
                build_embed_daily_claimed_other_notification(
                    received, balance_new, streak_new, source_user, interaction_event.guild_id
                ),
                Button(
                    'I don\'t want notifs, nya!!',
                    custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE,
                ),
            )


@FEATURE_CLIENTS.interactions(
    allowed_mentions = None,
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def daily(
    client,
    interaction_event,
    target_user_name: P(
        'str', 'Claiming daily for someone related?', 'related', autocomplete = autocomplete_related_name
    ) = None,
):
    """
    Claim a share of my love every day for yourself or for your related.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user_name : `None | str` = `None`, Optional
        The targeted user's name if any.
    
    Yields
    ------
    acknowledge / embed : `None | Embed`
    """
    if (target_user_name is None):
        target_user = None
    else:
        target_user = await get_related_with_name(
            interaction_event.user_id, interaction_event.guild_id, target_user_name
        )
        if (target_user is None):
            if len(target_user_name) > 100:
                target_user_name = target_user_name[:100] + '...'
            
            abort(f'Waifu not found: `{target_user_name}`')
            return
    
    try:
        yield
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status >= 500:
            return
        
        raise
    
    if target_user is None:
        coroutine_generator = claim_daily_for_yourself(client, interaction_event)
    else:
        coroutine_generator = claim_daily_for_other(client, interaction_event, target_user)
    
    async for embed in coroutine_generator:
        yield embed
