import re
from functools import partial as partial_func
from datetime import datetime, timedelta
from random import random
from math import log, ceil, floor
from itertools import chain

from hata import Client, elapsed_time, Embed, Color, BUILTIN_EMOJIS, DiscordException, Task, Future, KOKORO, \
    ERROR_CODES, USERS, ZEROUSER, ChannelGuildBase, WaitTillAll, future_or_timeout, parse_tdelta
from hata.ext.command_utils import Timeouter, GUI_STATE_READY, GUI_STATE_SWITCHING_CTX, \
    GUI_STATE_CANCELLED, GUI_STATE_CANCELLING, GUI_STATE_SWITCHING_PAGE
from hata.ext.slash import abort, InteractionResponse, set_permission, Button, Row, wait_for_component_interaction

from sqlalchemy.sql import select, desc

from bot_utils.models import DB_ENGINE, currency_model, CURRENCY_TABLE
from bot_utils.shared import ROLE__NEKO_DUNGEON__ELEVATED, ROLE__NEKO_DUNGEON__BOOSTER, GUILD__NEKO_DUNGEON, \
    EMOJI__HEART_CURRENCY, USER__DISBOARD, ROLE__NEKO_DUNGEON__HEART_BOOST, ROLE__NEKO_DUNGEON__ADMIN

SLASH_CLIENT: Client
def setup(lib):
    SLASH_CLIENT.events.message_create.append(GUILD__NEKO_DUNGEON, heart_generator)

def teardown(lib):
    SLASH_CLIENT.events.message_create.remove(GUILD__NEKO_DUNGEON, heart_generator)


GAMBLING_COLOR          = Color.from_rgb(254, 254, 164)
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

CARD_TYPES = (
    BUILTIN_EMOJIS['spades'].as_emoji,
    BUILTIN_EMOJIS['clubs'].as_emoji,
    BUILTIN_EMOJIS['hearts'].as_emoji,
    BUILTIN_EMOJIS['diamonds'].as_emoji,
)

CARD_NUMBERS = (
    BUILTIN_EMOJIS['two'].as_emoji,
    BUILTIN_EMOJIS['three'].as_emoji,
    BUILTIN_EMOJIS['four'].as_emoji,
    BUILTIN_EMOJIS['five'].as_emoji,
    BUILTIN_EMOJIS['six'].as_emoji,
    BUILTIN_EMOJIS['seven'].as_emoji,
    BUILTIN_EMOJIS['eight'].as_emoji,
    BUILTIN_EMOJIS['nine'].as_emoji,
    BUILTIN_EMOJIS['keycap_ten'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_j'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_q'].as_emoji,
    BUILTIN_EMOJIS['regional_indicator_k'].as_emoji,
    BUILTIN_EMOJIS['a'].as_emoji,
)

DECK_SIZE   = len(CARD_TYPES) * len(CARD_NUMBERS)
ACE_INDEX   = len(CARD_NUMBERS)-1
BET_MIN     = 10

IN_GAME_IDS = set()

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


@SLASH_CLIENT.interactions(is_global=True)
async def daily(client, event,
        target_user : ('user', 'Anyone to gift your daily love?') = None,
             ):
    """Claim a share of my love every day or gift it to your imouto nya!"""
    source_user = event.user
    if target_user is None:
        target_user = source_user
    
    now = datetime.utcnow()
    async with DB_ENGINE.connect() as connector:
        if source_user is target_user:
            response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==source_user.id))
            results = await response.fetchall()
            if results:
                source_result = results[0]
                daily_next = source_result.daily_next
                if daily_next > now:
                    return Embed(
                        'You already claimed your daily love for today~',
                        f'Come back in {elapsed_time(daily_next)}.',
                        color=GAMBLING_COLOR,
                    )
                
                daily_streak = calculate_daily_new_only(source_result.daily_streak, daily_next, now)
                
                if daily_next+DAILY_STREAK_BREAK < now:
                    streak_text = f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
                else:
                    streak_text = f'You are in a {daily_streak+1} day streak! Keep up the good work!'
                
                received = calculate_daily_for(source_user, daily_streak)
                total_love = source_result.total_love+received
                
                daily_streak += 1
                await connector.execute(CURRENCY_TABLE. \
                    update(currency_model.id==source_result.id). \
                    values(
                        total_love  = total_love,
                        daily_next  = now+DAILY_INTERVAL,
                        daily_streak= daily_streak,
                    )
                )
                
                return Embed(
                    'Here, some love for you~\nCome back tomorrow !',
                    f'You received {received} {EMOJI__HEART_CURRENCY:e} and now have {total_love} {EMOJI__HEART_CURRENCY:e}\n'
                    f'{streak_text}',
                    color=GAMBLING_COLOR,
                )
            
            received = calculate_daily_for(source_user, 0)
            await connector.execute(
                CURRENCY_TABLE.insert().values(
                    user_id         = source_user.id,
                    total_love      = received,
                    daily_next      = now+DAILY_INTERVAL,
                    daily_streak    = 1,
                    total_allocated = 0,
                )
            )
            
            return Embed(
                'Here, some love for you~\nCome back tomorrow !',
                f'You received {received} {EMOJI__HEART_CURRENCY:e} and now have {received} {EMOJI__HEART_CURRENCY:e}',
                color = GAMBLING_COLOR)
        
        response = await connector.execute(
            CURRENCY_TABLE.select(currency_model.user_id.in_([source_user.id, target_user.id,]))
        )
        
        results = await response.fetchall()
        if len(results) == 0:
            source_result = None
            target_result = None
        elif len(results) == 1:
            if results[0].user_id == source_user.id:
                source_result = results[0]
                target_result = None
            else:
                source_result = None
                target_result = results[0]
        else:
            if results[0].user_id == source_user.id:
                source_result = results[0]
                target_result = results[1]
            else:
                source_result = results[1]
                target_result = results[0]
        
        now = datetime.utcnow()
        if source_result is None:
            daily_streak = 0
            streak_text = 'I am happy you joined the sect too.'
            
            await connector.execute(
                CURRENCY_TABLE.insert().values(
                    user_id         = source_user.id,
                    total_love      = 0,
                    daily_next      = now+DAILY_INTERVAL,
                    daily_streak    = 1,
                    total_allocated = 0,
                )
            )
        else:
            daily_next = source_result.daily_next
            if daily_next > now:
                return Embed(
                    'You already claimed your daily love for today~',
                    f'Come back in {elapsed_time(daily_next)}.',
                    color = GAMBLING_COLOR)
            
            daily_streak = source_result.daily_streak
            daily_next = daily_next+DAILY_STREAK_BREAK
            if daily_next < now:
                daily_streak = daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
            
            if daily_streak < 0:
                daily_streak = 0
            
            if daily_next < now:
                streak_text = f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
            else:
                streak_text = f'You are in a {daily_streak+1} day streak! Keep up the good work!'
            
            await connector.execute(CURRENCY_TABLE.update(
                currency_model.id==source_result.id).values(
                    daily_next  = now+DAILY_INTERVAL,
                    daily_streak= daily_streak+1,
                )
            )
        
        received = calculate_daily_for(source_user, daily_streak)
        
        if target_result is None:
            await connector.execute(
                    CURRENCY_TABLE.insert().values(
                    user_id         = target_user.id,
                    total_love      = received,
                    daily_next      = now,
                    daily_streak    = 0,
                    total_allocated = 0,
                )
            )
            
            total_love = received
        else:
            total_love = target_result.total_love+received
            
            await connector.execute(CURRENCY_TABLE. \
                update(currency_model.id==target_result.id). \
                values(
                    total_love  = total_love,
                )
            )
    
    return Embed(
        f'Awww, you claimed your daily love for {target_user:f}, how sweet~',
        f'You gifted {received} {EMOJI__HEART_CURRENCY:e} and they have {total_love} {EMOJI__HEART_CURRENCY:e}\n'
        f'{streak_text}',
        color = GAMBLING_COLOR,
    )


@SLASH_CLIENT.interactions(is_global=True)
async def hearts(client, event,
        target_user: ('user', 'Do you wanna know some1 else\'s hearts?') = None,
        extended: ('bool', 'Extended info.') = False
            ):
    """How many hearts do you have?"""
    if target_user is None:
        target_user = event.user
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==target_user.id))
        results = await response.fetchall()
    
        if results:
            result = results[0]
            total_love = result.total_love
            daily_next = result.daily_next
            daily_streak = result.daily_streak
            total_allocated = result.total_allocated
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
            await connector.execute(CURRENCY_TABLE. \
                update(currency_model.id == result.id). \
                values(
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
    
    embed = Embed(title, description, color=GAMBLING_COLOR)
    
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
        if (not permissions.can_send_messages) or (not permissions.can_add_reactions) or \
                (not permissions.can_use_external_emojis):
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
        return Embed(title, description, color=GAMBLING_COLOR)

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
            select([currency_model.id]). \
            where(currency_model.user_id==user.id)
        )
        
        results = await response.fetchall()
        if results:
            entry_id = results[0][0]
            to_execute = CURRENCY_TABLE. \
                update(currency_model.id==entry_id). \
                values(total_love=currency_model.total_love+self.amount)
        
        else:
            to_execute = CURRENCY_TABLE.insert().values(
                user_id         = user_id,
                total_love      = self.amount,
                daily_next      = datetime.utcnow(),
                daily_streak    = 0,
                total_allocated = 0,
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
        if (not permissions.can_send_messages) or (not permissions.can_add_reactions) or \
                (not permissions.can_use_external_emojis):
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
        return Embed(title, description, color=GAMBLING_COLOR)
    
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
            select([
                currency_model.id,
                currency_model.daily_streak,
                currency_model.daily_next
            ]). \
            where(currency_model.user_id==user_id)
        )
        
        results = await response.fetchall()
        if results:
            entry_id, daily_streak, daily_next = results[0]
            now = datetime.utcnow()
            
            daily_streak, daily_next = calculate_daily_new(daily_streak, daily_next, now)
            daily_streak = daily_streak+self.amount
            
            to_execute = CURRENCY_TABLE. \
                update(currency_model.id==entry_id). \
                values(
                    daily_streak= daily_streak,
                    daily_next  = daily_next,
                )
        
        else:
            to_execute = CURRENCY_TABLE.insert().values(
                user_id         = user_id,
                total_love      = 0,
                daily_next      = datetime.utcnow(),
                daily_streak    = self.amount,
                total_allocated = 0,
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


@SLASH_CLIENT.interactions(name='21', is_global=True)
async def game_21(client, event,
        amount : ('int', 'The amount of hearts to bet'),
        mode : ([('single-player', 'sg'), ('multi-player', 'mp')], 'Game mode, yayyy') = 'sg',
            ):
    """Starts a card game where you can bet your hearts."""
    is_multi_player = (mode == 'mp')
    
    permissions = event.channel.cached_permissions_for(client)
    if (not permissions.can_send_messages) or (not permissions.can_add_reactions) or \
            (not permissions.can_use_external_emojis):
        abort('I require `send messages`, `add reactions` and `user external emojis` permissions to invoke this '
            'command.')
    
    embed = game_21_precheck(client, event.user, event.channel, amount, is_multi_player)
    yield embed
    if (embed is not None):
        return
    
    if is_multi_player:
        coroutine_function = game_21_multi_player
    else:
        coroutine_function = game_21_single_player
    
    await coroutine_function(client, event, amount)

def should_render_exception(exception):
    if isinstance(exception, ConnectionError):
        # no internet
        return False
    
    if isinstance(exception, DiscordException) and exception.code in (
                ERROR_CODES.unknown_message, # message deleted
                ERROR_CODES.unknown_channel, # message's channel deleted
                ERROR_CODES.missing_access, # client removed
                ERROR_CODES.missing_permissions, # permissions changed meanwhile
                ERROR_CODES.cannot_message_user, # user dm-s disabled or bot blocked.
                ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
            ):
         return False
    
    return True



class Game21Base:
    __slots__ = ('guild', 'all_pulled')
    def __new__(cls, guild):
        self = object.__new__(cls)
        self.guild = guild
        self.all_pulled = []
        return self
    
    def create_user_player(self, user):
        return Game21Player(self, user)
    
    def create_bot_player(self, user):
        player = Game21Player(self, user)
        player.auto_finish()
        return player
    
    def pull_card(self):
        all_pulled = self.all_pulled
        card = int((DECK_SIZE-len(all_pulled))*random())
        for pulled in all_pulled:
            if pulled > card:
                break
            
            card += 1
            continue
        
        all_pulled.append(card)
        all_pulled.sort()
        
        return card

class Game21Player:
    __slots__ = ('parent', 'user', 'hand', 'total', 'ace')
    def __new__(cls, parent, user):
        hand = []
        total = 0
        ace = 0
        
        while True:
            card = parent.pull_card()
            
            hand.append(card)
            
            number_index = card%len(CARD_NUMBERS)
            if number_index == ACE_INDEX:
                ace += 1
                card_weight = 11
            elif number_index > 7:
                card_weight = 10
            else:
                card_weight = number_index+2
            
            total += card_weight
            
            if total > 10 and len(hand) >= 2:
                break
        
        # We might draw 2 ace, at that case we hit 22.
        if total > 21:
            ace -= 1
            total -= 10
        
        self = object.__new__(cls)
        self.parent = parent
        self.user = user
        self.hand = hand
        self.total = total
        self.ace = ace
        return self
    
    def auto_finish(self):
        hand = self.hand
        total = self.total
        ace = self.ace
        
        while True:
            if total > (17 if ace else 15):
                break
            
            card = self.parent.pull_card()
            
            hand.append(card)
            
            number_index = card%len(CARD_NUMBERS)
            if number_index == ACE_INDEX:
                ace += 1
                card_weight = 11
            elif number_index > 7:
                card_weight = 10
            else:
                card_weight = number_index+2
            
            total += card_weight
            
            while total>21 and ace:
                total -= 10
                ace -= 1
            
            continue
        
        self.total = total
        self.ace = ace
    
    def pull_card(self):
        hand = self.hand
        total = self.total
        ace = self.ace
        
        card = self.parent.pull_card()
        
        hand.append(card)
        
        number_index = card%len(CARD_NUMBERS)
        if number_index == ACE_INDEX:
            ace += 1
            card_weight = 11
        elif number_index > 7:
            card_weight = 10
        else:
            card_weight = number_index+2
        
        total += card_weight
        
        while total>21 and ace:
            total -= 10
            ace -= 1
            
        self.total = total
        self.ace = ace
        
        # Return whether the user is done.
        if total >= 21:
            return True
        
        return False
    
    def add_done_embed_field(self, embed):
        field_content = []
        
        for round_, card in enumerate(self.hand, 1):
            type_index, number_index = divmod(card, len(CARD_NUMBERS))
            field_content.append('Round ')
            field_content.append(str(round_))
            field_content.append(': ')
            field_content.append(CARD_TYPES[type_index])
            field_content.append(' ')
            field_content.append(CARD_NUMBERS[number_index])
            field_content.append('\n')
        
        embed.add_field(f'{self.user.name_at(self.parent.guild)}\'s cards\'\nWeight: {self.total}',
            ''.join(field_content), inline=True)
    
    def add_hand(self, embed):
        for round_, card in enumerate(self.hand, 1):
            type_index, number_index = divmod(card, len(CARD_NUMBERS))
            embed.add_field(f'Round {round_}',
                f'You pulled {CARD_TYPES[type_index]} {CARD_NUMBERS[number_index]}')
        
    def create_gamble_embed(self, amount):
        embed = Embed(f'How to gamble {amount} {EMOJI__HEART_CURRENCY.as_emoji}',
            f'You have cards equal to {self.total} weight at your hand.',
            color=GAMBLING_COLOR)
        
        self.add_hand(embed)
        
        return embed
    
    def create_after_embed(self, amount):
        embed = Embed(f'Gambled {amount} {EMOJI__HEART_CURRENCY.as_emoji}',
            f'You have cards equal to {self.total} weight at your hand.\n'
            'Go back to the other channel and wait till all the player finishes the game and the winner will be '
            'announced!',
            color=GAMBLING_COLOR)
        
        self.add_hand(embed)
        
        return embed

GAME_21_STEP_NEW = BUILTIN_EMOJIS['new']
GAME_21_STEP_STOP = BUILTIN_EMOJIS['octagonal_sign']
GAME_21_STEP_EMOJIS = (GAME_21_STEP_NEW, GAME_21_STEP_STOP)

GAME_21_JOIN_ENTER = BUILTIN_EMOJIS['hand_splayed']
GAME_21_JOIN_START = BUILTIN_EMOJIS['ok_hand']
GAME_21_JOIN_CANCEL = BUILTIN_EMOJIS['x']
GAME_21_JOIN_EMOJIS = (GAME_21_JOIN_ENTER, GAME_21_JOIN_START, GAME_21_JOIN_CANCEL)

GAME_21_RESULT_FINISH = 0
GAME_21_RESULT_INITIALIZATION_ERROR = 1
GAME_21_RESULT_IN_GAME_ERROR = 2
GAME_21_RESULT_CANCELLED_TIMEOUT = 3
GAME_21_RESULT_CANCELLED_UNKNOWN = 4
GAME_21_RESULT_CANCELLED_BY_USER = 5

GAME_21_TIMEOUT = 300.0
GAME_21_CANCELLATION_TIMEOUT = 5.0

class Game21PlayerRunner:
    __slots__ = ('player', 'message', 'waiter', 'channel', 'client', 'amount', '_timeouter', 'canceller', '_task_flag',
        'render_after', )
    
    async def __new__(cls, client, base, user, channel, amount, render_after, event=None):
        player = base.create_user_player(user)
        
        waiter = Future(KOKORO)
        if player.total >= 21:
            if render_after:
                embed = player.create_after_embed(amount)
                try:
                    message = await client.message_create(channel, embed=embed)
                except BaseException as err:
                    if should_render_exception(err):
                        await client.events.error(client, f'{cls.__name__}.__new__', err)
                    message = None
            else:
                message = None
            
            waiter.set_result(GAME_21_RESULT_FINISH)
        else:
            embed = player.create_gamble_embed(amount)
            
            try:
                if event is None:
                    message = await client.message_create(channel, embed=embed)
                else:
                    if not event.is_acknowledged():
                        await client.interaction_response_message_create(event)
                    message = await client.interaction_followup_message_create(event, embed=embed)
                for emoji in GAME_21_STEP_EMOJIS:
                    await client.reaction_add(message, emoji)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, f'{cls.__name__}.__new__', err)
                
                waiter.set_result_if_pending(GAME_21_RESULT_INITIALIZATION_ERROR)
                message = None
        
        self = object.__new__(cls)
        self.player = player
        self.waiter = waiter
        self.message = message
        self.channel = channel
        self.amount = amount
        self.client = client
        self.render_after = render_after
        
        if message is None:
            self._timeouter = None
            self.canceller = None
            self._task_flag = GUI_STATE_SWITCHING_CTX
        else:
            self._timeouter = Timeouter(self, timeout=GAME_21_TIMEOUT)
            self.canceller = cls._canceller
            self._task_flag = GUI_STATE_READY
            client.events.reaction_add.append(message, self)
            client.events.reaction_delete.append(message, self)
        
        return self
    
    async def __call__(self, client, event):
        if (event.user is not self.player.user) or (event.emoji not in GAME_21_STEP_EMOJIS):
            return
        
        if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
            return
        
        emoji = event.emoji
        task_flag = self._task_flag
        if task_flag != GUI_STATE_READY:
            if task_flag == GUI_STATE_SWITCHING_PAGE:
                if emoji is GAME_21_STEP_STOP:
                    self._task_flag = GUI_STATE_CANCELLING
                return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        if emoji is GAME_21_STEP_NEW:
            # It is enough to delete the reaction at this ase if needed,
            # because after the other cases we will delete them anyways.
            game_ended = self.player.pull_card()
            
        elif emoji is GAME_21_STEP_STOP:
            game_ended = True
        
        else:
            # should not happen
            return
        
        if game_ended:
            self._task_flag = GUI_STATE_SWITCHING_CTX
            self.waiter.set_result_if_pending(GAME_21_RESULT_FINISH)
            
            if self.render_after:
                await self._canceller_render_after()
            
            self.cancel()
            return
        
        self._task_flag = GUI_STATE_SWITCHING_PAGE
        
        embed = self.player.create_gamble_embed(self.amount)
        
        try:
            await client.message_edit(self.message, embed)
        except BaseException as err:
            self._task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            if should_render_exception(err):
                await client.events.error(client, f'{self.__class__.__name__}.__new__', err)
            
            self.waiter.set_result_if_pending(GAME_21_RESULT_IN_GAME_ERROR)
        
        if self._task_flag == GUI_STATE_CANCELLING:
            self._task_flag = GUI_STATE_CANCELLED
            self.waiter.set_result_if_pending(GAME_21_RESULT_FINISH)
            self.cancel()
        else:
            self._task_flag = GUI_STATE_READY
            self._timeouter.set_timeout(GAME_21_TIMEOUT)
    
    async def _canceller(self, exception):
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self._task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self._task_flag = GUI_STATE_CANCELLED
        
        if exception is None:
            if self.render_after:
                await self._canceller_render_after()
            return
        
        if isinstance(exception, TimeoutError):
            self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_TIMEOUT)
            if self.render_after:
                await self._canceller_render_after()
            else:
                if self.channel.cached_permissions_for(client).can_manage_messages:
                    try:
                        await client.reaction_clear(message)
                    except BaseException as err:
                        if should_render_exception(err):
                            await client.events.error(client, f'{self.__class__.__name__}._canceller', err)
            return
        
        self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_UNKNOWN)
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        # We do nothing.
    
    def cancel(self, exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)
    
    async def _canceller_render_after(self):
        client = self.client
        message = self.message
        embed = self.player.create_after_embed(self.amount)
        try:
            await client.message_edit(message, embed)
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, f'{self.__class__.__name__}._canceller_render_after', err)
        
        if self.channel.cached_permissions_for(client).can_manage_messages:
            try:
                await client.reaction_clear(message)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, f'{self.__class__.__name__}._canceller_render_after', err)
        else:
            for emoji in GAME_21_STEP_EMOJIS:
                try:
                    await client.reaction_delete_own(message, emoji)
                except BaseException as err:
                    if should_render_exception(err):
                        await client.events.error(client, f'{self.__class__.__name__}._canceller_render_after', err)
                    break

def game_21_precheck(client, user, channel, amount, require_guild):
    if user.id in IN_GAME_IDS:
        error_message = 'You are already at a game.'
    elif amount < BET_MIN:
        error_message = f'You must bet at least {BET_MIN} {EMOJI__HEART_CURRENCY.as_emoji}'
    elif not channel.cached_permissions_for(client).can_add_reactions:
        error_message = 'I need to have `add reactions` permissions to execute this command.'
    elif require_guild and (not isinstance(channel, ChannelGuildBase)):
        error_message = 'Guild only command.'
    else:
        return
    
    return Embed('Ohoho', error_message, color=GAMBLING_COLOR)

async def game_21_postcheck(client, user, channel, amount):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([currency_model.id, currency_model.total_love, currency_model.total_allocated]). \
            where(currency_model.user_id==user.id)
        )
        
        results = await response.fetchall()
        if results:
            entry_id, total_love, total_allocated = results[0]
        else:
            total_love = 0
            total_allocated = 0
            entry_id = -1
        
        if total_love-total_allocated < amount:
            error_message = f'You have just {total_love} {EMOJI__HEART_CURRENCY.as_emoji}'
        else:
            return entry_id, None
    
    return entry_id, Embed('Ohoho', error_message, color=GAMBLING_COLOR)


async def game_21_single_player(client, event, amount):
    user = event.user
    channel = event.channel
    
    IN_GAME_IDS.add(event.user.id)
    try:
        entry_id, embed = await game_21_postcheck(client, event.user, event.channel, amount)
        if (embed is not None):
            try:
                await client.interaction_followup_message_create(event, embed=embed)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_single_player', err)
            return
        
        base = Game21Base(channel.guild)
        
        player_client = base.create_bot_player(client)
        
        player_runner = await Game21PlayerRunner(client, base, user, channel, amount, False, event=event)
        player_user_waiter = player_runner.waiter
        if player_user_waiter.done() or (entry_id == -1):
            unallocate = False
        else:
            unallocate = True
            async with DB_ENGINE.connect() as connector:
                await connector.execute(CURRENCY_TABLE. \
                    update(currency_model.id == entry_id). \
                    values(total_allocated = currency_model.total_allocated-amount)
                )
        
        game_state = await player_user_waiter
        
        if game_state == GAME_21_RESULT_FINISH:
            client_total = player_client.total
            user_total = player_runner.player.total
            if client_total > 21:
                if user_total > 21:
                    winner = None
                else:
                    winner = user
            else:
                if user_total > 21:
                    winner = client
                else:
                    if client_total > user_total:
                        winner = client
                    elif client_total < user_total:
                        winner = user
                    else:
                        winner = None
            
            if winner is client:
                bonus = -amount
            elif winner is None:
                bonus = 0
            else:
                bonus = amount
            
            async with DB_ENGINE.connect() as connector:
                expression = CURRENCY_TABLE.update(currency_model.user_id == user.id)
                
                if amount:
                    expression = expression.values(total_love=currency_model.total_love+bonus)
                
                if unallocate:
                    expression = expression.values(total_allocated=currency_model.total_allocated-amount)
                
                await connector.execute(expression)
            
            if winner is None:
                title = f'How to draw.'
            elif winner is client:
                title = f'How to lose {amount} {EMOJI__HEART_CURRENCY.as_emoji}'
            else:
                title = f'How to win {amount} {EMOJI__HEART_CURRENCY.as_emoji}'
            
            embed = Embed(title, color=GAMBLING_COLOR)
            player_runner.player.add_done_embed_field(embed)
            player_client.add_done_embed_field(embed)
            
            if player_runner.message is None:
                coro = client.message_create(channel, embed=embed)
            else:
                coro = client.message_edit(player_runner.message, embed=embed)
            
            try:
                await coro
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_single_player', err)
            
            if (player_runner.message is not None) and channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(player_runner.message)
                except BaseException as err:
                    if should_render_exception(err):
                        await client.events.error(client, 'game_21_single_player', err)
            
            return
        
        if game_state == GAME_21_RESULT_CANCELLED_TIMEOUT:
            if entry_id != -1:
                async with DB_ENGINE.connect() as connector:
                    expression = CURRENCY_TABLE. \
                        update(currency_model.id == entry_id). \
                        values(
                        total_love=currency_model.total_love-amount
                    )
                    
                    if unallocate:
                        expression = expression.values(
                            total_allocated = currency_model.total_allocated-amount
                        )
                    
                    await connector.execute(expression)
            
            embed = Embed(f'Timeout occurred, you lost your {amount} {EMOJI__HEART_CURRENCY.as_emoji} forever.')
            
            if player_runner.message is None:
                coroutine = client.interaction_followup_message_create(event, embed=embed)
            else:
                coroutine = client.message_edit(player_runner.message, embed=embed)
            
            try:
                await coroutine
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_single_player', err)
                return
            
            return
        
        # Error occurred
        if unallocate:
            async with DB_ENGINE.connect() as connector:
                expression = CURRENCY_TABLE. \
                    update(currency_model.id == entry_id). \
                    values(total_allocated = currency_model.total_allocated-amount)
                
                await connector.execute(expression)
    
    finally:
        IN_GAME_IDS.discard(user.id)


def create_join_embed(users, amount):
    description_parts = [
        'Bet amount: ', str(amount), ' ', EMOJI__HEART_CURRENCY.as_emoji, '\n'
        'Creator: ', users[0].mention, '\n',
    ]
    
    if len(users) > 1:
        description_parts.append('\nJoined users:\n')
        for user in users[1:]:
            description_parts.append(user.mention)
            description_parts.append('\n')
    
    description_parts.append('\nReact with ')
    description_parts.append(GAME_21_JOIN_ENTER.as_emoji)
    description_parts.append(' to join.')
    
    description = ''.join(description_parts)
    
    return Embed('Game 21 multiplayer', description, color=GAMBLING_COLOR)


async def game_21_mp_user_joiner(client, user, guild, source_channel, amount, joined_user_ids, private_channel,
        entry_id):
    try:
        private_channel = await client.channel_private_create(user)
    except BaseException as err:
        if not isinstance(err, ConnectionError):
            await client.events.error(client, 'game_21_mp_user_joiner', err)
        
        return
    
    if user.id in IN_GAME_IDS:
        embed = Embed('Ohoho', 'You are already at a game.', color=GAMBLING_COLOR)
        try:
            await client.message_create(private_channel, embed=embed)
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, 'game_21_mp_user_joiner', err)
        
        return
    
    result = False
    IN_GAME_IDS.add(user.id)
    joined_user_ids.add(user.id)
    
    entry_id = -1
    
    try:
        entry_id, embed = await game_21_postcheck(client, user, private_channel, amount)
        if (embed is None):
            embed = Embed('21 multiplayer game joined.',
                f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
                f'Guild: {guild.name}\n'
                f'Channel: {source_channel.mention}',
                    color=GAMBLING_COLOR)
            
            try:
                await client.message_create(private_channel, embed)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_mp_user_joiner', err)
                
            else:
                result = True
    finally:
        if result:
            if (entry_id != -1):
                async with DB_ENGINE.connect() as connector:
                    await connector.execute(CURRENCY_TABLE. \
                        update(currency_model.id == entry_id). \
                        values(total_allocated = currency_model.total_allocated+amount)
                    )
            
            joined_tuple = user, private_channel, entry_id
        
        else:
            IN_GAME_IDS.discard(user.id)
            joined_user_ids.discard(user.id)
            joined_tuple = None
    
    return joined_tuple



async def game_21_refund(entry_id, amount):
    async with DB_ENGINE.connect() as connector:
        await connector.execute(CURRENCY_TABLE. \
            update(currency_model.id == entry_id). \
            values(total_allocated = currency_model.total_allocated-amount)
        )

async def game_21_mp_user_leaver(client, user, guild, source_channel, amount, joined_user_ids, private_channel,
        entry_id):
    IN_GAME_IDS.discard(user.id)
    joined_user_ids.discard(user.id)
    
    await game_21_refund(entry_id, amount)
    
    embed = Embed('21 multiplayer game left.',
        f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
        f'Guild: {guild.name}\n'
        f'Channel: {source_channel.mention}',
            color=GAMBLING_COLOR)
    
    try:
        await client.message_create(private_channel, embed=embed)
    except BaseException as err:
        if should_render_exception(err):
            await client.events.error(client, 'game_21_mp_user_leaver', err)


async def game_21_mp_cancelled(client, user, guild, source_channel, amount, private_channel, joined_user_ids, entry_id):
    IN_GAME_IDS.discard(user.id)
    joined_user_ids.discard(user.id)
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(CURRENCY_TABLE. \
            update(currency_model.id == entry_id). \
            values(total_allocated = currency_model.total_allocated-amount)
        )
    
    embed = Embed('21 multiplayer game was cancelled.',
        f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
        f'Guild: {guild.name}\n'
        f'Channel: {source_channel.mention}',
            color=GAMBLING_COLOR)
    
    try:
        await client.message_create(private_channel, embed)
    except BaseException as err:
        if should_render_exception(err):
            await client.events.error(client, 'game_21_mp_cancelled', err)


def game_21_mp_notify_cancellation(client, joined_tuples, amount, channel, guild, joined_user_ids):
    Task(game_21_refund(joined_tuples[0][2], amount), KOKORO)
    for notify_user, private_channel, entry_id in joined_tuples[1:]:
        Task(game_21_mp_cancelled(client, notify_user, guild, channel, amount, private_channel,
            joined_user_ids, entry_id), KOKORO)

GAME_21_MP_MAX_USERS = 10
GAME_21_MP_FOOTER = f'Max {GAME_21_MP_MAX_USERS} users allowed.'

class Game21JoinGUI:
    __slots__ = ('client', 'channel', 'message', 'waiter', 'amount', 'joined_tuples', '_timeouter', '_task_flag',
        'canceller', 'user_locks', 'joined_user_ids', 'workers', 'guild', 'message_sync_last_state',
        'message_sync_in_progress', 'message_sync_handle')
    
    async def __new__(cls, client, channel, joined_user_tuple, amount, joined_user_ids, guild, event=None):
        waiter = Future(KOKORO)
        
        embed = create_join_embed([joined_user_tuple[0]], amount)
        embed.add_footer(GAME_21_MP_FOOTER)
        
        try:
            if event is None:
                message = await client.message_create(channel, embed=embed)
            else:
                if not event.is_acknowledged():
                    await client.interaction_response_message_create(event)
                message = await client.interaction_followup_message_create(event, embed=embed)
            for emoji in GAME_21_JOIN_EMOJIS:
                await client.reaction_add(message, emoji)
            
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, f'{cls.__name__}.__new__', err)
            
            waiter.set_result_if_pending(GAME_21_RESULT_INITIALIZATION_ERROR)
            message = None
        
        self = object.__new__(cls)
        self.client = client
        self.channel = channel
        self.message = message
        self.waiter = waiter
        self.amount = amount
        self.joined_tuples = [joined_user_tuple]
        self.user_locks = set()
        self.joined_user_ids = joined_user_ids
        self.workers = set()
        self.guild = guild
        self.message_sync_last_state = self.joined_tuples.copy()
        self.message_sync_in_progress = False
        self.message_sync_handle = None
        
        if message is None:
            self._timeouter = None
            self.canceller = None
            self._task_flag = GUI_STATE_SWITCHING_CTX
        else:
            self._timeouter = Timeouter(self, timeout=GAME_21_TIMEOUT)
            self.canceller = cls._canceller
            self._task_flag = GUI_STATE_READY
            client.events.reaction_add.append(message, self)
            client.events.reaction_delete.append(message, self)
        
        return self
    
    async def __call__(self, client, event):
        if event.user.is_bot:
            return
        
        emoji = event.emoji
        if (emoji not in GAME_21_JOIN_EMOJIS):
            return
        
        # Do not remove emoji enter emoji if the user is the source one, instead leave.
        if event.user is not self.joined_tuples[0][0]:
            if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
                return
        
        task_flag = self._task_flag
        if task_flag != GUI_STATE_READY:
            if emoji is GAME_21_JOIN_CANCEL:
                self._task_flag = GUI_STATE_CANCELLING
            return
            
            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        if emoji is GAME_21_JOIN_ENTER:
            user = event.user
            
            if user.id in self.user_locks:
                # already doing something.
                return
            
            joined_tuples = self.joined_tuples
            if user is joined_tuples[0][0]:
                return
            
            for maybe_user, private_channel, entry_id in joined_tuples[1:]:
                if maybe_user is user:
                    join = False
                    break
            else:
                private_channel = None
                join = True
                entry_id = -1
            
            if join and (len(joined_tuples) == GAME_21_MP_MAX_USERS):
                return
            
            self.user_locks.add(user.id)
            try:
                if join:
                    coroutine_function = game_21_mp_user_joiner
                else:
                    coroutine_function = game_21_mp_user_leaver
                
                task = Task(coroutine_function(client, user, self.guild, self.channel, self.amount,
                    self.joined_user_ids, private_channel, entry_id), KOKORO)
                
                self.workers.add(task)
                try:
                    result = await task
                    if join:
                        if (result is not None):
                            self.joined_tuples.append(result)
                    else:
                        for index in range(1, len(joined_tuples)):
                            maybe_user = joined_tuples[index][0]
                            if maybe_user is user:
                                del joined_tuples[index]
                                break
                finally:
                    self.workers.discard(task)
            
            finally:
                self.user_locks.discard(user.id)
            
            self.maybe_message_sync()
            return
        
        if (event.user is not self.joined_tuples[0][0]):
            return
        
        if emoji is GAME_21_JOIN_START:
            self._task_flag = GUI_STATE_SWITCHING_CTX
            
            # Wait for all worker to finish
            await self._wait_for_cancellation()
            
            self.waiter.set_result_if_pending(GAME_21_RESULT_FINISH)
            self.cancel()
            return
        
        if emoji is GAME_21_JOIN_CANCEL:
            self._task_flag = GUI_STATE_CANCELLING
            
            # Wait for all workers to finish
            await self._wait_for_cancellation()
            
            self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_BY_USER)
            self.cancel()
            return
    
    async def _canceller(self, exception):
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        message_sync_handle = self.message_sync_handle
        if (message_sync_handle is not None):
            self.message_sync_handle = None
            message_sync_handle.cancel()
        
        if self._task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return
        
        self._task_flag = GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        await self._wait_for_cancellation()
        game_21_mp_notify_cancellation(client, self.joined_tuples, self.amount, self.channel, self.guild,
            self.joined_user_ids)
        
        if isinstance(exception, TimeoutError):
            self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_TIMEOUT)
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except BaseException as err:
                    if should_render_exception(err):
                        await client.events.error(client, f'{self.__class__.__name__}._canceller', err)
            return
        
        self.waiter.set_result_if_pending(GAME_21_RESULT_CANCELLED_UNKNOWN)
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
    def cancel(self, exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller = None
        
        timeouter = self._timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self, exception), KOKORO)

    
    async def _wait_for_cancellation(self):
        workers = self.workers
        if workers:
            future = WaitTillAll(workers, KOKORO)
            future_or_timeout(future, GAME_21_CANCELLATION_TIMEOUT)
            done, pending = await future
            for future in chain(done, pending):
                future.cancel()
    
    def maybe_message_sync(self):
        if not self.message_sync_in_progress:
            self.message_sync_in_progress = True
            Task(self.do_message_sync(), KOKORO)
    
    def call_message_sync(self):
        Task(self.do_message_sync(), KOKORO)
    
    async def do_message_sync(self):
        self.message_sync_handle = None
        
        if (self._task_flag != GUI_STATE_READY) or (self.joined_tuples == self.message_sync_last_state):
            self.message_sync_in_progress = False
            return
        
        self.message_sync_last_state = self.joined_tuples.copy()
        
        embed = create_join_embed([item[0] for item in self.joined_tuples], self.amount)
        embed.add_footer(GAME_21_MP_FOOTER)
        
        task = Task(self.client.message_edit(self.message, embed=embed), KOKORO)
        self.workers.add(task)
        try:
            try:
                await task
            except BaseException as err:
                if should_render_exception(err):
                    client = self.client
                    await client.events.error(client, f'{self.__class__.__name__}.__new__', err)
        finally:
            self.workers.discard(task)
        
        if (self._task_flag != GUI_STATE_READY) or (self.joined_tuples == self.message_sync_last_state):
            self.message_sync_in_progress = False
            return
        
        self.message_sync_handle = KOKORO.call_later(1.0, self.__class__.call_message_sync, self)


async def game_21_multi_player(client, event, amount):
    user = event.user
    channel = event.channel
    
    guild = channel.guild
    
    IN_GAME_IDS.add(user.id)
    joined_user_ids = set()
    joined_user_ids.add(user.id)
    try:
        entry_id, embed = await game_21_postcheck(client, user, channel, amount)
        if (embed is not None):
            return embed
        
        try:
            private_channel = await client.channel_private_create(user)
        except BaseException as err:
            if not isinstance(err, ConnectionError):
                await client.events.error(client, 'game_21_multi_player', err)
            
            return
        
        embed = Embed('21 multiplayer game created.',
            f'Bet amount: {amount} {EMOJI__HEART_CURRENCY.as_emoji}\n'
            f'Guild: {guild.name}\n'
            f'Channel: {channel.mention}',
                color=GAMBLING_COLOR)
        
        try:
            await client.message_create(private_channel, embed)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if (not isinstance(err, DiscordException)) or (err.code != ERROR_CODES.cannot_message_user):
                await client.events.error(client, 'game_21_multi_player', err)
                return
            
            private_open = False
        else:
            private_open = True
        
        if (not private_open):
            embed = Embed('Error', 'I cannot send private message to you.', color=GAMBLING_COLOR)
            
            try:
                await client.interaction_followup_message_create(event, embed=embed)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        join_gui = await Game21JoinGUI(client, channel, (user, private_channel, entry_id), amount, joined_user_ids, guild,
            event=event)
        game_state = await join_gui.waiter
        message = join_gui.message
        
        if game_state == GAME_21_RESULT_CANCELLED_TIMEOUT:
            embed = Embed('Timeout', 'Timeout occurred, the hearts were refund', color=GAMBLING_COLOR)
            
            try:
                await client.message_edit(message, embed=embed)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        if not (game_state == GAME_21_RESULT_FINISH or game_state == GAME_21_RESULT_CANCELLED_BY_USER):
            return
        
        if channel.cached_permissions_for(client).can_manage_messages:
            try:
                await client.reaction_clear(message)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
                return
        
        if game_state == GAME_21_RESULT_CANCELLED_BY_USER:
            game_21_mp_notify_cancellation(client, join_gui.joined_tuples, amount, channel, guild, joined_user_ids)
            
            embed = Embed('Cancelled', 'The game has been cancelled, the hearts are refund.', color=GAMBLING_COLOR)
            try:
                await client.message_edit(message, embed=embed)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        joined_tuples = join_gui.joined_tuples
        if len(joined_tuples) == 1:
            await game_21_refund(joined_tuples[0][2], amount)
            
            embed = Embed('RIP', 'Starting the game alone, is just sad.', color=GAMBLING_COLOR)
            
            try:
                await client.message_edit(message, embed=embed)
            except BaseException as err:
                if should_render_exception(err):
                    await client.events.error(client, 'game_21_multi_player', err)
            return
        
        total_bet_amount = len(joined_tuples)*amount
        # Update message
        description_parts = ['Total bet amount: ', str(total_bet_amount), EMOJI__HEART_CURRENCY.as_emoji,
            '\n\nPlayers:\n',]
        
        for tuple_user, tuple_channel, entry_id in joined_tuples:
            description_parts.append(tuple_user.mention)
            description_parts.append('\n')
        
        del description_parts[-1]
        
        description = ''.join(description_parts)
        embed = Embed('Game 21 in progress', description, color=GAMBLING_COLOR)
        try:
            await client.message_edit(message, embed=embed)
        except BaseException as err:
            game_21_mp_notify_cancellation(client, joined_tuples, amount, channel, guild, joined_user_ids)
            if should_render_exception(err):
                await client.events.error(client, 'game_21_multi_player', err)
            return
        
        # Start game
        base = Game21Base(guild)
        tasks = []
        for tuple_user, tuple_channel, entry_id in joined_tuples:
            task = Task(Game21PlayerRunner(client, base, tuple_user, tuple_channel, amount, True), KOKORO)
            tasks.append(task)
        
        done, pending = await WaitTillAll(tasks, KOKORO)
        
        waiters_to_runners = {}
        
        for task in done:
            runner = await task
            waiter = runner.waiter
            waiters_to_runners[waiter] = runner
        
        done, pending = await WaitTillAll(waiters_to_runners, KOKORO)
        
        max_point = 0
        losers = []
        winners = []
        for waiter in done:
            game_state = waiter.result()
            runner = waiters_to_runners[waiter]
            if game_state != GAME_21_RESULT_FINISH:
                losers.append(user)
                continue
            
            user_total = runner.player.total
            user = runner.player.user
            if user_total > 21:
                losers.append(user)
                continue
            
            if user_total > max_point:
                losers.extend(winners)
                winners.clear()
                winners.append(user)
                max_point = user_total
                continue
            
            if user_total == max_point:
                winners.append(user)
                continue
            
            losers.append(user)
            continue
        
        user_entry_map = {}
        for tuple_user, tuple_channel, entry_id in joined_tuples:
            user_entry_map[tuple_user] = entry_id
        
        loser_entry_ids = None
        if losers:
            for user in losers:
                entry_id = user_entry_map[user]
                if entry_id == -1:
                    continue
                
                if loser_entry_ids is None:
                    loser_entry_ids = []
                loser_entry_ids.append(entry_id)
        
        winner_entry_ids = None
        if winners:
            for user in winners:
                entry_id = user_entry_map[user]
                if entry_id == -1:
                    continue
                
                if winner_entry_ids is None:
                    winner_entry_ids = []
                winner_entry_ids.append(entry_id)
        
        async with DB_ENGINE.connect() as connector:
            if (loser_entry_ids is not None):
                await connector.execute(CURRENCY_TABLE. \
                    update(currency_model.id.in_(loser_entry_ids)). \
                    values(
                        total_allocated = currency_model.total_allocated-amount,
                        total_love = currency_model.total_love-amount,
                    )
                )
                
                if (winner_entry_ids is not None):
                    won_per_user = int(len(losers)*amount//len(winners))
                    
                    await connector.execute(CURRENCY_TABLE. \
                        update(currency_model.id.in_(winner_entry_ids)). \
                        values(
                            total_allocated = currency_model.total_allocated-amount,
                            total_love = currency_model.total_love+won_per_user,
                        )
                    )
                
            else:
                if (winner_entry_ids is not None):
                    await connector.execute(CURRENCY_TABLE. \
                        update(currency_model.id.in_(winner_entry_ids)). \
                        values(
                            total_allocated = currency_model.total_allocated-amount,
                        )
                    )
        
        description_parts = ['Total bet amount: ', str(total_bet_amount), EMOJI__HEART_CURRENCY.as_emoji, '\n\n']
        
        if winners:
            description_parts.append('Winners:\n')
            for user in winners:
                description_parts.append(user.mention)
                description_parts.append('\n')
            
            description_parts.append('\n')
        
        if losers:
            description_parts.append('Losers:\n')
            for user in losers:
                description_parts.append(user.mention)
                description_parts.append('\n')
        
        if description_parts[-1] == '\n':
            del description_parts[-1]
        
        description = ''.join(description_parts)
        
        embed = Embed('Game ended', description, color=GAMBLING_COLOR)
        for runner in waiters_to_runners.values():
            runner.player.add_done_embed_field(embed)
        
        try:
            await client.message_edit(message, embed=embed)
        except BaseException as err:
            if should_render_exception(err):
                await client.events.error(client, 'game_21_multi_player', err)
        return
    
    finally:
        for user_id in joined_user_ids:
            IN_GAME_IDS.discard(user_id)


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
            select([currency_model.id, currency_model.total_love, currency_model.total_allocated]). \
            where(currency_model.user_id==source_user.id)
        )
        
        results = await response.fetchall()
        if results:
            source_user_entry_id, source_user_total_love, source_user_total_allocated = results[0]
        else:
            source_user_entry_id = -1
            source_user_total_love = 0
            source_user_total_allocated = 0
        
        if source_user_total_love == 0:
            yield Embed('So lonely...', 'You do not have any hearts to gift.', color=GAMBLING_COLOR)
            return
        
        if source_user_total_love == source_user_total_allocated:
            yield Embed('Like a flower', 'Whithering to the dust.', color=GAMBLING_COLOR)
            return
        
        response = await connector.execute(
            select([currency_model.id, currency_model.total_love]). \
            where(currency_model.user_id==target_user.id)
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
        
        await connector.execute(CURRENCY_TABLE. \
            update(currency_model.id==source_user_entry_id). \
            values(total_love = currency_model.total_love-amount)
        )
        
        if target_user_entry_id != -1:
            to_execute = CURRENCY_TABLE. \
                update(currency_model.id==target_user_entry_id). \
                values(total_love = currency_model.total_love+amount)
        
        else:
            to_execute = CURRENCY_TABLE.insert().values(
                user_id         = target_user.id,
                total_love      = target_user_new_total_love,
                daily_next      = datetime.utcnow(),
                daily_streak    = 0,
                total_allocated = 0,
            )
        
        await connector.execute(to_execute)
        
    embed = Embed('Aww, so lovely',
        f'You gifted {amount} {EMOJI__HEART_CURRENCY.as_emoji} to {target_user.full_name}',
        color=GAMBLING_COLOR,
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
        color=GAMBLING_COLOR,
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
        yield Embed('BAKA !!', 'You cannot award non-positive amount of hearts..', color=GAMBLING_COLOR)
        return
    
    if (message is not None) and len(message) > 1000:
        message = message[:1000]+'...'
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([currency_model.id, currency_model.total_love, currency_model.daily_streak,
                currency_model.daily_next]). \
            where(currency_model.user_id==target_user.id)
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
            to_execute = CURRENCY_TABLE. \
                update(currency_model.id == target_user_entry_id). \
                values(
                    total_love  = target_user_new_total_love,
                    daily_streak = target_user_new_daily_streak,
                    daily_next = target_user_new_daily_next,
                )
        else:
            to_execute = CURRENCY_TABLE.insert().values(
                user_id         = target_user.id,
                total_love      = target_user_new_total_love,
                daily_next      = target_user_new_daily_next,
                daily_streak    = target_user_new_daily_streak,
                total_allocated = 0,
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
    
    embed = Embed(f'You awarded {target_user.full_name} with {amount} {awarded_with}',
        f'Now they are up from {up_from} to {up_to} {awarded_with}',
        color=GAMBLING_COLOR)
    
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
        color=GAMBLING_COLOR,
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
            select([currency_model.id, currency_model.total_love, currency_model.total_allocated]). \
                where(currency_model.user_id==target_user.id)
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
                
                await connector.execute(CURRENCY_TABLE. \
                    update(currency_model.id==target_user_entry_id). \
                    values(
                        total_love = target_user_new_total_love,
                    )
                )
        else:
            target_user_total_love = 0
            target_user_new_total_love = 0
    
    yield Embed(f'You took {amount} {EMOJI__HEART_CURRENCY.as_emoji} away from {target_user.full_name}',
        f'They got down from {target_user_total_love} to {target_user_new_total_love} {EMOJI__HEART_CURRENCY.as_emoji}',
        color=GAMBLING_COLOR)
    
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
            select([currency_model.id, currency_model.user_id, currency_model.total_love]). \
            where(currency_model.user_id.in_([source_user.id, target_user.id]))
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
                CURRENCY_TABLE.delete(). \
                where(currency_model.id==source_user_entry_id)
            )
        
        if source_user_total_love:
            if target_user_found:
                to_execute = CURRENCY_TABLE. \
                    update(currency_model.id == target_user_entry_id). \
                    values(
                        total_love = currency_model.total_love+source_user_total_love,
                    )
            else:
                to_execute = CURRENCY_TABLE.insert(). \
                values(
                    user_id         = user_id,
                    total_love      = source_user_total_love,
                    daily_next      = datetime.utcnow(),
                    daily_streak    = 0,
                    total_allocated = 0,
                )
            
            await connector.execute(to_execute)
    
    embed = Embed(
        f'You transferred {source_user.full_name}\'s hearts to {target_user.full_name}',
        color=GAMBLING_COLOR,
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
        color=GAMBLING_COLOR,
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
            select([currency_model.id]). \
            where(currency_model.user_id == user_id)
        )
        
        results = await response.fetchall()
        if results:
            entry_id = results[0][0]
            entry_found = True
        else:
            entry_id = 0
            entry_found = False
        
        if entry_found:
            to_execute = CURRENCY_TABLE. \
                update(currency_model.id == entry_id). \
                values(
                    total_love      = hearts,
                    daily_next      = datetime.utcnow(),
                    daily_streak    = dailies,
                    total_allocated = 0,
                )
        else:
            to_execute = CURRENCY_TABLE.insert(). \
                values(
                    user_id         = user_id,
                    total_love      = hearts,
                    daily_next      = datetime.utcnow(),
                    daily_streak    = dailies,
                    total_allocated = 0,
                )
        
        await connector.execute(to_execute)
    
    yield Embed(
        'Inserting into currency table',
        color=GAMBLING_COLOR,
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
            select([currency_model.user_id, currency_model.total_love])
                .where(currency_model.total_love != 0)
                .order_by(desc(currency_model.total_love))
                .limit(20)
                .offset(20*(page-1))
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
        index_adjust = floor(log((page-1)*20+len(parts), 10.0))+1
        hearts_adjust = floor(log(max_hearts, 10.0))+1
        
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


HEART_SHOP = SLASH_CLIENT.interactions(None,
    name = 'heart-shop',
    description = 'Trade your love!',
    is_global = True,
)


ELEVATED_IDENTIFIER = '1'
HEART_BOOST_IDENTIFIER = '2'

BUYABLE_ROLES = {
    ELEVATED_IDENTIFIER: (ROLE__NEKO_DUNGEON__ELEVATED, ELEVATED_COST),
    HEART_BOOST_IDENTIFIER: (ROLE__NEKO_DUNGEON__HEART_BOOST, HEART_BOOST_COST),
}

ROLE_CHOICES = [
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
            select([currency_model.total_love, currency_model.total_allocated]). \
            where(currency_model.user_id==user_id)
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
            
            await connector.execute(CURRENCY_TABLE. \
                update(currency_model.user_id == user_id). \
                values(
                    total_love = currency_model.total_love-cost,
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
            select([currency_model.id, currency_model.total_love, currency_model.daily_streak, currency_model.daily_next]). \
            where(currency_model.user_id==user_id)
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
            
            await connector.execute(CURRENCY_TABLE. \
                update(currency_model.id == entry_id). \
                values(
                    total_love = currency_model.total_love+sell_price,
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
        response = await connector.execute(select([currency_model.id]).where(currency_model.user_id==user_id))
        results = await response.fetchall()
        if results:
            entry_id = results[0][0]
            to_execute = CURRENCY_TABLE. \
                update(currency_model.id == entry_id). \
                values(
                    total_love = currency_model.total_love+increase,
                )
        else:
            to_execute = CURRENCY_TABLE.insert().values(
                user_id         = user_id,
                total_love      = increase,
                daily_next      = datetime.utcnow(),
                daily_streak    = 0,
                total_allocated = 0,
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
        
