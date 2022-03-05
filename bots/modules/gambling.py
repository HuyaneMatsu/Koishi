from functools import partial as partial_func
from datetime import datetime, timedelta
from random import random
from math import log10, floor

from scarletio import Task, Future
from hata import Client, elapsed_time, Embed, BUILTIN_EMOJIS, DiscordException, KOKORO, \
    ERROR_CODES, USERS, ZEROUSER, parse_tdelta, Permission, InteractionType
from hata.ext.slash import abort, set_permission, Button, Row, wait_for_component_interaction
from sqlalchemy.sql import select, desc

from bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE, get_create_common_user_expression

from bot_utils.constants import ROLE__SUPPORT__ELEVATED, ROLE__SUPPORT__BOOSTER, GUILD__SUPPORT, \
    EMOJI__HEART_CURRENCY, ROLE__SUPPORT__ADMIN, COLOR__GAMBLING, LINK__KOISHI_TOP_GG
from bot_utils.utils import send_embed_to
from bot_utils.daily import DAILY_INTERVAL, calculate_daily_new_only, calculate_daily_new, DAILY_STREAK_BREAK, \
    calculate_daily_for, TOP_GG_VOTE_DELAY_MIN, TOP_GG_VOTE_DELAY_MAX

SLASH_CLIENT: Client


EVENT_MAX_DURATION = timedelta(hours=24)
EVENT_MIN_DURATION = timedelta(minutes=30)
EVENT_HEART_MIN_AMOUNT = 50
EVENT_HEART_MAX_AMOUNT = 3000
EVENT_OK_EMOJI = BUILTIN_EMOJIS['ok_hand']
EVENT_ABORT_EMOJI = BUILTIN_EMOJIS['x']
EVENT_DAILY_MIN_AMOUNT = 1
EVENT_DAILY_MAX_AMOUNT = 7
EVENT_OK_BUTTON = Button(emoji=EVENT_OK_EMOJI)
EVENT_ABORT_BUTTON = Button(emoji=EVENT_ABORT_EMOJI)
EVENT_COMPONENTS = Row(EVENT_OK_BUTTON, EVENT_ABORT_BUTTON)
EVENT_CURRENCY_BUTTON = Button(emoji=EMOJI__HEART_CURRENCY)


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
        
        now = datetime.utcnow()
        
        results = await response.fetchall()
        if results:
            entry_id, total_love, daily_streak, daily_next, count_top_gg_vote, top_gg_last_vote = results[0]
            
            if daily_next > now:
                return Embed(
                    'You already claimed your daily love for today~',
                    f'Come back in {elapsed_time(daily_next)}.',
                    color = COLOR__GAMBLING,
                )
            
            daily_streak = calculate_daily_new_only(daily_streak, daily_next, now)
            
            if daily_next + DAILY_STREAK_BREAK < now:
                streak_text = f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
            else:
                streak_text = f'You are in a {daily_streak + 1} day streak! Keep up the good work!'
            
            received = calculate_daily_for(user, daily_streak)
            total_love = total_love + received
            
            daily_streak += 1
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == entry_id,
                ).values(
                    total_love = total_love,
                    daily_next = now + DAILY_INTERVAL,
                    daily_streak = daily_streak,
                    count_daily_self = user_common_model.count_daily_self + 1,
                )
            )
            
            if (
                (count_top_gg_vote > 0) and
                (now - TOP_GG_VOTE_DELAY_MIN > top_gg_last_vote) and
                (now - TOP_GG_VOTE_DELAY_MAX < top_gg_last_vote)
            ):
                voted = await client.top_gg.get_user_vote(user.id)
                if not voted:
                    streak_text = (
                        f'{streak_text}\n'
                        f'\n'
                        f'Please vote for me on [top.gg]({LINK__KOISHI_TOP_GG}) for extra {EMOJI__HEART_CURRENCY}'
                    )
            
            return Embed(
                'Here, some love for you~\nCome back tomorrow !',
                (
                    f'You received {received} {EMOJI__HEART_CURRENCY:e} and now have {total_love} '
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
                    f'{target_user.name} already claimed your daily love for today~',
                    f'Come back in {elapsed_time(target_daily_next)}.',
                    color = COLOR__GAMBLING,
                )
            
            target_daily_streak = target_entry[4]
            target_daily_streak = calculate_daily_new_only(target_daily_streak, target_daily_next, now)
            
            if target_daily_next + DAILY_STREAK_BREAK < now:
                streak_text = f'They did not claim daily for more than 1 day, they got down to {target_daily_streak}.'
            else:
                streak_text = f'They are in a {target_daily_streak + 1} day streak! Keep up the good work for them!'
            
            received = calculate_daily_for(target_user, target_daily_streak)
            
            target_total_love = target_entry[3]
            target_total_love = target_total_love + received
            
            target_daily_streak += 1
            
            waifu_cost_increase = 1 + floor(received * 0.01)
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == source_entry[0],
                ).values(
                    waifu_cost = user_common_model.waifu_cost + waifu_cost_increase,
                    count_daily_for_waifu = user_common_model.count_daily_for_waifu + 1,
                )
            )
            
            await connector.execute(
                USER_COMMON_TABLE.update(
                    user_common_model.id == target_entry[0],
                ).values(
                    total_love = target_total_love,
                    daily_next = now + DAILY_INTERVAL,
                    daily_streak = target_daily_streak,
                    waifu_cost = user_common_model.waifu_cost + waifu_cost_increase,
                    count_daily_by_waifu = user_common_model.count_daily_by_waifu + 1,
                )
            )
            
            await client.interaction_followup_message_create(
                event,
                embed = Embed(
                    'How sweet, you claimed my love for your chosen one !',
                    (
                        f'{target_user.name} received {received} {EMOJI__HEART_CURRENCY:e} and they have '
                        f'{target_total_love} {EMOJI__HEART_CURRENCY:e}\n'
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
                            f'You received {received} {EMOJI__HEART_CURRENCY} and now you have '
                            f'{target_total_love} {EMOJI__HEART_CURRENCY}\n'
                            f'You are on a {target_daily_streak} day streak.'
                        ),
                        color = COLOR__GAMBLING,
                    ),
                    Button(
                        'I don\'t want notifs, nya!!',
                        custom_id = 'accessibility.change_notification_settings.daily.disable',
                    ),
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
    yield
    
    if target_user is None:
        coroutine = claim_daily_for_yourself(client, event)
    else:
        coroutine = claim_daily_for_waifu(client, event, target_user)
    
    yield await coroutine


def convert_tdelta(delta):
    result = []
    rest = delta.days
    if rest:
        result.append(f'{rest} days')
    rest = delta.seconds
    amount = rest // 3600
    if amount:
        result.append(f'{amount} hours')
        rest %= 3600
    amount = rest // 60
    if amount:
        result.append(f'{amount} minutes')
        rest %= 60
    if rest:
        result.append(f'{rest} seconds')
    return ', '.join(result)


def heart_event_start_checker(client, event):
    if event.user.has_role(ROLE__SUPPORT__ADMIN):
        return True
    
    return True


PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)


@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__ADMIN, True)
async def heart_event(client, event,
    duration : ('str', 'The event\'s duration.'),
    amount : ('int', 'The hearst to earn.'),
    user_limit : ('int', 'The maximal amount fo claimers.') = 0,
):
    """Starts a heart event at the channel."""
    while True:
        if not event.user.has_role(ROLE__SUPPORT__ADMIN):
            response = f'{ROLE__SUPPORT__ADMIN.mention} only!'
            error = True
            break
        
        permissions = event.channel.cached_permissions_for(client)
        if not permissions & PERMISSION_MASK_MESSAGING:
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
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit - len(self.user_ids)} users'
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
            to_execute = USER_COMMON_TABLE.update(
                user_common_model.id == entry_id,
            ).values(
                total_love=user_common_model.total_love + self.amount,
            )
        
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
        
        sleep_time = (self.duration % update_delta).seconds
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


@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__ADMIN, True)
async def daily_event(client, event,
    duration: ('str', 'The event\'s duration.'),
    amount: ('int', 'The extra daily steaks to earn.'),
    user_limit: ('int', 'The maximal amount fo claimers.') = 0,
):
    """Starts a heart event at the channel. (Bot owner only)"""
    while True:
        if not event.user.has_role(ROLE__SUPPORT__ADMIN):
            response = f'{ROLE__SUPPORT__ADMIN.mention} only!'
            error = True
            break
        
        permissions = event.channel.cached_permissions_for(client)
        if not permissions & PERMISSION_MASK_MESSAGING:
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
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit - len(self.user_ids)} users'
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
            daily_streak = daily_streak + self.amount
            
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
        
        sleep_time = (self.duration % update_delta).seconds
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



@SLASH_CLIENT.interactions(is_global=True)
async def gift(client, event,
    target_user: ('user', 'Who is your heart\'s chosen one?'),
    amount: ('int', 'How much do u love them?'),
    message: ('str', 'Optional message to send with the gift.') = None,
):
    """Gifts hearts to the chosen by your heart."""
    source_user = event.user
    
    if not (source_user.has_role(ROLE__SUPPORT__ELEVATED) or source_user.has_role(ROLE__SUPPORT__BOOSTER)):
        abort(f'You must have either {ROLE__SUPPORT__ELEVATED.name} or '
            f'{ROLE__SUPPORT__BOOSTER.name} role to invoke this command.', allowed_mentions=None)
    
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
            amount = source_user_total_love - source_user_total_allocated
            source_user_new_love = source_user_total_allocated
        else:
            source_user_new_love = source_user_total_love - amount
        
        target_user_new_total_love = target_user_total_love + amount
        
        await connector.execute(
            USER_COMMON_TABLE.update(
                user_common_model.id == source_user_entry_id
            ).values(
                total_love = user_common_model.total_love - amount,
            )
        )
        
        if target_user_entry_id != -1:
            to_execute = USER_COMMON_TABLE.update(
                user_common_model.id == target_user_entry_id
            ).values(
                total_love = user_common_model.total_love + amount,
            )
        
        else:
            to_execute = get_create_common_user_expression(
                target_user.id,
                total_love = target_user_new_total_love,
            )
        
        await connector.execute(to_execute)
        
    embed = Embed(
        'Aww, so lovely',
        f'You gifted {amount} {EMOJI__HEART_CURRENCY} to {target_user.full_name}',
        color = COLOR__GAMBLING,
    ).add_field(
        f'Your {EMOJI__HEART_CURRENCY}',
        f'{source_user_total_love} -> {source_user_new_love}',
    ).add_field(
        f'Their {EMOJI__HEART_CURRENCY}',
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
        f'You have been gifted {amount} {EMOJI__HEART_CURRENCY} by {source_user.full_name}',
        color = COLOR__GAMBLING,
    ).add_field(
        f'Your {EMOJI__HEART_CURRENCY}',
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

@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__ADMIN, True)
async def award(client, event,
    target_user: ('user', 'Who do you want to award?'),
    amount: ('int', 'With how much love do you wanna award them?'),
    message : ('str', 'Optional message to send with the gift.') = None,
    with_: (AWARD_TYPES, 'Select award type') = 'hearts',
):
    """Awards the user with love."""
    if not event.user.has_role(ROLE__SUPPORT__ADMIN):
        abort(f'{ROLE__SUPPORT__ADMIN.mention} only!', allowed_mentions=None)
    
    if amount <= 0:
        yield Embed(
            'BAKA !!',
            'You cannot award non-positive amount of hearts..',
            color = COLOR__GAMBLING,
        )
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
            target_user_new_total_love = target_user_total_love + amount
            target_user_new_daily_streak = target_user_daily_streak
        else:
            now = datetime.utcnow()
            target_user_new_total_love = target_user_total_love
            if target_user_daily_next < now:
                target_user_daily_streak, target_user_daily_next = calculate_daily_new(
                    target_user_daily_streak, 
                    target_user_daily_next,
                    now
                )
            
            target_user_new_daily_streak = target_user_daily_streak + amount
        
        target_user_new_daily_next = target_user_daily_next
            
        if (target_user_entry_id != -1):
            to_execute = USER_COMMON_TABLE.update(
                user_common_model.id == target_user_entry_id,
            ).values(
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


@SLASH_CLIENT.interactions(guild=GUILD__SUPPORT, allow_by_default=False)
@set_permission(GUILD__SUPPORT, ROLE__SUPPORT__ADMIN, True)
async def take(client, event,
    target_user: ('user', 'From who do you want to take love away?'),
    amount: ('int', 'How much love do you want to take away?'),
):
    """Takes away hearts form the lucky user."""
    if not event.user.has_role(ROLE__SUPPORT__ADMIN):
        abort(f'{ROLE__SUPPORT__ADMIN.mention} only!', allowed_mentions=None)
    
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
            target_user_heart_reducible = target_user_total_love - target_user_total_allocated
            if target_user_heart_reducible <= 0:
                target_user_new_total_love = 0
            else:
                target_user_new_total_love = target_user_heart_reducible - amount
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
        f'You took {amount} {EMOJI__HEART_CURRENCY} away from {target_user.full_name}',
        f'They got down from {target_user_total_love} to {target_user_new_total_love} {EMOJI__HEART_CURRENCY}',
        color = COLOR__GAMBLING,
    )
    
    return


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
                20 * (page - 1),
            )
        )
        
        results = await response.fetchall()
        
        parts = []
        max_hearts = 0
        
        for index, (user_id, total_hearts) in enumerate(results, (page * 20) - 19):
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
        index_adjust = floor(log10((page - 1) * 20 + len(parts))) + 1
        hearts_adjust = floor(log10(max_hearts)) + 1
        
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





HEART_GENERATOR_COOLDOWNS = set()
HEART_GENERATOR_COOLDOWN = 3600.0
HEART_GENERATION_AMOUNT = 10

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component
INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE = InteractionType.application_command_autocomplete

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
            to_execute = USER_COMMON_TABLE.update(
                user_common_model.id == entry_id
            ).values(
                total_love = user_common_model.total_love + increase,
            )
        else:
            to_execute = get_create_common_user_expression(
                user_id,
                total_love = increase,
            )
        
        await connector.execute(to_execute)

# yup, we are generating hearts
@SLASH_CLIENT.events(name='interaction_create')
async def heart_generator(client, event):
    user_id = event.user.id
    if user_id in HEART_GENERATOR_COOLDOWNS:
        return
    
    event_type = event.type
    if event_type is INTERACTION_TYPE_APPLICATION_COMMAND:
        chance = 0.05
    elif event_type is INTERACTION_TYPE_MESSAGE_COMPONENT:
        chance = 0.01
    elif event_type is INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE:
        chance = 0.005
    else:
        return
    
    if random() < chance:
        KOKORO.call_later(HEART_GENERATOR_COOLDOWN, set.discard, HEART_GENERATOR_COOLDOWNS, user_id)
        await increase_user_total_love(user_id, HEART_GENERATION_AMOUNT)
