__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from hata import Embed
from hata.ext.slash import Button
from sqlalchemy.sql import select

from ...bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY
from ...bot_utils.daily import calculate_vote_for, refresh_daily_streak
from ...bot_utils.models import DB_ENGINE, USER_COMMON_TABLE, get_create_common_user_expression, user_common_model
from ...bot_utils.user_getter import get_user
from ...bot_utils.utils import send_embed_to

from ..user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE, get_one_user_settings_with_connector,
    get_preferred_client_for_user
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
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.count_top_gg_vote,
                ]
            ).where(
                user_common_model.user_id == external_event.user_id,
            )
        )
        
        now = DateTime.now(TimeZone.utc)
        
        result = await response.fetchone()
        if (result is not None):
            entry_id, total_love, daily_streak, daily_next, count_top_gg_vote = result
            daily_next = daily_next.replace(tzinfo = TimeZone.utc)
            
            daily_streak_new = refresh_daily_streak(daily_streak, daily_next, now)
            received = calculate_vote_for(user, daily_streak_new)
            daily_streak_new += 1
            total_love = total_love + received
            
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = total_love,
                    count_top_gg_vote = count_top_gg_vote + 1,
                    daily_streak = daily_streak_new,
                    daily_next = daily_next,
                    top_gg_last_vote = now,
                )
            )
        
        else:
            daily_streak = 0
            total_love = calculate_vote_for(user, 0)
            daily_streak_new = 1
            daily_next = now
            count_top_gg_vote = 1
        
            await connector.execute(
                get_create_common_user_expression(
                    external_event.user_id,
                    total_love = total_love,
                    count_top_gg_vote = count_top_gg_vote,
                    daily_streak = daily_streak,
                    daily_next = daily_next,
                    top_gg_last_vote = now,
                )
            )
        
        target_user_settings = await get_one_user_settings_with_connector(
            external_event.user_id, connector
        )
        if target_user_settings.notification_vote:
            await send_embed_to(
                get_preferred_client_for_user(user, target_user_settings.preferred_client_id, None),
                user.id,
                Embed(
                    f'You voted for me, Its so embarrassing. *blushes*',
                    (
                        f'You received {received} {EMOJI__HEART_CURRENCY} and now you have '
                        f'{total_love} {EMOJI__HEART_CURRENCY}\n'
                        f'You are on a {daily_streak_new} day streak.'
                    ),
                    color = COLOR__GAMBLING,
                ),
                Button(
                    'I don\'t want notifs, nya!!',
                    custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_VOTE_DISABLE,
                ),
            )
