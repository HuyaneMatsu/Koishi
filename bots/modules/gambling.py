import re
from functools import partial as partial_func
from datetime import datetime, timedelta
from random import random
from math import log10, ceil, floor

from hata import Client, elapsed_time, Embed, Color, BUILTIN_EMOJIS, DiscordException, Task, Future, KOKORO, \
    ERROR_CODES, USERS, ZEROUSER, parse_tdelta, Permission
from hata.ext.slash import abort, InteractionResponse, set_permission, Button, Row, wait_for_component_interaction
from sqlalchemy.sql import select, desc

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression, \
    waifu_list_model, WAIFU_LIST_TABLE, waifu_proposal_model, WAIFU_PROPOSAL_TABLE

from bot_utils.constants import ROLE__NEKO_DUNGEON__ELEVATED, ROLE__NEKO_DUNGEON__BOOSTER, GUILD__NEKO_DUNGEON, \
    EMOJI__HEART_CURRENCY, USER__DISBOARD, ROLE__NEKO_DUNGEON__HEART_BOOST, ROLE__NEKO_DUNGEON__ADMIN, \
    ROLE__NEKO_DUNGEON__NSFW_ACCESS, IN_GAME_IDS, COLOR__GAMBLING
from bot_utils.utils import send_embed_to

SLASH_CLIENT: Client
Satori: Client

def setup(lib):
    Satori.events.message_create.append(GUILD__NEKO_DUNGEON, heart_generator)

def teardown(lib):
    Satori.events.message_create.remove(GUILD__NEKO_DUNGEON, heart_generator)


DAILY_INTERVAL          = timedelta(hours=22)
DAILY_STREAK_BREAK      = timedelta(hours=26)
DAILY_STREAK_LOSE       = timedelta(hours=12)

DAILY_BASE              = 100
DAILY_PER_DAY           = 5
DAILY_LIMIT             = 300

DAILY_LIMIT_BONUS_W_E   = 300

DAILY_PER_DAY_BONUS_W_B = 5
DAILY_LIMIT_BONUS_W_B   = 300

DAILY_BASE_BONUS_W_HE   = 514
DAILY_LIMIT_BONUS_W_HE  = 5140

NSFW_ACCESS_COST        = 666
ELEVATED_COST           = 10000
HEART_BOOST_COST        = 514000


EVENT_MAX_DURATION      = timedelta(hours=24)
EVENT_MIN_DURATION      = timedelta(minutes=30)
EVENT_HEART_MIN_AMOUNT  = 50
EVENT_HEART_MAX_AMOUNT  = 3000
EVENT_OK_EMOJI          = BUILTIN_EMOJIS['ok_hand']
EVENT_ABORT_EMOJI       = BUILTIN_EMOJIS['x']
EVENT_DAILY_MIN_AMOUNT  = 1
EVENT_DAILY_MAX_AMOUNT  = 7
EVENT_OK_BUTTON         = Button(emoji=EVENT_OK_EMOJI)
EVENT_ABORT_BUTTON      = Button(emoji=EVENT_ABORT_EMOJI)
EVENT_COMPONENTS        = Row(EVENT_OK_BUTTON, EVENT_ABORT_BUTTON)
EVENT_CURRENCY_BUTTON   = Button(emoji=EMOJI__HEART_CURRENCY)


def calculate_daily_for(user, daily_streak):
    """
    Returns how much daily love the given user gets after the given streak.
    
    Parameters
    ----------
    user : ``User`` or ``Client``
        The respective user.
    daily_streak : `int`
        The daily streak of the respective user.
    
    Returns
    -------
    received : `int`
    """
    daily_base = DAILY_BASE
    daily_per_day = DAILY_PER_DAY
    daily_limit = DAILY_LIMIT
    
    
    if user.has_role(ROLE__NEKO_DUNGEON__ELEVATED):
        daily_limit += DAILY_LIMIT_BONUS_W_E
    
    if user.has_role(ROLE__NEKO_DUNGEON__BOOSTER):
        daily_per_day += DAILY_PER_DAY_BONUS_W_B
        daily_limit += DAILY_LIMIT_BONUS_W_B
    
    if user.has_role(ROLE__NEKO_DUNGEON__HEART_BOOST):
        daily_base += DAILY_BASE_BONUS_W_HE
        daily_limit += DAILY_LIMIT_BONUS_W_HE
    
    
    daily_extra = daily_streak*daily_per_day
    if (daily_extra > daily_limit):
        daily_extra = daily_limit
    
    received = daily_base+daily_extra+daily_streak
    
    return received

def calculate_daily_new_only(daily_streak, daily_next, now):
    """
    Calculates daily streak loss and the new next claim time.
    
    Parameters
    ----------
    daily_streak : `int`
        The user's actual daily streak.
    daily_next : `datetime`
        The time when the user can claim it's next daily reward.
    now : `datetime`
        The current utc time.
    
    Returns
    -------
    daily_streak_new : `int`
        The new daily streak value of the user.
    """
    daily_next_with_break = daily_next+DAILY_STREAK_BREAK
    if daily_next_with_break < now:
        daily_streak_new = daily_streak-((now-daily_next_with_break)//DAILY_STREAK_LOSE)-1
        
        if daily_streak_new < 0:
            daily_streak_new = 0
    
    else:
        daily_streak_new = daily_streak
    
    return daily_streak_new


def calculate_daily_new(daily_streak, daily_next, now):
    """
    Calculates daily streak loss and the new next claim time.
    
    Parameters
    ----------
    daily_streak : `int`
        The user's actual daily streak.
    daily_next : `datetime`
        The time when the user can claim it's next daily reward.
    now : `datetime`
        The current utc time.
    
    Returns
    -------
    daily_streak_new : `int`
        The new daily streak value of the user.
    daily_next_new : `datetime`
        The new daily next value of the user.
    """
    daily_next_with_break = daily_next+DAILY_STREAK_BREAK
    if daily_next_with_break < now:
        daily_streak_new = daily_streak-((now-daily_next_with_break)//DAILY_STREAK_LOSE)-1
        
        if daily_streak_new < 0:
            daily_streak_new = 0
            daily_next_new = now
        else:
            daily_next_new = daily_next+(DAILY_STREAK_LOSE*(daily_streak-daily_streak_new))
    
    else:
        daily_streak_new = daily_streak
        daily_next_new = daily_next
    
    return daily_streak_new, daily_next_new


async def claim_daily_for_yourself(event):
    user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                ]
            ).where(
                user_common_model.user_id == user.id,
            )
        )
        
        now = datetime.utcnow()
        
        results = await response.fetchall()
        if results:
            entry_id, total_love, daily_streak, daily_next = results[0]
            
            if daily_next > now:
                return Embed(
                    'You already claimed your daily love for today~',
                    f'Come back in {elapsed_time(daily_next)}.',
                    color = COLOR__GAMBLING,
                )
            
            daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
            
            if daily_next+DAILY_STREAK_BREAK < now:
                streak_text = f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
            else:
                streak_text = f'You are in a {daily_streak+1} day streak! Keep up the good work!'
            
            received = calculate_daily_for(user, daily_streak)
            total_love = total_love+received
            
            daily_streak += 1
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = total_love,
                    daily_next = now+DAILY_INTERVAL,
                    daily_streak = daily_streak,
                )
            )
            
            return Embed(
                'Here, some love for you~\nCome back tomorrow !',
                (
                    f'You received {received} {EMOJI__HEART_CURRENCY:e} and now have {total_love} '
                    f'{EMOJI__HEART_CURRENCY:e}\n'
                    f'{streak_text}'
                ),
                color = COLOR__GAMBLING,
            )
        
        received = calculate_daily_for(user, 0)
        await connector.execute(
            get_create_common_user_expression(
                user.id,
                total_love = received,
                daily_next = now+DAILY_INTERVAL,
                daily_streak = 1,
            )
        )
        
        return Embed(
            'Here, some love for you~\nCome back tomorrow !',
            (
                f'You received {received} {EMOJI__HEART_CURRENCY:e} and now have {received} {EMOJI__HEART_CURRENCY:e}'
            ),
            color = COLOR__GAMBLING,
        )


async def claim_daily_for_waifu(client, event, target_user):
    source_user = event.user
    
    while True:
        async with DB_ENGINE.connect() as connector:
            # To be someone your waifu, you both need to be in the database, so simple.
            response = await connector.execute(
                select(
                    [
                        user_common_model.id,
                        user_common_model.user_id,
                        user_common_model.waifu_owner_id,
                        user_common_model.total_love,
                        user_common_model.daily_streak,
                        user_common_model.daily_next,
                        user_common_model.notify_daily,
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
            
            source_waifu_owner_id = source_entry[2]
            target_waifu_owner_id = target_entry[2]
            
            if (source_waifu_owner_id != target_user.id) and (target_waifu_owner_id != source_user.id):
                break
            
            now = datetime.utcnow()
            
            target_daily_next = target_entry[5]
            if target_daily_next > now:
                return Embed(
                    'They already claimed your daily love for today~',
                    f'Come back in {elapsed_time(target_daily_next)}.',
                    color = COLOR__GAMBLING,
                )
            
            target_daily_streak = target_entry[4]
            target_daily_streak = calculate_daily_new_only(target_daily_streak, target_daily_next, now)
            
            if target_daily_next+DAILY_STREAK_BREAK < now:
                streak_text = f'They did not claim daily for more than 1 day, they got down to {target_daily_streak}.'
            else:
                streak_text = f'They are in a {target_daily_streak+1} day streak! Keep up the good work for them!'
            
            received = calculate_daily_for(target_user, target_daily_streak)
            
            target_total_love = target_entry[3]
            target_total_love = target_total_love+received
            
            target_daily_streak += 1
            
            waifu_cost_increase = 1+floor(received*0.01)
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == source_entry[0],
                ).values(
                    waifu_cost = user_common_model.waifu_cost+waifu_cost_increase,
                )
            )
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == target_entry[0],
                ).values(
                    total_love = target_total_love,
                    daily_next = now+DAILY_INTERVAL,
                    daily_streak = target_daily_streak,
                    waifu_cost = user_common_model.waifu_cost+waifu_cost_increase,
                )
            )
            
            await client.interaction_response_message_create(
                event,
                embed = Embed(
                    'How sweet, you claimed my love for your chosen one !',
                    (
                        f'They received {received} {EMOJI__HEART_CURRENCY:e} and they have {target_total_love} '
                        f'{EMOJI__HEART_CURRENCY:e}\n'
                        f'{streak_text}'
                    ),
                    color = COLOR__GAMBLING,
                )
            )
            
            if (not target_user.is_bot) and target_entry[6]:
                await send_embed_to(
                    client,
                    target_user.id,
                    Embed(
                        f'{source_user.full_name} claimed daily love for you.',
                        (
                            f'You received {received} {EMOJI__HEART_CURRENCY.as_emoji} and now you have '
                            f'{target_total_love} {EMOJI__HEART_CURRENCY.as_emoji}\n'
                            f'You are on a {target_daily_streak} day streak.'
                        ),
                        color = COLOR__GAMBLING,
                    )
                )
            
            return
    
    return Embed(
        'Savage',
        f'{target_user.full_name} is not your waifu.',
        color = COLOR__GAMBLING,
    )



@SLASH_CLIENT.interactions(is_global=True)
async def daily(client, event,
    target_user: ('user', 'Anyone to gift your daily love?', 'waifu') = None,
):
    """Claim a share of my love every day for yourself or for your waifu."""
    if target_user is None:
        coroutine = claim_daily_for_yourself(event)
    else:
        coroutine = claim_daily_for_waifu(client, event, target_user)
    
    return await coroutine



@SLASH_CLIENT.interactions(is_global=True)
async def hearts(client, event,
        target_user: ('user', 'Do you wanna know some1 else\'s hearts?') = None,
        extended: ('bool', 'Extended info.') = False
            ):
    """How many hearts do you have?"""
    if target_user is None:
        target_user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == target_user.id,
            )
        )
        
        results = await response.fetchall()
    
        if results:
            entry_id, total_love, daily_streak, daily_next, total_allocated = results[0]
            
            now = datetime.utcnow()
            if daily_next > now:
                ready_to_claim = False
            else:
                ready_to_claim = True
                
                daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
        
        else:
            total_love = 0
            daily_streak = 0
            total_allocated = 0
            ready_to_claim = True
        
        if total_allocated and (target_user.id not in IN_GAME_IDS):
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_allocated = 0,
                )
            )
    
    is_own = (event.user is target_user)
    
    if is_own:
        title_prefix = 'You have'
    else:
        title_prefix = target_user.full_name+' has'
    
    title = f'{title_prefix} {total_love} {EMOJI__HEART_CURRENCY:e}'
    
    if total_love == 0 and daily_streak == 0:
        if is_own:
            description = 'Awww, you seem so lonely..'
        else:
            description = 'Awww, they seem so lonely..'
    elif daily_streak:
        if is_own:
            if ready_to_claim:
                description_postfix = 'and you are ready to claim your daily'
            else:
                description_postfix = 'keep up the good work'
            description = f'You are on a {daily_streak} day streak, {description_postfix}!'
        
        else:
            description = f'They are on a {daily_streak} day streak, hope they will keep up their good work.'
    else:
        description = None
    
    embed = Embed(title, description, color=COLOR__GAMBLING)
    
    if extended:
        field_value_parts = [
            '**Base:**\n'
            'Daily base: ', repr(DAILY_BASE), '\n'
            'Daily bonus: ', repr(DAILY_PER_DAY), '\n'
            'Daily bonus limit: ', repr(DAILY_LIMIT),
        ]
        
        daily_base = DAILY_BASE
        daily_per_day = DAILY_PER_DAY
        daily_limit = DAILY_LIMIT
        has_extra_role = False
        
        if target_user.has_role(ROLE__NEKO_DUNGEON__ELEVATED):
            has_extra_role = True
            
            field_value_parts.append('\n\n**')
            field_value_parts.append(ROLE__NEKO_DUNGEON__ELEVATED.mention)
            field_value_parts.append(':**\n')
            
            field_value_parts.append('+ ')
            field_value_parts.append(repr(DAILY_LIMIT_BONUS_W_E))
            field_value_parts.append(' daily bonus limit')
            
            daily_limit += DAILY_LIMIT_BONUS_W_E
        
        if target_user.has_role(ROLE__NEKO_DUNGEON__BOOSTER):
            has_extra_role = True
            
            field_value_parts.append('\n\n**')
            field_value_parts.append(ROLE__NEKO_DUNGEON__BOOSTER.mention)
            field_value_parts.append(':**\n')
            
            field_value_parts.append('+ ')
            field_value_parts.append(repr(DAILY_PER_DAY_BONUS_W_B))
            field_value_parts.append(' daily bonus\n')
            
            field_value_parts.append('+ ')
            field_value_parts.append(repr(DAILY_LIMIT_BONUS_W_B))
            field_value_parts.append(' daily bonus limit')
            
            daily_per_day += DAILY_PER_DAY_BONUS_W_B
            daily_limit += DAILY_LIMIT_BONUS_W_B
        
        if target_user.has_role(ROLE__NEKO_DUNGEON__HEART_BOOST):
            has_extra_role = True
            
            field_value_parts.append('\n\n**')
            field_value_parts.append(ROLE__NEKO_DUNGEON__HEART_BOOST.mention)
            field_value_parts.append(':**\n')
            
            field_value_parts.append('+ ')
            field_value_parts.append(repr(DAILY_BASE_BONUS_W_HE))
            field_value_parts.append(' daily base\n')
            
            field_value_parts.append('+ ')
            field_value_parts.append(repr(DAILY_LIMIT_BONUS_W_HE))
            field_value_parts.append(' daily bonus limit')
            
            daily_base += DAILY_BASE_BONUS_W_HE
            daily_limit += DAILY_LIMIT_BONUS_W_HE
        
        field_value_parts.append('\n**\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**')
        
        if has_extra_role:
            field_value_parts.append('\n\n**Total:**\nDaily base: ')
            field_value_parts.append(repr(daily_base))
            field_value_parts.append('\nDaily bonus: ')
            field_value_parts.append(repr(daily_per_day))
            field_value_parts.append('\nDaily bonus limit: ')
            field_value_parts.append(repr(daily_limit))
        
        field_value_parts.append('\n\n**Formula:**\ndaily base + min(daily bonus limit, daily bonus * daily streak) + '
            'daily streak\n')
        
        field_value_parts.append(repr(daily_base))
        field_value_parts.append(' + min(')
        field_value_parts.append(repr(daily_limit))
        field_value_parts.append(', ')
        field_value_parts.append(repr(daily_per_day))
        field_value_parts.append(' \* ')
        field_value_parts.append(repr(daily_streak))
        field_value_parts.append(') + ')
        field_value_parts.append(repr(daily_streak))
        field_value_parts.append(' = ')
        field_value_parts.append(repr(daily_base + min(daily_limit, daily_per_day * daily_streak) + daily_streak))
        
        field_value = ''.join(field_value_parts)
        
        embed.add_field('Daily reward calculation:', field_value)
    
    return InteractionResponse(embed=embed, allowed_mentions=None)


def convert_tdelta(delta):
    result = []
    rest = delta.days
    if rest:
        result.append(f'{rest} days')
    rest = delta.seconds
    amount = rest//3600
    if amount:
        result.append(f'{amount} hours')
        rest %= 3600
    amount = rest//60
    if amount:
        result.append(f'{amount} minutes')
        rest %= 60
    if rest:
        result.append(f'{rest} seconds')
    return ', '.join(result)


def heart_event_start_checker(client, event):
    if event.user.has_role(ROLE__NEKO_DUNGEON__ADMIN):
        return True
    
    return True


PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ADMIN, True)
async def heart_event(client, event,
        duration : ('str', 'The event\'s duration.'),
        amount : ('int', 'The hearst to earn.'),
        user_limit : ('int', 'The maximal amount fo claimers.') = 0,
            ):
    """Starts a heart event at the channel."""
    while True:
        if not event.user.has_role(ROLE__NEKO_DUNGEON__ADMIN):
            response = f'{ROLE__NEKO_DUNGEON__ADMIN.mention} only!'
            error = True
            break
        
        permissions = event.channel.cached_permissions_for(client)
        if not permissions&PERMISSION_MASK_MESSAGING:
            response = (
                'I require `send messages`, `add reactions` and `user external emojis` permissions to invoke this '
                'command.'
            )
            error = True
            break
        
        guild = event.guild
        if (guild is not None):
            if (client.get_guild_profile_for(guild) is None):
                response = 'Please add me to the guild before invoking the command.'
                error = True
                break
        
        duration = parse_tdelta(duration)
        if (duration is None):
            response = 'Could not interpret the given duration.'
            error = True
            break
        
        if duration > EVENT_MAX_DURATION:
            response = (
                f'**Duration passed the upper limit**\n'
                f'**>** upper limit : {convert_tdelta(EVENT_MAX_DURATION)}\n'
                f'**>** passed : {convert_tdelta(duration)}'
            )
            error = True
            break
        
        if duration < EVENT_MIN_DURATION:
            response = (
                f'**Duration passed the lower limit**\n'
                f'**>** lower limit : {convert_tdelta(EVENT_MIN_DURATION)}\n'
                f'**>** passed : {convert_tdelta(duration)}'
            )
            error = True
            break
        
        if amount > EVENT_HEART_MAX_AMOUNT:
            response = (
                f'**Amount passed the upper limit**\n'
                f'**>** upper limit : {EVENT_HEART_MAX_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            error = True
            break
        
        if amount < EVENT_HEART_MIN_AMOUNT:
            response = (
                f'**Amount passed the lower limit**\n'
                f'**>** lower limit : {EVENT_HEART_MIN_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            error = True
            break
        
        if user_limit < 0:
            response = (
                f'**User limit passed the lower limit**\n'
                f'**>** lower limit : 0\n'
                f'**>** - passed : {user_limit}'
            )
            error = True
            break
        
        response_parts = [
            '**Is everything correct?**\n'
            'Duration: '
        ]
        response_parts.append(convert_tdelta(duration))
        response_parts.append('\nAmount: ')
        response_parts.append(str(amount))
        if user_limit:
            response_parts.append('\nUser limit: ')
            response_parts.append(str(user_limit))
        
        response = ''.join(response_parts)
        error = False
        break
    
    if error:
        await client.interaction_response_message_create(event, response, show_for_invoking_user_only=True)
        return
    
    await client.interaction_application_command_acknowledge(event)
    message = await client.interaction_followup_message_create(event, response, components=EVENT_COMPONENTS)
    
    try:
        component_event = await wait_for_component_interaction(message,
            check=partial_func(heart_event_start_checker, client), timeout=300.)
    except TimeoutError:
        try:
            await client.interaction_response_message_edit(event, 'Heart event cancelled, timeout.',
                components=None)
        except ConnectionError:
            pass
        return
    
    if component_event.interaction == EVENT_ABORT_BUTTON:
        try:
            await client.interaction_component_message_edit(component_event, 'Heart event cancelled.',
                components=None)
        except ConnectionError:
            pass
        return
    
    await client.interaction_component_acknowledge(component_event)
    await HeartEventGUI(client, event, duration, amount, user_limit)


class HeartEventGUI:
    _update_time = 60.
    _update_delta = timedelta(seconds=_update_time)
    
    __slots__=('amount', 'client', 'connector', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    async def __new__(cls, client, event, duration, amount, user_limit):
        self = object.__new__(cls)
        self.connector = None
        self.user_ids = set()
        self.user_limit = user_limit
        self.client = client
        self.duration = duration
        self.amount = amount
        self.waiter = Future(KOKORO)
        
        message = event.message
        self.message = message
        
        try:
            await client.interaction_response_message_edit(event, content='', embed=self.generate_embed(),
                components=EVENT_CURRENCY_BUTTON)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            raise
        
        self.connector = await DB_ENGINE.connect()
        client.slasher.add_component_interaction_waiter(message, self)
        Task(self.countdown(client, message), KOKORO)
        return
    
    def generate_embed(self):
        title = f'Click on {EMOJI__HEART_CURRENCY:e} to receive {self.amount}'
        if self.user_limit:
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit-len(self.user_ids)} users'
        else:
            description = f'{convert_tdelta(self.duration)} left'
        return Embed(title, description, color=COLOR__GAMBLING)

    async def __call__(self, event):
        if event.interaction != EVENT_CURRENCY_BUTTON:
            return
        
        user = event.user
        
        user_id = user.id
        user_ids = self.user_ids
        
        old_ln = len(user_ids)
        user_ids.add(user_id)
        new_ln = len(user_ids)
        
        if new_ln == old_ln:
            return

        if new_ln == self.user_limit:
            self.duration = timedelta()
            self.waiter.set_result(None)
        
        connector = self.connector
        
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                ]
            ).where(
                user_common_model.user_id == user.id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id = results[0][0]
            to_execute = USER_COMMON_TABLE. \
                update(user_common_model.id==entry_id). \
                values(total_love=user_common_model.total_love+self.amount)
        
        else:
            to_execute = get_create_common_user_expression(
                user_id,
                total_love = self.amount,
            )
        
        await connector.execute(to_execute)
        
        await self.client.interaction_component_acknowledge(event)
        
    async def countdown(self, client, message):
        update_delta = self._update_delta
        waiter = self.waiter
        
        sleep_time = (self.duration%update_delta).seconds
        if sleep_time:
            self.duration -= timedelta(seconds=sleep_time)
            KOKORO.call_later(sleep_time, waiter.__class__.set_result_if_pending, waiter, None)
            await waiter
            waiter.clear()
        
        sleep_time = self._update_time
        while True:
            KOKORO.call_later(sleep_time, waiter.__class__.set_result_if_pending, waiter, None)
            await waiter
            waiter.clear()
            self.duration -= update_delta
            if self.duration < update_delta:
                break
            try:
                await client.message_edit(message, embed=self.generate_embed())
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    break
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        break
                
                await client.events.error(client, f'{self!r}.countdown', err)
                break
        
        client.slasher.remove_component_interaction_waiter(message, self)
        try:
            await client.message_delete(message)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_access, # client removed
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.countdown', err)
            return
        
        finally:
            connector = self.connector
            if (connector is not None):
                self.connector = None
                await connector.close()
    
    def __del__(self):
        connector = self.connector
        if connector is None:
            return
        
        self.connector = None
        Task(connector.close(), KOKORO)


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ADMIN, True)
async def daily_event(client, event,
        duration : ('str', 'The event\'s duration.'),
        amount : ('int', 'The extra daily steaks to earn.'),
        user_limit : ('int', 'The maximal amount fo claimers.') = 0,
            ):
    """Starts a heart event at the channel. (Bot owner only)"""
    while True:
        if not event.user.has_role(ROLE__NEKO_DUNGEON__ADMIN):
            response = f'{ROLE__NEKO_DUNGEON__ADMIN.mention} only!'
            error = True
            break
        
        permissions = event.channel.cached_permissions_for(client)
        if not permissions&PERMISSION_MASK_MESSAGING:
            response = (
                'I require `send messages`, `add reactions` and `user external emojis` permissions to invoke this '
                'command.'
            )
            error = True
            break
        
        guild = event.guild
        if (guild is not None):
            if (client.get_guild_profile_for(guild) is None):
                response = 'Please add me to the guild before invoking the command.'
                error = True
                break
        
        duration = parse_tdelta(duration)
        if (duration is None):
            response = 'Could not interpret the given duration.'
            error = True
            break
        
        if duration > EVENT_MAX_DURATION:
            response = (
                f'Duration passed the upper limit\n'
                f'**>** upper limit : {convert_tdelta(EVENT_MAX_DURATION)}\n'
                f'**>** passed : {convert_tdelta(duration)}'
            )
            error = True
            break
        
        if duration < EVENT_MIN_DURATION:
            response = (
                f'Duration passed the lower limit\n'
                f'**>** lower limit : {convert_tdelta(EVENT_MIN_DURATION)}\n'
                f'**>** passed : {convert_tdelta(duration)}'
            )
            error = True
            break
        
        if amount > EVENT_DAILY_MAX_AMOUNT:
            response = (
                f'Amount passed the upper limit\n'
                f'**>** upper limit : {EVENT_DAILY_MAX_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            error = True
            break
        
        if amount < EVENT_DAILY_MIN_AMOUNT:
            response = (
                f'Amount passed the lower limit\n'
                f'**>** lower limit : {EVENT_DAILY_MIN_AMOUNT}\n'
                f'**>** passed : {amount}'
            )
            error = True
            break
        
        if user_limit < 0:
            response = (
                f'User limit passed the lower limit\n'
                f'**>** lower limit : 0\n'
                f'**>** passed : {user_limit}'
            )
            error = True
            break
        
        response_parts = [
            '**Is everything correct?**\n'
            'Duration: '
        ]
        response_parts.append(convert_tdelta(duration))
        response_parts.append('\nAmount: ')
        response_parts.append(str(amount))
        if user_limit:
            response_parts.append('\nUser limit: ')
            response_parts.append(str(user_limit))
        
        response = ''.join(response_parts)
        error = False
        break
    
    if error:
        await client.interaction_response_message_create(event, response, show_for_invoking_user_only=True)
        return
    
    await client.interaction_application_command_acknowledge(event)
    message = await client.interaction_followup_message_create(event, response, components=EVENT_COMPONENTS)
    
    try:
        component_event = await wait_for_component_interaction(message,
            check=partial_func(heart_event_start_checker, client), timeout=300.)
    except TimeoutError:
        try:
            await client.interaction_response_message_edit(event, message, 'Daily event cancelled, timeout.',
                components=None)
        except ConnectionError:
            pass
        return
    
    if component_event.interaction == EVENT_ABORT_BUTTON:
        try:
            await client.interaction_component_message_edit(component_event, 'Daily event cancelled.',
                components=None)
        except ConnectionError:
            pass
        return
    
    await client.interaction_component_acknowledge(component_event)
    await DailyEventGUI(client, event, duration, amount, user_limit)


class DailyEventGUI:
    _update_time = 60.
    _update_delta = timedelta(seconds=_update_time)
    
    __slots__=('amount', 'client', 'connector', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    async def __new__(cls, client, event, duration, amount, user_limit):
        self = object.__new__(cls)
        self.connector = None
        self.user_ids = set()
        self.user_limit = user_limit
        self.client = client
        self.duration = duration
        self.amount = amount
        self.waiter = Future(KOKORO)
        
        message = event.message
        self.message = message
        
        try:
            await client.interaction_response_message_edit(event, content='', embed=self.generate_embed(),
                components=EVENT_CURRENCY_BUTTON)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            raise
        
        self.connector = await DB_ENGINE.connect()
        
        self.connector = await DB_ENGINE.connect()
        client.slasher.add_component_interaction_waiter(message, self)
        Task(self.countdown(client, message), KOKORO)
        return
    
    def generate_embed(self):
        title = f'React with {EMOJI__HEART_CURRENCY:e} to increase your daily streak by {self.amount}'
        if self.user_limit:
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit-len(self.user_ids)} users'
        else:
            description = f'{convert_tdelta(self.duration)} left'
        return Embed(title, description, color=COLOR__GAMBLING)
    
    async def __call__(self, event):
        if event.interaction != EVENT_CURRENCY_BUTTON:
            return
        user = event.user
        
        user_id = user.id
        user_ids = self.user_ids
        
        old_ln = len(user_ids)
        user_ids.add(user_id)
        new_ln = len(user_ids)
        
        if new_ln == old_ln:
            return
        
        if new_ln == self.user_limit:
            self.duration = timedelta()
            self.waiter.set_result(None)
        
        connector = self.connector
        
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id, daily_streak, daily_next = results[0]
            now = datetime.utcnow()
            
            daily_streak, daily_next = calculate_daily_new(daily_streak, daily_next, now)
            daily_streak = daily_streak+self.amount
            
            to_execute = USER_COMMON_TABLE.update(
                user_common_model.id == entry_id,
            ).values(
                daily_streak = daily_streak,
                daily_next = daily_next,
            )
        
        else:
            to_execute = get_create_common_user_expression(
                user_id,
                daily_streak = self.amount,
            )
        
        await connector.execute(to_execute)
    
        await self.client.interaction_component_acknowledge(event)
    
    async def countdown(self, client, message):
        update_delta = self._update_delta
        waiter = self.waiter
        
        sleep_time = (self.duration%update_delta).seconds
        if sleep_time:
            self.duration -= timedelta(seconds=sleep_time)
            KOKORO.call_later(sleep_time, waiter.__class__.set_result_if_pending, waiter, None)
            await waiter
            waiter.clear()
        
        sleep_time = self._update_time
        while True:
            KOKORO.call_later(sleep_time, waiter.__class__.set_result_if_pending, waiter, None)
            await waiter
            waiter.clear()
            self.duration -= update_delta
            if self.duration < update_delta:
                break
            try:
                await client.message_edit(message,embed=self.generate_embed())
            except BaseException as err:
                if isinstance(err,ConnectionError):
                    break
                
                if isinstance(err,DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                            ERROR_CODES.missing_access, # client removed
                            ERROR_CODES.missing_permissions, # permissions changed meanwhile
                                ):
                        break
                
                await client.events.error(client, f'{self!r}.countdown', err)
                break
        
        client.slasher.remove_component_interaction_waiter(message, self)
        try:
            await client.message_delete(message)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                # no internet
                return
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.missing_access, # client removed
                            ):
                    return
            
            await client.events.error(client, f'{self!r}.countdown', err)
            return
        
        finally:
            connector = self.connector
            if (connector is not None):
                self.connector = None
                await connector.close()
    
    def __del__(self):
        connector = self.connector
        if connector is None:
            return
        
        self.connector = None
        Task(connector.close(), KOKORO)



@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ELEVATED, True)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__BOOSTER, True)
async def gift(client, event,
        target_user: ('user', 'Who is your heart\'s chosen one?'),
        amount : ('int', 'How much do u love them?'),
        message : ('str', 'Optional message to send with the gift.') = None,
            ):
    """Gifts hearts to the chosen by your heart."""
    source_user = event.user
    
    if not (source_user.has_role(ROLE__NEKO_DUNGEON__ELEVATED) or source_user.has_role(ROLE__NEKO_DUNGEON__BOOSTER)):
        abort(f'You must have either {ROLE__NEKO_DUNGEON__ELEVATED.mention} or '
            f'{ROLE__NEKO_DUNGEON__BOOSTER.mention} role to invoke this command.', allowed_mentions=None)
    
    if source_user is target_user:
        abort('You cannot give love to yourself..')
    
    if amount <= 0:
        abort('You cannot gift non-positive amount of hearts..')
    
    if (message is not None) and len(message) > 1000:
        message = message[:1000]+'...'
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.total_allocated
                ]
            ).where(
                user_common_model.user_id == source_user.id,
            )
        )
        
        results = await response.fetchall()
        if results:
            source_user_entry_id, source_user_total_love, source_user_total_allocated = results[0]
        else:
            source_user_entry_id = -1
            source_user_total_love = 0
            source_user_total_allocated = 0
        
        if source_user_total_love == 0:
            yield Embed('So lonely...', 'You do not have any hearts to gift.', color=COLOR__GAMBLING)
            return
        
        if source_user_total_love == source_user_total_allocated:
            yield Embed('Like a flower', 'Whithering to the dust.', color=COLOR__GAMBLING)
            return
        
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                ]
            ).where(
                user_common_model.user_id == target_user.id,
            )
        )
        
        results = await response.fetchall()
        if results:
            target_user_entry_id, target_user_total_love = results[0]
        else:
            target_user_entry_id = -1
            target_user_total_love = 0
        
        source_user_total_love -= source_user_total_allocated
        
        if amount > source_user_total_love:
            amount = source_user_total_love-source_user_total_allocated
            source_user_new_love = source_user_total_allocated
        else:
            source_user_new_love = source_user_total_love-amount
        
        target_user_new_total_love = target_user_total_love+amount
        
        await connector.execute(USER_COMMON_TABLE. \
            update(user_common_model.id==source_user_entry_id). \
            values(total_love = user_common_model.total_love-amount)
        )
        
        if target_user_entry_id != -1:
            to_execute = USER_COMMON_TABLE. \
                update(user_common_model.id==target_user_entry_id). \
                values(total_love = user_common_model.total_love+amount)
        
        else:
            to_execute = get_create_common_user_expression(
                target_user.id,
                total_love = target_user_new_total_love,
            )
        
        await connector.execute(to_execute)
        
    embed = Embed('Aww, so lovely',
        f'You gifted {amount} {EMOJI__HEART_CURRENCY.as_emoji} to {target_user.full_name}',
        color=COLOR__GAMBLING,
    ).add_field(
        f'Your {EMOJI__HEART_CURRENCY.as_emoji}',
        f'{source_user_total_love} -> {source_user_new_love}',
    ).add_field(
        f'Their {EMOJI__HEART_CURRENCY.as_emoji}',
        f'{target_user_total_love} -> {target_user_new_total_love}',
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    yield embed
    
    if target_user.is_bot:
        return
    
    try:
        target_user_channel = await client.channel_private_create(target_user)
    except ConnectionError:
        return
    
    embed = Embed('Aww, love is in the air',
        f'You have been gifted {amount} {EMOJI__HEART_CURRENCY.as_emoji} by {source_user.full_name}',
        color = COLOR__GAMBLING,
    ).add_field(
        f'Your {EMOJI__HEART_CURRENCY.as_emoji}',
        f'{target_user_total_love} -> {target_user_new_total_love}',
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    try:
        await client.message_create(target_user_channel, embed=embed)
    except ConnectionError:
        return
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user:
            return
        
        raise


AWARD_TYPES = [
    ('hearts', 'hearts'),
    ('daily-streak', 'daily-streak')
]

@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ADMIN, True)
async def award(client, event,
        target_user: ('user', 'Who do you want to award?'),
        amount: ('int', 'With how much love do you wanna award them?'),
        message : ('str', 'Optional message to send with the gift.') = None,
        with_: (AWARD_TYPES, 'Select award type') = 'hearts',
            ):
    """Awards the user with love."""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__ADMIN):
        abort(f'{ROLE__NEKO_DUNGEON__ADMIN.mention} only!', allowed_mentions=None)
    
    if amount <= 0:
        yield Embed('BAKA !!', 'You cannot award non-positive amount of hearts..', color=COLOR__GAMBLING)
        return
    
    if (message is not None) and len(message) > 1000:
        message = message[:1000]+'...'
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                ]
            ).where(
                user_common_model.user_id == target_user.id
            )
        )
        
        results = await response.fetchall()
        if results:
            target_user_entry_id, target_user_total_love, target_user_daily_streak, target_user_daily_next = results[0]
        else:
            target_user_entry_id = -1
            target_user_total_love = 0
            target_user_daily_streak = 0
            target_user_daily_next = datetime.utcnow()
        
        
        if with_ == 'hearts':
            target_user_new_total_love = target_user_total_love+amount
            target_user_new_daily_streak = target_user_daily_streak
        else:
            now = datetime.utcnow()
            target_user_new_total_love = target_user_total_love
            if target_user_daily_next < now:
                target_user_daily_streak, target_user_daily_next = calculate_daily_new(target_user_daily_streak, 
                    target_user_daily_next, now)
            
            target_user_new_daily_streak = target_user_daily_streak+amount
        
        target_user_new_daily_next = target_user_daily_next
            
        if (target_user_entry_id != -1):
            to_execute = USER_COMMON_TABLE. \
                update(user_common_model.id == target_user_entry_id). \
                values(
                    total_love  = target_user_new_total_love,
                    daily_streak = target_user_new_daily_streak,
                    daily_next = target_user_new_daily_next,
                )
        else:
            to_execute = get_create_common_user_expression(
                target_user.id,
                total_love = target_user_new_total_love,
                daily_next = target_user_new_daily_next,
                daily_streak = target_user_new_daily_streak,
            )
        
        await connector.execute(to_execute)
    
    if with_ == 'hearts':
        awarded_with = EMOJI__HEART_CURRENCY.as_emoji
        up_from = target_user_total_love
        up_to = target_user_new_total_love
    else:
        awarded_with = 'daily streak(s)'
        up_from = target_user_daily_streak
        up_to = target_user_new_daily_streak
    
    embed = Embed(
        f'You awarded {target_user.full_name} with {amount} {awarded_with}',
        f'Now they are up from {up_from} to {up_to} {awarded_with}',
        color = COLOR__GAMBLING,
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    yield embed
    
    if target_user.is_bot:
        return

    try:
        target_user_channel = await client.channel_private_create(target_user)
    except ConnectionError:
        return
    
    embed = Embed(
        'Aww, love is in the air',
        f'You have been awarded {amount} {awarded_with} by {event.user.full_name}',
        color = COLOR__GAMBLING,
    ).add_field(
        f'Your {awarded_with}',
        f'{up_from} -> {up_to}',
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    try:
        await client.message_create(target_user_channel, embed=embed)
    except ConnectionError:
        return
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user:
            return
        
        raise


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ADMIN, True)
async def take(client, event,
        target_user: ('user', 'From who do you want to take love away?'),
        amount: ('int', 'How much love do you want to take away?'),
            ):
    """Takes away hearts form the lucky user."""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__ADMIN):
        abort(f'{ROLE__NEKO_DUNGEON__ADMIN.mention} only!', allowed_mentions=None)
    
    if amount <= 0:
        abort('You cannot award non-positive amount of hearts..')
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == target_user.id
            )
        )
        results = await response.fetchall()
        if results:
            target_user_entry_id, target_user_total_love, target_user_total_allocated = results[0]
            target_user_heart_reducible = target_user_total_love-target_user_total_allocated
            if target_user_heart_reducible <= 0:
                target_user_new_total_love = 0
            else:
                target_user_new_total_love = target_user_heart_reducible-amount
                if target_user_new_total_love < 0:
                    target_user_new_total_love = 0
                
                target_user_new_total_love += target_user_total_allocated
                
                await connector.execute(
                    USER_COMMON_TABLE.update(
                        user_common_model.id == target_user_entry_id,
                    ).values(
                        total_love = target_user_new_total_love,
                    )
                )
        else:
            target_user_total_love = 0
            target_user_new_total_love = 0
    
    yield Embed(
        f'You took {amount} {EMOJI__HEART_CURRENCY.as_emoji} away from {target_user.full_name}',
        f'They got down from {target_user_total_love} to {target_user_new_total_love} {EMOJI__HEART_CURRENCY.as_emoji}',
        color = COLOR__GAMBLING,
    )
    
    return


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ADMIN, True)
async def transfer(client, event,
        source_user: ('user', 'Who\'s hearst do you want to transfer?'),
        target_user: ('user', 'To who do you want transfer the taken heart?'),
        message : ('str', 'Optional message to send with the transfer.') = None,
            ):
    """Transfers all of someone\'s hearts to an other person."""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__ADMIN):
        abort(f'{ROLE__NEKO_DUNGEON__ADMIN.mention} only!', allowed_mentions=None)
    
    if (message is not None) and len(message) > 1000:
        message = message[:1000]+'...'
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.user_id,
                    user_common_model.total_love,
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
        
        source_user_found = False
        source_user_entry_id = 0
        source_user_total_love = 0
        
        target_user_found = False
        target_user_entry_id = 0
        target_user_total_love = 0
        
        results = await response.fetchall()
        for result in results:
            entry_id, user_id, total_love = result
            
            if user_id == source_user.id:
                source_user_found = True
                source_user_entry_id = entry_id
                source_user_total_love = total_love
            else:
                target_user_found = True
                target_user_entry_id = entry_id
                target_user_total_love = total_love
        
        if source_user_found:
            await connector.execute(
                USER_COMMON_TABLE.delete(). \
                where(user_common_model.id==source_user_entry_id)
            )
        
        if source_user_total_love:
            if target_user_found:
                to_execute = USER_COMMON_TABLE. \
                    update(user_common_model.id == target_user_entry_id). \
                    values(
                        total_love = user_common_model.total_love+source_user_total_love,
                    )
            else:
                to_execute = get_create_common_user_expression(
                    user_id,
                    total_love = source_user_total_love,
                )
            
            await connector.execute(to_execute)
    
    embed = Embed(
        f'You transferred {source_user.full_name}\'s hearts to {target_user.full_name}',
        color = COLOR__GAMBLING,
    ).add_field(
        f'Their {EMOJI__HEART_CURRENCY:e}',
        f'{target_user_total_love} -> {target_user_total_love+source_user_total_love}',
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    yield embed
    
    if target_user.is_bot:
        return
    
    try:
        target_user_channel = await client.channel_private_create(target_user)
    except ConnectionError:
        return
    
    embed = Embed(
        f'{source_user.full_name}\'s {EMOJI__HEART_CURRENCY:r} has been transferred to you.',
        color = COLOR__GAMBLING,
    ).add_field(
        f'Your {EMOJI__HEART_CURRENCY:r}',
        f'{target_user_total_love} -> {target_user_total_love+source_user_total_love}',
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    try:
        await client.message_create(target_user_channel, embed=embed)
    except ConnectionError:
        return
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user:
            return
        
        raise


@SLASH_CLIENT.interactions(guild=GUILD__NEKO_DUNGEON, allow_by_default=False)
@set_permission(GUILD__NEKO_DUNGEON, ROLE__NEKO_DUNGEON__ADMIN, True)
async def currency_insert(client, event,
        target_user: ('user', 'To who do you want transfer the taken heart?'),
        hearts : ('int', 'The amount to insert'),
        dailies : ('int', 'The amount of daily streaks'),
            ):
    """Inserts a new field into the currency table"""
    if not event.user.has_role(ROLE__NEKO_DUNGEON__ADMIN):
        abort(f'{ROLE__NEKO_DUNGEON__ADMIN.mention} only!', allowed_mentions=None)
    
    user_id = target_user.id
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id = results[0][0]
            entry_found = True
        else:
            entry_id = 0
            entry_found = False
        
        if entry_found:
            to_execute = USER_COMMON_TABLE.update(
                user_common_model.id == entry_id,
            ).values(
                total_love      = hearts,
                daily_next      = datetime.utcnow(),
                daily_streak    = dailies,
                total_allocated = 0,
            )
        else:
            to_execute = get_create_common_user_expression(
                user_id,
                total_love = hearts,
                daily_streak = dailies,
            )
        
        await connector.execute(to_execute)
    
    yield Embed(
        'Inserting into currency table',
        color = COLOR__GAMBLING,
    ).add_field(
        'User',
        target_user.full_name,
    ).add_field(
        'Hearts',
        str(hearts),
    ).add_field(
        'Dailies',
        str(dailies),
    )


@SLASH_CLIENT.interactions(is_global=True)
async def top_list(client, event,
        page : ('number', 'page?') = 1,
            ):
    """A list of my best simps."""
    if page < 1:
        page = 1
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.user_id,
                    user_common_model.total_love,
                ]
            ).where(
                user_common_model.total_love != 0,
            ).order_by(
                desc(user_common_model.total_love),
            ).limit(
                20,
            ).offset(
                20*(page-1),
            )
        )
        
        results = await response.fetchall()
        
        parts = []
        max_hearts = 0
        
        for index, (user_id, total_hearts) in enumerate(results, (page*20)-19):
            try:
                user = USERS[user_id]
            except KeyError:
                try:
                    user = await client.user_get(user_id)
                except BaseException as err:
                    if isinstance(err, ConnectionError):
                        return
                    
                    if isinstance(err, DiscordException):
                        if err.code == ERROR_CODES.unknown_user:
                            user = ZEROUSER
                        else:
                            raise
                    
                    else:
                        raise
            
            if total_hearts > max_hearts:
                max_hearts = total_hearts
            parts.append((index, total_hearts, user.full_name))
    
    result_parts = [
        EMOJI__HEART_CURRENCY.as_emoji,
        ' **Top-list** ',
        EMOJI__HEART_CURRENCY.as_emoji,
    ]
    
    if page != 1:
        result_parts.append(' *[Page ')
        result_parts.append(repr(page))
        result_parts.append(']*')
    
    result_parts.append('\n```')
    
    if max_hearts:
        result_parts.append('cs\n')
        index_adjust = floor(log10((page-1)*20+len(parts)))+1
        hearts_adjust = floor(log10(max_hearts))+1
        
        for index, total_hearts, full_name in parts:
            result_parts.append(str(index).rjust(index_adjust))
            result_parts.append('.: ')
            result_parts.append(str(total_hearts).rjust(hearts_adjust))
            result_parts.append(' ')
            result_parts.append(full_name)
            result_parts.append('\n')
    else:
        result_parts.append('\n*no result*\n')
    
    result_parts.append('```')
    
    yield ''.join(result_parts)
    return


HEART_SHOP = SLASH_CLIENT.interactions(
    None,
    name = 'heart-shop',
    description = 'Trade your love!',
    is_global = True,
)


NSFW_ACCESS_IDENTIFIER = '0'
ELEVATED_IDENTIFIER = '1'
HEART_BOOST_IDENTIFIER = '2'

BUYABLE_ROLES = {
    NSFW_ACCESS_IDENTIFIER: (ROLE__NEKO_DUNGEON__NSFW_ACCESS, NSFW_ACCESS_COST),
    ELEVATED_IDENTIFIER: (ROLE__NEKO_DUNGEON__ELEVATED, ELEVATED_COST),
    HEART_BOOST_IDENTIFIER: (ROLE__NEKO_DUNGEON__HEART_BOOST, HEART_BOOST_COST),
}

ROLE_CHOICES = [
    (f'Horny ({NSFW_ACCESS_COST})', NSFW_ACCESS_IDENTIFIER),
    (f'Nekogirl Worshipper ({ELEVATED_COST})', ELEVATED_IDENTIFIER),
    (f'Koishi enjoyer ({HEART_BOOST_COST})', HEART_BOOST_IDENTIFIER),
]


@HEART_SHOP.interactions
async def roles(client, event,
        role_: (ROLE_CHOICES, 'Choose a role to buy!')
            ):
    """Buy roles to enhance your love!"""
    role, cost = BUYABLE_ROLES[role_]
    
    user = event.user
    guild = role.guild
    if (client.get_guild_profile_for(guild) is None):
        abort(f'You must be in {guild.name} to buy any role.')
    
    if user.has_role(role):
        abort(f'You already have {role.name} role.')
    
    user_id = user.id
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.total_love,
                    user_common_model.total_allocated,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        results = await response.fetchall()
        
        if results:
            total_love, total_allocated = results[0]
            available_love = total_love-total_allocated
        else:
            total_love = 0
            available_love = 0
        
        if available_love > cost:
            bought = True
        else:
            bought = False
        
        
        if bought:
            yield
            
            await client.user_role_add(user, role)
            
            await connector.execute(USER_COMMON_TABLE. \
                update(user_common_model.user_id == user_id). \
                values(
                    total_love = user_common_model.total_love-cost,
                )
            )
    
    embed = Embed(f'Buying {role.name} for {cost} {EMOJI__HEART_CURRENCY:e}'). \
        add_thumbnail(client.avatar_url)
    
    if bought:
        embed.description = 'Was successful.'
        embed.add_field(
            f'Your {EMOJI__HEART_CURRENCY:e}',
            f'{total_love} -> {total_love-cost}',
        )
    else:
        embed.description = 'You have insufficient amount of hearts.'
        embed.add_field(
            f'Your {EMOJI__HEART_CURRENCY:e}',
            str(total_love),
        )
    
    yield embed


# ((d+1)*d)>>1 - (((d-a)+1)*(d-a))>>1
# (((d+1)*d) - (((d-a)+1)*(d-a)))>>1
# (d*d+d - (((d-a)+1)*(d-a)))>>1
# (d*d+d - ((d-a+1)*(d-a)))>>1
# (d*d+d - (d*d-d*a+d-d*a+a*a-a))>>1
# (d*d+d - (d*d - d*a + d - d*a + a*a - a))>>1
# (d*d+d + (-d*d + d*a - d + d*a - a*a + a))>>1
# (d*d + d - d*d + d*a - d + d*a - a*a + a)>>1
# (d + d*a - d + d*a - a*a + a)>>1
# (d*a + d*a - a*a + a)>>1
# (d*a + d*a - a*a + a)>>1
# (2*d*a - a*a + a)>>1
# (a*(2*d - a + 1))>>1
# (a*((d<<1) - a + 1))>>1
# (a*((d<<1)-a+1))>>1

DAILY_REFUND_MIN = 124

def calculate_sell_price(daily_count, daily_refund):

    under_price = DAILY_REFUND_MIN-daily_count+daily_refund
    if under_price < 0:
        under_price = 0
        over_price = daily_refund
    else:
        if under_price > daily_refund:
            under_price = daily_refund
            over_price = 0
        else:
            over_price = daily_refund-under_price
    
    price = 0
    
    if over_price:
        price += (over_price*((daily_count<<1)-over_price+1))>>1
    
    if under_price:
        price += (under_price*DAILY_REFUND_MIN)
    
    return price



@HEART_SHOP.interactions
async def sell_daily(client, event,
        amount: ('number', 'How much?'),
            ):
    """Sell excess daily streak for extra hearts."""
    if amount < 1:
        abort('`amount` must be non-negative!')
    
    user_id = event.user.id
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                    user_common_model.total_love,
                    user_common_model.daily_streak,
                    user_common_model.daily_next,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        
        results = await response.fetchall()
        if results:
            entry_id, total_love, daily_streak, daily_next = results[0]
            now = datetime.utcnow()
            if daily_next < now:
                daily_streak, daily_next = calculate_daily_new(daily_streak, daily_next, now)
        
        else:
            entry_id = -1
            total_love = 0
            daily_streak = 0
        
        if amount <= daily_streak:
            sell_price = calculate_sell_price(daily_streak, amount)
            
            await connector.execute(USER_COMMON_TABLE. \
                update(user_common_model.id == entry_id). \
                values(
                    total_love = user_common_model.total_love+sell_price,
                    daily_next = daily_next,
                    daily_streak = daily_streak-amount,
                )
            )
            
            sold = True
        else:
            sold = False
    
    embed = Embed(f'Selling {amount} daily for {EMOJI__HEART_CURRENCY:e}'). \
        add_thumbnail(client.avatar_url)
    
    if sold:
        embed.description = 'Great success!'
        embed.add_field(
            f'Your daily streak',
            f'{daily_streak} -> {daily_streak-amount}',
        )
        embed.add_field(
            f'Your {EMOJI__HEART_CURRENCY:e}',
            f'{total_love} -> {total_love+sell_price}',
        )
    else:
        embed.description = 'You have insufficient amount of daily streak.'
        embed.add_field(
            f'Your daily streak',
            str(daily_streak),
        )
    
    return embed


HEART_GENERATOR_COOLDOWNS = set()
HEART_GENERATOR_COOLDOWN = 3600.0
HEART_GENERATION_AMOUNT = 10
HEART_BUMP_AMOUNT = 100

BUMP_RP = re.compile(
    '<@!?(\d{7,21})>, \n'
    ' {6}Bump done :thumbsup:\n' # This is really not an emoji!
    ' {6}Check it on DISBOARD: https://disboard\.org/'
)


async def increase_user_total_love(user_id, increase):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_common_model.id,
                ]
            ).where(
                user_common_model.user_id == user_id,
            )
        )
        results = await response.fetchall()
        if results:
            entry_id = results[0][0]
            to_execute = USER_COMMON_TABLE. \
                update(user_common_model.id == entry_id). \
                values(
                    total_love = user_common_model.total_love+increase,
                )
        else:
            to_execute = get_create_common_user_expression(
                user_id,
                total_love = increase,
            )
        
        await connector.execute(to_execute)


async def heart_generator(client, message):
    user = message.author
    if user.is_bot:
        if user is USER__DISBOARD:
            embeds = message.embeds
            if (embeds is not None):
                content = embeds[0].description
                if (content is not None):
                    matched = BUMP_RP.fullmatch(content)
                    if (matched is not None):
                        user_id = int(matched.group(1))
                        await increase_user_total_love(user_id, HEART_BUMP_AMOUNT)
        
        return
    
    if random() < 0.01:
        user_id = user.id
        if user_id not in HEART_GENERATOR_COOLDOWNS:
            HEART_GENERATOR_COOLDOWNS.add(user_id)
            
            KOKORO.call_later(HEART_GENERATOR_COOLDOWN, set.remove, HEART_GENERATOR_COOLDOWNS, user_id)
            await increase_user_total_love(user_id, HEART_GENERATION_AMOUNT)
        
