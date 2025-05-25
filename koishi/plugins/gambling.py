__all__ = ()

from datetime import datetime as DateTime, timedelta as TimeDelta, timezone as TimeZone
from functools import partial as partial_func
from random import random

from hata import (
    BUILTIN_EMOJIS, DiscordException, ERROR_CODES, Embed, InteractionType, KOKORO, Permission, create_button,
    create_row, parse_tdelta
)
from hata.ext.slash import abort, wait_for_component_interaction
from scarletio import CancelledError, Future, Task

from ..bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY, GUILD__SUPPORT, ROLE__SUPPORT__ADMIN
from ..bot_utils.daily import calculate_daily_new
from ..bot_utils.utils import send_embed_to
from ..bots import FEATURE_CLIENTS

from .user_balance import get_user_balance
from .user_settings import get_one_user_settings, get_preferred_client_for_user


EVENT_MAX_DURATION = TimeDelta(hours = 24)
EVENT_MIN_DURATION = TimeDelta(minutes = 30)
EVENT_HEART_MIN_AMOUNT = 50
EVENT_HEART_MAX_AMOUNT = 3000
EVENT_OK_EMOJI = BUILTIN_EMOJIS['ok_hand']
EVENT_ABORT_EMOJI = BUILTIN_EMOJIS['x']
EVENT_DAILY_MIN_AMOUNT = 1
EVENT_DAILY_MAX_AMOUNT = 7
EVENT_OK_BUTTON = create_button(emoji = EVENT_OK_EMOJI)
EVENT_ABORT_BUTTON = create_button(emoji = EVENT_ABORT_EMOJI)
EVENT_COMPONENTS = create_row(EVENT_OK_BUTTON, EVENT_ABORT_BUTTON)
EVENT_CURRENCY_BUTTON = create_button(emoji = EMOJI__HEART_CURRENCY)


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



@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def heart_event(
    client,
    event,
    duration : ('str', 'The event\'s duration.'),
    amount : ('int', 'The hearst to earn.'),
    user_limit : ('int', 'The maximal amount fo claimers.') = 0,
):
    """Starts a heart event at the channel."""
    while True:
        if not event.user_permissions.administrator:
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
        await client.interaction_response_message_create(event, response, show_for_invoking_user_only = True)
        return
    
    await client.interaction_application_command_acknowledge(event)
    message = await client.interaction_followup_message_create(event, response, components = EVENT_COMPONENTS)
    
    try:
        component_event = await wait_for_component_interaction(message,
            check = partial_func(heart_event_start_checker, client), timeout = 300.)
    except TimeoutError:
        try:
            await client.interaction_response_message_edit(event, 'Heart event cancelled, timeout.',
                components = None)
        except ConnectionError:
            pass
        return
    
    if component_event.interaction == EVENT_ABORT_BUTTON:
        try:
            await client.interaction_component_message_edit(component_event, 'Heart event cancelled.',
                components = None)
        except ConnectionError:
            pass
        return
    
    await client.interaction_component_acknowledge(component_event)
    await HeartEventGUI(client, event, duration, amount, user_limit)


class HeartEventGUI:
    _update_time = 60.0
    _update_delta = TimeDelta(seconds = _update_time)
    
    __slots__ = ('amount', 'client', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    
    async def __new__(cls, client, event, duration, amount, user_limit):
        self = object.__new__(cls)
        self.user_ids = set()
        self.user_limit = user_limit
        self.client = client
        self.duration = duration
        self.amount = amount
        self.waiter = Future(KOKORO)
        
        message = event.message
        self.message = message
        
        try:
            await client.interaction_response_message_edit(
                event, content = '', embed = self.generate_embed(), components = EVENT_CURRENCY_BUTTON
            )
        except ConnectionError:
            return
        
        client.slasher.add_component_interaction_waiter(message, self)
        Task(KOKORO, self.countdown(client, message))
        return
    
    def generate_embed(self):
        title = f'Click on {EMOJI__HEART_CURRENCY} to receive {self.amount}'
        if self.user_limit:
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit - len(self.user_ids)} users'
        else:
            description = f'{convert_tdelta(self.duration)} left'
        return Embed(title, description, color = COLOR__GAMBLING)

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
            self.duration = TimeDelta()
            self.waiter.set_result(None)
        
        user_balance = await get_user_balance(user.id)
        user_balance.set('balance', user_balance.balance + self.amount)
        await user_balance.save()
        
        await self.client.interaction_component_acknowledge(event)
    
    
    async def countdown(self, client, message):
        update_delta = self._update_delta
        waiter = self.waiter
        
        sleep_time = (self.duration % update_delta).seconds
        if sleep_time:
            self.duration -= TimeDelta(seconds = sleep_time)
            KOKORO.call_after(sleep_time, type(waiter).set_result_if_pending, waiter, None)
            await waiter
            self.waiter = waiter = Future(KOKORO)
        
        sleep_time = self._update_time
        while True:
            KOKORO.call_after(sleep_time, type(waiter).set_result_if_pending, waiter, None)
            await waiter
            self.waiter = waiter = Future(KOKORO)
            self.duration -= update_delta
            if self.duration < update_delta:
                break
            try:
                await client.message_edit(message, embed = self.generate_embed())
            except GeneratorExit:
                raise
            
            except CancelledError:
                raise
            
            except ConnectionError:
                break
            
            except BaseException as err:
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
        except GeneratorExit:
            raise
        
        except CancelledError:
            raise
        
        except ConnectionError:
            return
        
        except BaseException as err:
            if isinstance(err, DiscordException):
                if err.code in (
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.missing_access, # client removed
                ):
                    return
            
            await client.events.error(client, f'{self!r}.countdown', err)
            return


@FEATURE_CLIENTS.interactions(
    guild = GUILD__SUPPORT,
    required_permissions = Permission().update_by_keys(administrator = True),
)
async def daily_event(
    client,
    event,
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
        await client.interaction_response_message_create(event, response, show_for_invoking_user_only = True)
        return
    
    await client.interaction_application_command_acknowledge(event)
    message = await client.interaction_followup_message_create(event, response, components = EVENT_COMPONENTS)
    
    try:
        component_event = await wait_for_component_interaction(message,
            check = partial_func(heart_event_start_checker, client), timeout = 300.0)
    except TimeoutError:
        try:
            await client.interaction_response_message_edit(event, message, 'Daily event cancelled, timeout.',
                components = None)
        except ConnectionError:
            pass
        return
    
    if component_event.interaction == EVENT_ABORT_BUTTON:
        try:
            await client.interaction_component_message_edit(component_event, 'Daily event cancelled.',
                components = None)
        except ConnectionError:
            pass
        return
    
    await client.interaction_component_acknowledge(component_event)
    await DailyEventGUI(client, event, duration, amount, user_limit)


class DailyEventGUI:
    _update_time = 60.0
    _update_delta = TimeDelta(seconds = _update_time)
    
    __slots__ = ('amount', 'client', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    
    async def __new__(cls, client, event, duration, amount, user_limit):
        self = object.__new__(cls)
        self.user_ids = set()
        self.user_limit = user_limit
        self.client = client
        self.duration = duration
        self.amount = amount
        self.waiter = Future(KOKORO)
        
        message = event.message
        self.message = message
        
        try:
            await client.interaction_response_message_edit(
                event, content = '', embed = self.generate_embed(), components = EVENT_CURRENCY_BUTTON
            )
        except ConnectionError:
            return
        
        client.slasher.add_component_interaction_waiter(message, self)
        Task(KOKORO, self.countdown(client, message))
        return
    
    def generate_embed(self):
        title = f'React with {EMOJI__HEART_CURRENCY} to increase your streak by {self.amount}'
        if self.user_limit:
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit - len(self.user_ids)} users'
        else:
            description = f'{convert_tdelta(self.duration)} left'
        return Embed(title, description, color = COLOR__GAMBLING)
    
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
            self.duration = TimeDelta()
            self.waiter.set_result(None)
        
        
        user_balance = await get_user_balance(user.id)
        streak, daily_can_claim_at = calculate_daily_new(
            user_balance.streak, user_balance.daily_can_claim_at.replace, DateTime.now(TimeZone.utc)
        )
        user_balance.set('streak', streak + self.amount)
        user_balance.set('daily_can_claim_at', daily_can_claim_at)
        await user_balance.save()
        
        await self.client.interaction_component_acknowledge(event)
    
    
    async def countdown(self, client, message):
        update_delta = self._update_delta
        waiter = self.waiter
        
        sleep_time = (self.duration % update_delta).seconds
        if sleep_time:
            self.duration -= TimeDelta(seconds = sleep_time)
            KOKORO.call_after(sleep_time, type(waiter).set_result_if_pending, waiter, None)
            await waiter
            self.waiter = waiter = Future(KOKORO)
        
        sleep_time = self._update_time
        while True:
            KOKORO.call_after(sleep_time, type(waiter).set_result_if_pending, waiter, None)
            await waiter
            self.waiter = waiter = Future(KOKORO)
            self.duration -= update_delta
            if self.duration < update_delta:
                break
            
            try:
                await client.message_edit(message, embed = self.generate_embed())
            except GeneratorExit:
                raise
            
            except CancelledError:
                raise
            
            except BaseException as err:
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
        except GeneratorExit:
            raise
        
        except CancelledError:
            raise
        
        except ConnectionError:
            return
        
        except BaseException as err:
            if isinstance(err, DiscordException):
                if err.code in (
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.missing_access, # client removed
                ):
                    return
            
            await client.events.error(client, f'{self!r}.countdown', err)
            return


AWARD_TYPES = [
    ('hearts', 'hearts'),
    ('streak', 'streak')
]


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT, required_permissions = Permission().update_by_keys(administrator = True))
async def award(
    client,
    event,
    target_user: ('user', 'Who do you want to award?'),
    amount: ('int', 'With how much hearts do you wanna award them?'),
    message : ('str', 'Optional message to send with the gift.') = None,
    with_: (AWARD_TYPES, 'Select award type') = 'hearts',
):
    """Awards the user with balance or streak."""
    if not event.user_permissions.administrator:
        abort(f'You must have administrator permission to invoke this command.')
    
    if amount <= 0:
        yield Embed(
            'BAKA !!',
            'You cannot award non-positive amount of hearts..',
            color = COLOR__GAMBLING,
        )
        return
    
    if (message is not None) and len(message) > 1000:
        message = message[ : 1000] + '...'
    
    target_user_balance = await get_user_balance(target_user.id)
    target_balance = target_user_balance.balance
    target_streak = target_user_balance.streak
    target_daily_can_claim_at = target_user_balance.daily_can_claim_at
    
    if with_ == 'hearts':
        target_new_balance = target_balance + amount
        target_new_streak = target_streak
    else:
        now = DateTime.now(TimeZone.utc)
        target_new_balance = target_user_balance.balance
        target_new_streak, target_daily_can_claim_at = calculate_daily_new(
            target_streak, 
            target_daily_can_claim_at,
            now,
        )
        
        target_new_streak = target_streak + amount
    
    target_user_balance.set('balance', target_new_balance)
    target_user_balance.set('streak', target_new_streak)
    target_user_balance.set('daily_can_claim_at', target_daily_can_claim_at)
    await target_user_balance.save()
    
    if with_ == 'hearts':
        awarded_with = EMOJI__HEART_CURRENCY.as_emoji
        up_from = target_balance
        up_to = target_new_balance
    else:
        awarded_with = 'streak(s)'
        up_from = target_streak
        up_to = target_new_streak
    
    embed = Embed(
        f'You awarded {target_user.name_at(event.guild_id)} with {amount} {awarded_with}',
        f'Now they are up from {up_from} to {up_to} {awarded_with}',
        color = COLOR__GAMBLING,
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    yield embed
    
    if target_user.bot:
        return
    
    embed = Embed(
        'Aww, love is in the air',
        f'You have been awarded {amount} {awarded_with} by {event.user.name_at(event.guild_id)}',
        color = COLOR__GAMBLING,
    ).add_field(
        f'Your {awarded_with}',
        f'{up_from} -> {up_to}',
    )
    
    if (message is not None):
        embed.add_field('Message:', message)
    
    target_user_settings = await get_one_user_settings(target_user.id)
    
    await send_embed_to(
        get_preferred_client_for_user(target_user, target_user_settings.preferred_client_id, client),
        target_user.id,
        embed,
        None,
    )


@FEATURE_CLIENTS.interactions(guild = GUILD__SUPPORT, required_permissions = Permission().update_by_keys(administrator = True))
async def take(
    client,
    event,
    target_user: ('user', 'From who do you want to take hearts away?'),
    amount: ('int', 'How much hearts do you want to take away?'),
):
    """Takes away hearts form the lucky user."""
    if not event.user_permissions.administrator:
        abort(f'You must have administrator permission to invoke this command.')
    
    if amount <= 0:
        abort('You cannot award non-positive amount of hearts..')
    
    user_balance = await get_user_balance(target_user.id)
    
    balance = target_user.balance
    can_take = min(balance - user_balance.allocated, amount)
    
    if can_take:
        user_balance.set('balance', balance - can_take)
        await user_balance.save()
    
    yield Embed(
        f'You took {amount} {EMOJI__HEART_CURRENCY} away from {target_user.full_name}',
        f'They got down from {balance} to {balance - can_take} {EMOJI__HEART_CURRENCY}',
        color = COLOR__GAMBLING,
    )


HEART_GENERATOR_COOLDOWNS = set()
HEART_GENERATOR_COOLDOWN = 3600.0
HEART_GENERATION_AMOUNT = 10

INTERACTION_TYPE_APPLICATION_COMMAND = InteractionType.application_command
INTERACTION_TYPE_MESSAGE_COMPONENT = InteractionType.message_component
INTERACTION_TYPE_APPLICATION_COMMAND_AUTOCOMPLETE = InteractionType.application_command_autocomplete


# yup, we are generating hearts
@FEATURE_CLIENTS.events(name = 'interaction_create')
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
        KOKORO.call_after(HEART_GENERATOR_COOLDOWN, set.discard, HEART_GENERATOR_COOLDOWNS, user_id)
        user_balance = await get_user_balance(user_id)
        user_balance.set('balance', user_balance.balance + HEART_GENERATION_AMOUNT)
        await user_balance.save()
