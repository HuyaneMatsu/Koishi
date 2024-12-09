__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone
from math import floor
from re import compile as re_compile

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import DiscordException, Embed, elapsed_time
from hata.discord.utils import DATETIME_MAX
from hata.ext.slash import Button, abort
from sqlalchemy import and_, or_
from sqlalchemy.sql import select

from ..bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY, URL__KOISHI_TOP_GG, WAIFU_COST_DEFAULT
from ..bot_utils.daily import (
    DAILY_INTERVAL, DAILY_STREAK_BREAK, TOP_GG_VOTE_DELAY_MAX, TOP_GG_VOTE_DELAY_MIN, calculate_daily_for,
    refresh_daily_streak
)
from ..bot_utils.models import (
    DB_ENGINE, USER_COMMON_TABLE, get_create_common_user_expression, user_common_model, waifu_list_model
)
from ..bot_utils.user_getter import get_users_unordered
from ..bot_utils.utils import send_embed_to
from ..bots import FEATURE_CLIENTS


from .user_settings import (
    USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE, get_preferred_client_for_user,
    get_one_user_settings_with_connector
)

WAIFU_WITH_COMMENT_RP = re_compile('(.*?)(?:\\s*\\(.*\\)\\s*)?')



async def claim_daily_for_yourself(client, event):
    user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.count_top_gg_vote,
                    user_common_model.top_gg_last_vote,
                ]
            ).where(
                user_common_model.user_id == user.id,
            )
        )
        
        now = DateTime.now(TimeZone.utc)
        
        result = await response.fetchone()
        if (result is not None):
            entry_id, total_love, daily_streak, daily_next, count_top_gg_vote, top_gg_last_vote = result
            daily_next = daily_next.replace(tzinfo = TimeZone.utc)
            top_gg_last_vote = top_gg_last_vote.replace(tzinfo = TimeZone.utc)
            
            if daily_next > now:
                return Embed(
                    'You already claimed your daily love for today~',
                    f'Come back in {elapsed_time(daily_next)}.',
                    color = COLOR__GAMBLING,
                )
            
            new_daily_streak = refresh_daily_streak(daily_streak, daily_next, now)
            received = calculate_daily_for(user, new_daily_streak)
            new_daily_streak += 1
            total_love = total_love + received
            
            if new_daily_streak > daily_streak:
                streak_text = f'You are on a {new_daily_streak} day streak! Keep up the good work!'
            elif new_daily_streak < daily_streak:
                streak_text = (
                    f'You did not claim daily for more than 1 day, you lost {daily_streak - new_daily_streak}, '
                    f'and now you are at {new_daily_streak}.'
                )
            else:
                streak_text = f'You did not claim daily for 1 day, your daily stands at {daily_streak!s}.'
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = total_love,
                    daily_next = now + DAILY_INTERVAL,
                    daily_streak = new_daily_streak,
                    count_daily_self = user_common_model.count_daily_self + 1,
                    daily_reminded = False,
                )
            )
            
            if (count_top_gg_vote > 0):
                vote_difference = now - top_gg_last_vote
                if (
                    (vote_difference > TOP_GG_VOTE_DELAY_MIN) and
                    (vote_difference < TOP_GG_VOTE_DELAY_MAX)
                ):
                    voted = await client.top_gg.get_user_vote(user.id)
                    if not voted:
                        streak_text = (
                            f'{streak_text}\n'
                            f'\n'
                            f'Please vote for me on [top.gg]({URL__KOISHI_TOP_GG}) for extra {EMOJI__HEART_CURRENCY}'
                        )
            
            
            return Embed(
                'Here, some love for you~\nCome back tomorrow !',
                (
                    f'You received {received} {EMOJI__HEART_CURRENCY} and now have {total_love} '
                    f'{EMOJI__HEART_CURRENCY}\n'
                    f'{streak_text}'
                ),
                color = COLOR__GAMBLING,
            )
        
        received = calculate_daily_for(user, 0)
        await connector.execute(
            get_create_common_user_expression(
                user.id,
                total_love = received,
                daily_next = now + DAILY_INTERVAL,
                daily_streak = 1,
                count_daily_self = 1,
            )
        )
        
        return Embed(
            'Here, some love for you~\nCome back tomorrow !',
            (
                f'You received {received} {EMOJI__HEART_CURRENCY} and now have {received} {EMOJI__HEART_CURRENCY}'
            ),
            color = COLOR__GAMBLING,
        )


async def claim_daily_for_waifu(client, event, target_user):
    source_user = event.user
    
    while True:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                select(
                    [
                        waifu_list_model.id,
                    ]
                ).where(
                    or_(
                        and_(
                            waifu_list_model.user_id == source_user.id,
                            waifu_list_model.waifu_id == target_user.id,
                        ),
                        and_(
                            waifu_list_model.user_id == target_user.id,
                            waifu_list_model.waifu_id == source_user.id,
                        ),
                    )
                )
            )
            
            results = await response.fetchall()
            if len(results) < 1:
                break
            
            # To be someone your waifu, you both need to be in the database, so simple.
            response = await connector.execute(
                select(
                    [
                        user_common_model.id,
                        user_common_model.user_id,
                        user_common_model.total_love,
                        user_common_model.daily_streak,
                        user_common_model.daily_next,
                        user_common_model.waifu_cost,
                    ]
                ).where(
                    user_common_model.user_id.in_(
                        [
                            source_user.id,
                            target_user.id,
                        ]
                    )
                )
            )
            
            if response.rowcount != 2:
                break
            
            results = await response.fetchall()
            if results[0][1] == source_user.id:
                source_entry, target_entry = results
                
            else:
                target_entry, source_entry = results
            
            now = DateTime.now(TimeZone.utc)
            
            target_daily_next = target_entry[4]
            target_daily_next = target_daily_next.replace(tzinfo = TimeZone.utc)
            
            if target_daily_next > now:
                return Embed(
                    f'{target_user.name} already claimed their daily love for today~',
                    f'Come back in {elapsed_time(target_daily_next)}.',
                    color = COLOR__GAMBLING,
                )
            
            target_daily_streak = target_entry[3]
            target_daily_streak = refresh_daily_streak(target_daily_streak, target_daily_next, now)
            
            if target_daily_next + DAILY_STREAK_BREAK < now:
                streak_text = f'They did not claim daily for more than 1 day, they got down to {target_daily_streak}.'
            else:
                streak_text = f'They are in a {target_daily_streak + 1} day streak! Keep up the good work for them!'
            
            received = calculate_daily_for(target_user, target_daily_streak)
            
            target_total_love = target_entry[2]
            target_total_love = target_total_love + received
            
            target_daily_streak += 1
            
            waifu_cost_increase = 1 + floor(received * 0.01)
            
            
            new_waifu_cost = source_entry[5]
            if not new_waifu_cost:
                new_waifu_cost = WAIFU_COST_DEFAULT
            new_waifu_cost += waifu_cost_increase
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == source_entry[0],
                ).values(
                    waifu_cost = new_waifu_cost,
                    count_daily_for_waifu = user_common_model.count_daily_for_waifu + 1,
                )
            )
            
            new_waifu_cost = target_entry[5]
            if not new_waifu_cost:
                new_waifu_cost = WAIFU_COST_DEFAULT
            new_waifu_cost += waifu_cost_increase
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == target_entry[0],
                ).values(
                    total_love = target_total_love,
                    daily_next = now + DAILY_INTERVAL,
                    daily_streak = target_daily_streak,
                    waifu_cost = new_waifu_cost,
                    count_daily_by_waifu = user_common_model.count_daily_by_waifu + 1,
                    daily_reminded = False,
                )
            )
            
            await client.interaction_followup_message_create(
                event,
                embed = Embed(
                    'How sweet, you claimed my love for your chosen one !',
                    (
                        f'{target_user.name} received {received} {EMOJI__HEART_CURRENCY} and they have '
                        f'{target_total_love} {EMOJI__HEART_CURRENCY}\n'
                        f'{streak_text}'
                    ),
                    color = COLOR__GAMBLING,
                )
            )
            
            if (not target_user.bot):
                target_user_settings = await get_one_user_settings_with_connector(
                    target_user.id, connector
                )
                if target_user_settings.notification_daily_by_waifu:
                    await send_embed_to(
                        get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
                        target_user.id,
                        Embed(
                            f'{source_user.full_name} claimed daily love for you.',
                            (
                                f'You received {received} {EMOJI__HEART_CURRENCY} and now you have '
                                f'{target_total_love} {EMOJI__HEART_CURRENCY}\n'
                                f'You are on a {target_daily_streak} day streak.'
                            ),
                            color = COLOR__GAMBLING,
                        ),
                        Button(
                            'I don\'t want notifs, nya!!',
                            custom_id = USER_SETTINGS_CUSTOM_ID_NOTIFICATION_DAILY_BY_WAIFU_DISABLE,
                        ),
                    )
            
            return
    
    # Since now we pre-match waifus by name, this could only happen if some race-condition happened.
    return Embed(
        'Savage',
        f'{target_user.full_name} is not your waifu.',
        color = COLOR__GAMBLING,
    )


async def get_waifu_ids_and_daily_next(user_id):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.user_id,
                    user_common_model.daily_next,
                ]
            ).where(
                user_common_model.user_id.in_(
                    select(
                        [
                            waifu_list_model.user_id,
                        ]
                    ).where(
                        waifu_list_model.waifu_id == user_id,
                    ).union(
                        select(
                            [
                                waifu_list_model.waifu_id,
                            ]
                        ).where(
                            waifu_list_model.user_id == user_id,
                        )
                    )
                ),
            )
        )
        
        results = await response.fetchall()
    
    return {waifu_id: daily_next.replace(tzinfo = TimeZone.utc) for (waifu_id, daily_next) in results}


async def get_waifu_with_name(event, name):
    match = WAIFU_WITH_COMMENT_RP.fullmatch(name)
    if (match is not None):
        name = match.group(1)

    user_id = event.user.id
    waifu_ids_and_daily_next = await get_waifu_ids_and_daily_next(user_id)
    waifus = await get_users_unordered(waifu_ids_and_daily_next.keys())
    
    for waifu in waifus:
        if waifu.has_name_like_at(name, event.guild_id):
            return waifu


async def get_waifus_with_name_and_next_daily(event, value):
    if (value is not None):
        match = WAIFU_WITH_COMMENT_RP.fullmatch(value)
        if (match is not None):
            value = match.group(1)
    
    user_id = event.user.id
    waifu_ids_and_daily_next = await get_waifu_ids_and_daily_next(user_id)
    waifus = await get_users_unordered(waifu_ids_and_daily_next.keys())
    
    if (value is not None):
        waifus = [waifu for waifu in waifus if waifu.has_name_like_at(value, event.guild_id)]
    
    return {waifu: waifu_ids_and_daily_next.get(waifu.id) for waifu in waifus}


def get_waifu_sort_key_and_suggestion(waifu, now, daily_next):
    if daily_next is None:
        comment = 'unknown'
        sort_key = DATETIME_MAX
    
    elif daily_next <= now:
        comment = None
        sort_key = now
    
    else:
        comment = elapsed_time(RelativeDelta(daily_next, now))
        sort_key = daily_next
    
    suggestion = waifu.full_name
    if (comment is not None):
        suggestion = f'{suggestion} ({comment})'
    
    return sort_key, suggestion


@FEATURE_CLIENTS.interactions(is_global = True)
async def daily(
    client,
    event,
    target_user_name: ('str', 'Claiming daily for a waifu?', 'waifu') = None,
):
    """Claim a share of my love every day for yourself or for your waifu."""
    if (target_user_name is None):
        target_user = None
    else:
        target_user = await get_waifu_with_name(event, target_user_name)
        if (target_user is None):
            if len(target_user_name) > 100:
                target_user_name = target_user_name[:100] + '...'
            
            abort(f'Waifu not found: `{target_user_name}`')
            return
    
    try:
        await client.interaction_application_command_acknowledge(event)
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status >= 500:
            return
        
        raise
    
    if target_user is None:
        embed = await claim_daily_for_yourself(client, event)
    else:
        embed = await claim_daily_for_waifu(client, event, target_user)
    
    yield embed


@daily.autocomplete('target_user_name')
async def autocomplete_waifu_name(event, value):
    waifus_and_next_daily = await get_waifus_with_name_and_next_daily(event, value)
    now = DateTime.now(TimeZone.utc)
    
    return [
        item[1] for item in sorted(
            get_waifu_sort_key_and_suggestion(waifu, now, daily_next)
            for waifu, daily_next in waifus_and_next_daily.items()
        )
    ]
