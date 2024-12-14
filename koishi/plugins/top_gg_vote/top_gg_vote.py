__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import Embed
from hata.ext.slash import Button

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY
from ...bot_utils.daily import calculate_daily_new, calculate_vote_for
from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to

from ..user_balance import get_user_balance
from ..user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE, get_one_user_settings, get_preferred_client_for_user
)


async def handle_top_gg_vote(external_event):
    """
    Handles a top.gg vote.
    
    This function is a coroutine.
    
    Parameters
    ----------
    external_event : ``ExternalEvent``
        The received event about the vote.
    """
    user = await get_user(external_event.user_id)
    
    user_balance = await get_user_balance(external_event.user_id)
    
    now = DateTime.now(TimeZone.utc)
    streak_new, daily_can_claim_at = calculate_daily_new(user_balance.streak, user_balance.daily_can_claim_at, now)
    received = calculate_vote_for(user, streak_new)
    streak_new += 1
    balance = user_balance.balance + received
    
    user_balance.set('balance', balance)
    user_balance.set('streak', streak_new)
    user_balance.set('daily_can_claim_at', max(daily_can_claim_at, now))
    user_balance.set('count_top_gg_vote', user_balance.count_top_gg_vote + 1)
    user_balance.set('top_gg_voted_at', now)
    await user_balance.save()
    

    target_user_settings = await get_one_user_settings(external_event.user_id)
    if target_user_settings.notification_vote:
        await send_embed_to(
            get_preferred_client_for_user(user, target_user_settings.preferred_client_id, None),
            user.id,
            Embed(
                f'You voted for me, Its so embarrassing. *blushes*',
                (
                    f'You received {received} {EMOJI__HEART_CURRENCY} and now you have '
                    f'{balance} {EMOJI__HEART_CURRENCY}\n'
                    f'You are on a {streak_new} day streak.'
                ),
                color = COLOR__GAMBLING,
            ),
            Button(
                'I don\'t want notifs, nya!!',
                custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE,
            ),
        )
