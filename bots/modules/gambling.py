# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from random import random
from math import log, ceil

from hata import Client, elapsed_time, Embed, Color, Emoji, BUILTIN_EMOJIS, DiscordException, sleep, Task, Future, \
    KOKORO, ERROR_CODES, USERS, ZEROUSER
from hata.ext.commands import wait_for_reaction, Timeouter, Cooldown, GUI_STATE_READY, GUI_STATE_SWITCHING_CTX, \
    GUI_STATE_CANCELLED, GUI_STATE_CANCELLING, GUI_STATE_SWITCHING_PAGE, Converter, checks, ConverterFlag, Closer

from sqlalchemy.sql import select, desc

from bot_utils.models import DB_ENGINE, currency_model, CURRENCY_TABLE
from bot_utils.tools import CooldownHandler
from bot_utils.shared import WORSHIPPER_ROLE, DUNGEON_PREMIUM_ROLE, DUNGEON
from bot_utils.command_utils import USER_CONVERTER_EVERYWHERE, USER_CONVERTER_EVERYWHERE_AUTHOR_DEFAULT

Koishi: Client
def setup(lib):
    Koishi.command_processer.append(DUNGEON, heart_generator)

def teardown(lib):
    Koishi.command_processer.remove(DUNGEON, heart_generator)


GAMBLING_COLOR          = Color.from_rgb(254, 254, 164)
CURRENCY_EMOJI          = Emoji.precreate(603533301516599296)
DAILY_INTERVAL          = timedelta(hours=22)
DAILY_STREAK_BREAK      = timedelta(hours=26)
DAILY_STREAK_LOSE       = timedelta(hours=12)
DAILY_REWARD            = 100
DAILY_STREAK_BONUS      = 5
DAILY_REWARD_BONUS_W_W  = 10
DAILY_REWARD_LIMIT      = 300
DAILY_REWARD_LIMIT_W_P  = 600


EVENT_MAX_DURATION      = timedelta(hours=24)
EVENT_MIN_DURATION      = timedelta(minutes=30)
EVENT_HEART_MIN_AMOUNT  = DAILY_REWARD//2               # half day of min
EVENT_HEART_MAX_AMOUNT  = 7*DAILY_REWARD_LIMIT_W_P      # 1 week of max
EVENT_OK_EMOJI          = BUILTIN_EMOJIS['ok_hand']
EVENT_ABORT_EMOJI       = BUILTIN_EMOJIS['x']
EVENT_DAILY_MIN_AMOUNT  = 1
EVENT_DAILY_MAX_AMOUNT  = 7

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
    if user.has_role(WORSHIPPER_ROLE):
        daily_streak_bonus = DAILY_REWARD_BONUS_W_W
    else:
        daily_streak_bonus = DAILY_STREAK_BONUS
    
    if user.has_role(DUNGEON_PREMIUM_ROLE):
        daily_bonus_limit = DAILY_REWARD_LIMIT_W_P
    else:
        daily_bonus_limit = DAILY_REWARD_LIMIT
    
    received = DAILY_REWARD+daily_streak*daily_streak_bonus
    if received > daily_bonus_limit:
        received = daily_bonus_limit
    
    return received

async def daily_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('daily',(
        'Claim everyday your share of my love!\n'
        f'Usage: `{prefix}daily <user>`\n'
        'You can also gift your daily reward to your lovely imouto.'
        ), color=GAMBLING_COLOR)


@Koishi.commands(description=daily_description, category='GAMBLING')
@Cooldown('user', 40., limit=4, weight=2, handler=CooldownHandler())
async def daily(client, message, target_user: USER_CONVERTER_EVERYWHERE_AUTHOR_DEFAULT):
    source_user = message.author
    if target_user.is_bot:
        target_user = source_user
    now = datetime.utcnow()
    async with DB_ENGINE.connect() as connector:
        while True:
            if source_user == target_user:
                response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==source_user.id))
                results = await response.fetchall()
                if results:
                    source_result = results[0]
                    daily_next = source_result.daily_next
                    if daily_next > now:
                        embed = Embed(
                            'You already claimed your daily love for today~',
                            f'Come back in {elapsed_time(daily_next)}.',
                            GAMBLING_COLOR)
                        break
                    daily_streak = source_result.daily_streak
                    daily_next = daily_next+DAILY_STREAK_BREAK
                    if daily_next < now:
                        daily_streak = daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
                        if daily_streak < 0:
                            daily_streak = 0
                        streak_text = f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
                    else:
                        streak_text = f'You are in a {daily_streak} day streak! Keep up the good work!'
                    
                    received = calculate_daily_for(source_user, daily_streak)
                    total_love = source_result.total_love+received
                    
                    await connector.execute(CURRENCY_TABLE.update().values(
                        total_love  = total_love,
                        daily_next  = now+DAILY_INTERVAL,
                        daily_streak= daily_streak+1,
                            ).where(currency_model.user_id==source_user.id))
                    
                    embed = Embed(
                        'Here, some love for you~\nCome back tomorrow !',
                        f'You received {received} {CURRENCY_EMOJI:e} and now have {total_love} {CURRENCY_EMOJI:e}\n'
                        f'{streak_text}',
                        GAMBLING_COLOR)
                    break
                
                await connector.execute(CURRENCY_TABLE.insert().values(
                    user_id     = source_user.id,
                    total_love  = DAILY_REWARD,
                    daily_next  = now+DAILY_INTERVAL,
                    daily_streak= 1,))
                
                embed = Embed(
                    'Here, some love for you~\nCome back tomorrow !',
                    f'You received {DAILY_REWARD} {CURRENCY_EMOJI:e} and now have {DAILY_REWARD} {CURRENCY_EMOJI:e}',
                    GAMBLING_COLOR)
                break
            
            response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id.in_([source_user.id, target_user.id,])))
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
                    
            now=datetime.utcnow()
            if source_result is None:
                daily_streak = 0
                streak_text='I am happy you joined the sect too.'

                await connector.execute(CURRENCY_TABLE.insert().values(
                    user_id     = source_user.id,
                    total_love  = 0,
                    daily_next  = now+DAILY_INTERVAL,
                    daily_streak= 1,))
            else:
                daily_next=source_result.daily_next
                if daily_next > now:
                    embed = Embed(
                        'You already claimed your daily love for today~',
                        f'Come back in {elapsed_time(daily_next)}.',
                        GAMBLING_COLOR)
                    break
                daily_streak = source_result.daily_streak
                daily_next = daily_next+DAILY_STREAK_BREAK
                if daily_next < now:
                    daily_streak = daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
                    if daily_streak < 0:
                        daily_streak = 0
                    streak_text = f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
                else:
                    streak_text = f'You are in a {daily_streak} day streak! Keep up the good work!'
                
                await connector.execute(CURRENCY_TABLE.update().values(
                    daily_next  = now+DAILY_INTERVAL,
                    daily_streak= daily_streak+1,
                        ).where(currency_model.user_id==source_user.id))
            
            received = calculate_daily_for(source_user, daily_streak)
            if target_result is None:
                await connector.execute(CURRENCY_TABLE.insert().values(
                    user_id     = target_user.id,
                    total_love  = received,
                    daily_next  = now,
                    daily_streak= 0,))
                
                total_love = received
            else:
                total_love = target_result.total_love+received
                
                await connector.execute(CURRENCY_TABLE.update().values(
                    total_love  = total_love,
                        ).where(currency_model.user_id==target_user.id))
            
            embed=Embed(
                f'Awww, you claimed your daily love for {target_user:f}, how sweet~',
                f'You gifted {received} {CURRENCY_EMOJI:e} and they have {total_love} {CURRENCY_EMOJI:e}\n{streak_text}',
                GAMBLING_COLOR)
            break
    
    await client.message_create(message.channel,embed=embed)


async def hearts_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('hearts', (
        'How many hearts do you have?\n'
        f'Usage: `{prefix}hearts <user>`\n'
        'You can also check other user\'s hearts too.'
            ), color=GAMBLING_COLOR)


@Koishi.commands(description=hearts_description, category='GAMBLING')
@daily.shared(weight=1)
async def hearts(client,message, target_user: USER_CONVERTER_EVERYWHERE_AUTHOR_DEFAULT):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==target_user.id))
        results = await response.fetchall()
    
    if results:
        result = results[0]
        total_love = result.total_love
        daily_next = result.daily_next
        daily_streak = result.daily_streak
        now = datetime.utcnow()
        if daily_next > now:
            ready_to_claim = False
        else:
            ready_to_claim = True
            
            daily_next = daily_next+DAILY_STREAK_BREAK
            if daily_next < now:
                daily_streak = daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
                if daily_streak < 0:
                    daily_streak = 0
    
    else:
        total_love = 0
        daily_streak = 0
        ready_to_claim = True
    
    is_own = ( message.author is target_user)
    
    if is_own:
        title_prefix = 'You have'
    else:
        title_prefix = target_user.full_name+' has'
    
    title = f'{title_prefix} {total_love} {CURRENCY_EMOJI:e}'
    
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
    
    embed = Embed( title, description, color=GAMBLING_COLOR)
    await client.message_create(message.channel, embed=embed)


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


class heartevent_start_checker(object):
    __slots__ = ('client',)
    def __init__(self,client):
        self.client=client

    def __call__(self, event):
        if not self.client.is_owner(event.user):
            return False
        
        emoji = event.emoji
        if (emoji is EVENT_OK_EMOJI) or (emoji is EVENT_ABORT_EMOJI):
            return True
        
        return False


async def heartevent_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('heartevent', (
        'Starts a heart event at the channel.\n'
        f'Usage: `{prefix}heartevent *duration* *amount* <users_limit>`\n'
        f'Min `duration`: {convert_tdelta(EVENT_MIN_DURATION)}\n'
        f'Max `duration`: {convert_tdelta(EVENT_MAX_DURATION)}\n'
        f'Min `amount`: {EVENT_HEART_MIN_AMOUNT}\n'
        f'Max `amount`: {EVENT_HEART_MAX_AMOUNT}\n'
        'If `user_limit` is not included, the event will have no user limit.'
            ), color=GAMBLING_COLOR).add_footer(
            'Owner only!')


@Koishi.commands(checks=checks.owner_only(), description=heartevent_description, category='GAMBLING')
class heartevent(object):
    _update_time = 60.
    _update_delta = timedelta(seconds=_update_time)
    
    __slots__=('amount', 'client', 'connector', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    async def __new__(cls, client, message, duration:timedelta, amount:int, user_limit:int=0):
        channel = message.channel
        while True:
            if duration > EVENT_MAX_DURATION:
                embed = Embed('Duration passed the upper limit\n',
                     f'**>**  upper limit : {convert_tdelta(EVENT_MAX_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif duration < EVENT_MIN_DURATION:
                embed = Embed('Duration passed the lower limit\n',
                     f'**>**  lower limit : {convert_tdelta(EVENT_MIN_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif amount > EVENT_HEART_MAX_AMOUNT:
                embed = Embed('Amount passed the upper limit\n',
                     f'**>**  upper limit : {EVENT_HEART_MAX_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif amount < EVENT_HEART_MIN_AMOUNT:
                embed = Embed('Amount passed the lower limit\n',
                     f'**>**  lower limit : {EVENT_HEART_MIN_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif user_limit < 0:
                embed = Embed('User limit passed the lower limit\n',
                      '**>** lower limit : 0\n'
                     f'**>**  - passed : {user_limit}',
                      color=GAMBLING_COLOR)
            else:
                break
            
            to_delete = await client.message_create(channel, embed=embed)
            await sleep(30., KOKORO)
            try:
                await client.message_delete(to_delete)
                await client.message_delete(message)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return None
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                ):
                        return None
                
                raise
            
            return None
        
        result = []
        result.append('Duration: ')
        result.append(convert_tdelta(duration))
        result.append('\n Amount : ')
        result.append(str(amount))
        if user_limit:
            result.append('\n user limit : ')
            result.append(str(user_limit))
        
        embed = Embed('Is everything correct?', ''.join(result), color=GAMBLING_COLOR)
        del result
        
        to_check = await client.message_create(channel, embed=embed)
        
        try:
            await client.reaction_add(to_check, EVENT_OK_EMOJI)
            await client.reaction_add(to_check, EVENT_ABORT_EMOJI)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return None
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return None
            
            raise
        
        try:
            event = await wait_for_reaction(client, to_check, heartevent_start_checker(client), 1800.)
        except TimeoutError:
            return
        finally:
            try:
                await client.message_delete(to_check)
                await client.message_delete(message)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return None
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                ):
                        return None
                
                raise
        
        if event.emoji is EVENT_ABORT_EMOJI:
            return
        
        self = object.__new__(cls)
        self.connector = None
        self.user_ids = set()
        self.user_limit = user_limit
        self.client = client
        self.duration = duration
        self.amount = amount
        self.waiter = Future(KOKORO)
        
        try:
            message = await client.message_create(channel, embed=self.generate_embed())
        except BaseException as err:
            self.message = None
            if isinstance(err, ConnectionError):
                return None
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return None
            
            raise
        
        self.message = message
        
        self.connector = await DB_ENGINE.connect()
        
        client.events.reaction_add.append(message, self)
        Task(self.countdown(client, message), KOKORO)
        await client.reaction_add(message, CURRENCY_EMOJI)
        return self
    
    def generate_embed(self):
        title = f'React with {CURRENCY_EMOJI:e} to receive {self.amount}'
        if self.user_limit:
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit-len(self.user_ids)} users'
        else:
            description = f'{convert_tdelta(self.duration)} left'
        return Embed(title, description, color=GAMBLING_COLOR)

    async def __call__(self, client, event):
        user = event.user
        if user.is_bot or (event.emoji is not CURRENCY_EMOJI):
            return
        
        user_id = user.id
        user_ids = self.user_ids
        
        old_ln = len(user_ids)
        user_ids.add(user_id)
        new_ln = len(user_ids)
        
        if new_ln == old_ln:
            return

        if new_ln == self.user_limit:
            self.duration=timedelta()
            self.waiter.set_result(None)
        
        connector = self.connector
        
        response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==user_id))
        results = await response.fetchall()
        if results:
            result = results[0]
            to_execute = CURRENCY_TABLE.update().values(
                total_love  = result.total_love+self.amount,
                    ).where(currency_model.user_id==user_id)
        else:
            to_execute=CURRENCY_TABLE.insert().values(
                user_id     = user_id,
                total_love  = self.amount,
                daily_next  = datetime.utcnow(),
                daily_streak= 0,)
        await connector.execute(to_execute)

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
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                ):
                        break
                
                await client.events.error(client, f'{self!r}.countdown', err)
                break
        
        client.events.reaction_add.remove(message, self)
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
                        ERROR_CODES.invalid_access, # client removed
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
        
async def dailyevent_description(client,message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('dailyevent',(
        'Starts a daily event at the channel.\n'
        f'Usage: `{prefix}dailyevent *duration* *amount* <users_limit>`\n'
        f'Min `duration`: {convert_tdelta(EVENT_MIN_DURATION)}\n'
        f'Max `duration`: {convert_tdelta(EVENT_MAX_DURATION)}\n'
        f'Min `amount`: {EVENT_DAILY_MIN_AMOUNT}\n'
        f'Max `amount`: {EVENT_DAILY_MAX_AMOUNT}\n'
        'If `user_limit` is not included, the event will have no user limit.'
            ), color=GAMBLING_COLOR).add_footer(
            'Owner only!')

    
@Koishi.commands(checks=checks.owner_only(), description=dailyevent_description, category='GAMBLING')
class dailyevent(object):
    _update_time=60.
    _update_delta=timedelta(seconds=_update_time)

    __slots__=('amount', 'client', 'connector', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    async def __new__(cls, client, message, duration:timedelta, amount:int, user_limit: int=0):
        channel = message.channel
        while True:
            if duration > EVENT_MAX_DURATION:
                embed = Embed('Duration passed the upper limit\n',
                     f'**>**  upper limit : {convert_tdelta(EVENT_MAX_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif duration < EVENT_MIN_DURATION:
                embed = Embed('Duration passed the lower limit\n',
                     f'**>**  lower limit : {convert_tdelta(EVENT_MIN_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif amount > EVENT_DAILY_MAX_AMOUNT:
                embed = Embed('Amount passed the upper limit\n',
                     f'**>**  upper limit : {EVENT_DAILY_MAX_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif amount < EVENT_DAILY_MIN_AMOUNT:
                embed = Embed('Amount passed the lower limit\n',
                     f'**>**  lower limit : {EVENT_DAILY_MIN_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif user_limit < 0:
                embed = Embed('User limit passed the lower limit\n',
                      '**>** lower limit : 0\n'
                     f'**>**  - passed : {user_limit}',
                      color=GAMBLING_COLOR)
            else:
                break
            
            to_delete = await client.message_create(channel, embed=embed)
            await sleep(30., KOKORO)
            try:
                await client.message_delete(to_delete)
                await client.message_delete(message)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return None
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ERROR_CODES.invalid_message_send_user, # user has dm-s disallowed
                                ):
                        return None
                
                raise
            
            return None
        
        result = []
        result.append('Duration: ')
        result.append(convert_tdelta(duration))
        result.append('\n Amount : ')
        result.append(str(amount))
        if user_limit:
            result.append('\n user limit : ')
            result.append(str(user_limit))
        
        embed = Embed('Is everything correct?', ''.join(result), color=GAMBLING_COLOR)
        del result
        
        to_check = await client.message_create(channel, embed=embed)
        
        try:
            await client.reaction_add(to_check, EVENT_OK_EMOJI)
            await client.reaction_add(to_check, EVENT_ABORT_EMOJI)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return None
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return None
            
            raise
        
        try:
            event = await wait_for_reaction(client, to_check, heartevent_start_checker(client), 1800.)
        except TimeoutError:
            return
        finally:
            try:
                await client.message_delete(to_check)
                await client.message_delete(message)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    return None
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.unknown_message, # message deleted
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                ):
                        return None
                
                raise
        
        if event.emoji is EVENT_ABORT_EMOJI:
            return
        
        self = object.__new__(cls)
        self.connector = None
        self.user_ids = set()
        self.user_limit = user_limit
        self.client = client
        self.duration = duration
        self.amount = amount
        self.waiter = Future(KOKORO)
        
        try:
            message = await client.message_create(channel, embed=self.generate_embed())
        except BaseException as err:
            self.message = None
            if isinstance(err, ConnectionError):
                return None
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                            ):
                    return None
            
            raise
        
        self.message = message
        self.connector = await DB_ENGINE.connect()
        
        client.events.reaction_add.append(message, self)
        Task(self.countdown(client, message), KOKORO)
        await client.reaction_add(message, CURRENCY_EMOJI)
        return self
    
    def generate_embed(self):
        title = f'React with {CURRENCY_EMOJI:e} to increase your daily streak by {self.amount}'
        if self.user_limit:
            description = f'{convert_tdelta(self.duration)} left or {self.user_limit-len(self.user_ids)} users'
        else:
            description = f'{convert_tdelta(self.duration)} left'
        return Embed(title, description, color=GAMBLING_COLOR)
    
    async def __call__(self, client, event):
        user = event.user
        if user.is_bot or (event.emoji is not CURRENCY_EMOJI):
            return
        
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
        
        response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==user_id))
        results = await response.fetchall()
        if results:
            result = results[0]
            now = datetime.utcnow()
            daily_next = result.daily_next+DAILY_STREAK_BREAK
            if daily_next > now:
                to_execute=CURRENCY_TABLE.update().values(
                    daily_streak  = result.daily_streak+self.amount,
                        ).where(currency_model.user_id==user_id)
            else:
                daily_streak=result.daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
                if daily_streak < 0:
                    daily_streak = self.amount
                else:
                    daily_streak = daily_streak+self.amount

                to_execute=CURRENCY_TABLE.update().values(
                    daily_streak= daily_streak,
                    daily_next  = now,
                        ).where(currency_model.user_id==user_id)

        else:
            to_execute=CURRENCY_TABLE.insert().values(
                user_id     = user_id,
                total_love  = 0,
                daily_next  = datetime.utcnow(),
                daily_streak= self.amount,)
        await connector.execute(to_execute)
    
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
                            ERROR_CODES.invalid_access, # client removed
                            ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                                ):
                        break
                
                await client.events.error(client, f'{self!r}.countdown', err)
                break
        
        client.events.reaction_add.remove(message, self)
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
                        ERROR_CODES.invalid_access, # client removed
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


async def game21_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('21',(
        'Starts a 21 game at the channel.\n'
        f'Usage: `{prefix}21 *amount*`\n'
        'Your chalange is to collect cards with weight up to 21. Each card with number 2-10 has the same weight as '
        'their number says, meanwhile J, Q and K has fix weight of 10. Ace has weight of 11, but if You would pass '
        '21, it loses 9 of it.\n'
        'At this game you are fighting me, so if we boss lose, it is a draw.\n'
        'You start with 2 cards initially drawed and at every round, you have option to draw a new card, or to stop.'
            ), color=GAMBLING_COLOR)


@Koishi.commands(name='21', description=game21_description, category='GAMBLING')
class Game21(object):
    NEW = BUILTIN_EMOJIS['new']
    STOP = BUILTIN_EMOJIS['octagonal_sign']
    EMOJIS = (NEW, STOP)
    
    __slots__ = ('all_pulled', 'amount', 'canceller', 'channel', 'client', 'client_hand', 'client_total', 'message',
        'task_flag', 'timeouter', 'user', 'user_ace', 'user_hand', 'user_total')
    
    def pull_card(all_pulled):
        card = int((DECK_SIZE-len(all_pulled))*random())
        for pulled in all_pulled:
            if pulled > card:
                break
            
            card += 1
            continue
        
        all_pulled.append(card)
        all_pulled.sort()
        
        return card
    
    async def __new__(cls, client, source_message, amount:int=0):
        user = source_message.author
        channel = source_message.channel
        
        while True:
            if user.id in IN_GAME_IDS:
                error_msg = f'You are already at a game.'
                break
            
            if amount < BET_MIN:
                error_msg = f'You must bet at least {BET_MIN} {CURRENCY_EMOJI.as_emoji}'
                break
        
            if not channel.cached_permissions_for(client).can_add_reactions:
                error_msg = 'I cannot start this command here, not enough permissions provided.'
                break
            
            async with DB_ENGINE.connect() as connector:
                response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==user.id))
                results = await response.fetchall()
                if results:
                    total_love = results[0].total_love

                    if total_love < amount:
                        error_msg=f'You have just {total_love} {CURRENCY_EMOJI.as_emoji}'
                        break
                    
                    await connector.execute(CURRENCY_TABLE.update().values(
                        total_love  = total_love-amount,
                            ).where(currency_model.user_id==user.id))
                
                else:
                    error_msg=f'You have 0 {CURRENCY_EMOJI.as_emoji}'
                    break
            
            error_msg = None
            break
        
        if (error_msg is not None):
            await client.message_create(channel,
                embed=Embed(error_msg, color=GAMBLING_COLOR))
            return None
        
        IN_GAME_IDS.add(user.id)
        
        all_pulled = []
        
        client_hand = []
        client_total = 0
        client_ace = 0
        
        while True:
            card = cls.pull_card(all_pulled)
            
            client_hand.append(card)
            
            number_index = card%len(CARD_NUMBERS)
            if number_index == ACE_INDEX:
                client_ace += 1
                card_weight = 11
            elif number_index > 7:
                card_weight = 10
            else:
                card_weight = number_index+2
            
            client_total += card_weight
            
            while client_total>21 and client_ace:
                client_total -= 10
                client_ace -= 1
            
            if client_total > (17 if client_ace else 15):
                break
            
            continue
        
        
        user_hand = []
        user_total = 0
        user_ace = 0
        
        while True:
            card = cls.pull_card(all_pulled)
            
            user_hand.append(card)
            
            number_index = card%len(CARD_NUMBERS)
            if number_index == ACE_INDEX:
                user_ace += 1
                card_weight = 11
            elif number_index > 7:
                card_weight = 10
            else:
                card_weight = number_index+2
            
            user_total += card_weight
            
            if user_total > 10:
                break
        
        embed = Embed(f'How to gamble {amount} {CURRENCY_EMOJI.as_emoji}',
            f'You have cards equal to {user_total} weight at your hand',
            color=GAMBLING_COLOR)
        
        for round_,card in enumerate(user_hand, 1):
            type_index, number_index = divmod(card,len(CARD_NUMBERS))
            embed.add_field(f'Round {round_}',
                f'You pulled {CARD_TYPES[type_index]} {CARD_NUMBERS[number_index]}')
        
        try:
            message = await client.message_create(channel, embed=embed)
            for emoji in cls.EMOJIS:
                await client.reaction_add(message, emoji)
        
        except BaseException as err:
            # If exception occures right here we need to remove the game from
            # games and revert the heart amount
            IN_GAME_IDS.remove(user.id)

            async with DB_ENGINE.connect() as connector:
                response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==user.id))
                results = await response.fetchall()
                if results:
                    total_love = results[0].total_love
                    to_execute = CURRENCY_TABLE.update().values(
                        total_love  = total_love,
                            ).where(currency_model.user_id==user.id)
                else:
                    to_execute = CURRENCY_TABLE.insert().values(
                        user_id     = user.id,
                        total_love  = amount,
                        daily_next  = datetime.utcnow(),
                        daily_streak= 0,)
                
                await connector.execute(to_execute)
            
            if isinstance(err, ConnectionError):
                return None
            
            if isinstance(err, DiscordException):
                if err.code in (
                        ERROR_CODES.unknown_message, # message deleted
                        ERROR_CODES.unknown_channel, # message's channel deleted
                        ERROR_CODES.max_reactions, # reached reaction 20, some1 is trolling us.
                        ERROR_CODES.invalid_access, # client removed
                        ERROR_CODES.invalid_permissions, # permissions changed meanwhile
                    ):
                 return None
            
            raise
        
        self = object.__new__(cls)
        self.client = client
        self.channel = channel
        self.canceller = cls._canceller
        self.task_flag = GUI_STATE_READY
        self.message = message
        self.user = user
        self.amount = amount
        self.all_pulled = all_pulled
        self.user_hand = user_hand
        self.user_total = user_total
        self.user_ace = user_ace
        self.client_hand = client_hand
        self.client_total = client_total
        self.timeouter = Timeouter(self, timeout=300.)
        client.events.reaction_add.append(message, self)
        client.events.reaction_delete.append(message, self)
        return self
    
    async def __call__(self, client, event):
        if (event.user != self.user) or (event.emoji not in self.EMOJIS):
            return
        
        if (event.delete_reaction_with(client) == event.DELETE_REACTION_NOT_ADDED):
            return
        
        emoji = event.emoji
        task_flag = self.task_flag
        if task_flag != GUI_STATE_READY:
            if task_flag == GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self.task_flag = GUI_STATE_CANCELLING
                return

            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        if emoji is self.NEW:
            # It is enough to delete the reaction at this ase if needed,
            # because after the other cases we will delete them anyways.
            card = type(self).pull_card(self.all_pulled)
            
            self.user_hand.append(card)
            
            user_ace = self.user_ace
            number_index = card%len(CARD_NUMBERS)
            if number_index == ACE_INDEX:
                user_ace += 1
                card_weight = 11
            elif number_index > 7:
                card_weight = 10
            else:
                card_weight = number_index+2
            
            user_total = self.user_total + card_weight
            while user_total > 21 and user_ace:
                user_total -= 10
                user_ace -= 1
            
            self.user_total = user_total
            self.user_ace = user_ace
            
            game_ended = (user_total>21)
            
        elif emoji is self.STOP:
            game_ended = True
        
        else:
            # should not happen
            return
        
        if game_ended:
            self.task_flag = GUI_STATE_CANCELLED
            self.cancel()
            
            user_total = self.user_total
            client_total = self.client_total
            
            if client_total > 21:
                if user_total > 21:
                    winner = None
                else:
                    winner = self.user
            else:
                if user_total > 21:
                    winner = client
                else:
                    if client_total > user_total:
                        winner = client
                    elif client_total < user_total:
                        winner = self.user
                    else:
                        winner = None
            
            if (winner is not client):
                if winner is None:
                    bonus = self.amount
                else:
                    bonus = self.amount*2
                    
                async with DB_ENGINE.connect() as connector:
                    response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==self.user.id))
                    results = await response.fetchall()

                    if results:
                        total_love = results[0].total_love
                        
                        to_execute=CURRENCY_TABLE.update().values(
                            total_love  = total_love+bonus,
                                ).where(currency_model.user_id==self.user.id)
                    else:
                        to_execute=CURRENCY_TABLE.insert().values(
                            user_id     = self.user.id,
                            total_love  = bonus,
                            daily_next  = datetime.utcnow(),
                            daily_streak= 0,)
                    
                    await connector.execute(to_execute)
                
            if winner is None:
                title = f'How to draw.'
            elif winner is client:
                title = f'How to lose {self.amount} {CURRENCY_EMOJI.as_emoji}'
            else:
                title = f'How to win {self.amount} {CURRENCY_EMOJI.as_emoji}'
            
            embed=Embed(title,color=GAMBLING_COLOR)
            
            field_content=[]
            
            for round_, card in enumerate(self.user_hand, 1):
                type_index, number_index = divmod(card, len(CARD_NUMBERS))
                field_content.append('Round ')
                field_content.append(str(round_))
                field_content.append(': ')
                field_content.append(CARD_TYPES[type_index])
                field_content.append(' ')
                field_content.append(CARD_NUMBERS[number_index])
                field_content.append('\n')
            
            embed.add_field(f'{self.user.name_at(self.message.guild)}\'s cards\' weight: {user_total}',
                ''.join(field_content))
            field_content.clear()
            
            for round_, card in enumerate(self.client_hand, 1):
                type_index, number_index = divmod(card, len(CARD_NUMBERS))
                field_content.append('Round ')
                field_content.append(str(round_))
                field_content.append(': ')
                field_content.append(CARD_TYPES[type_index])
                field_content.append(' ')
                field_content.append(CARD_NUMBERS[number_index])
                field_content.append('\n')
            
            embed.add_field(f'{client.name_at(self.message.guild)}\'s cards\' weight: {client_total}',
                ''.join(field_content))
            field_content = None
            
            try:
                await client.message_edit(self.message, embed=embed)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message already deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                # We definitedly do not want to silence `ERROR_CODES.invalid_form_body`
                await client.events.error(client,f'{self!r}.__call__',err)
                return
                
        else:
            embed = Embed(f'How to gamble {self.amount} {CURRENCY_EMOJI.as_emoji}',
                f'You have cards equal to {user_total} weight at your hand',
                color=GAMBLING_COLOR)
            
            for round_, card in enumerate(self.user_hand, 1):
                type_index, number_index = divmod(card, len(CARD_NUMBERS))
                embed.add_field(f'Round {round_}',
                    f'You pulled {CARD_TYPES[type_index]} {CARD_NUMBERS[number_index]}')
            
            self.task_flag = GUI_STATE_SWITCHING_PAGE
            
            try:
                await client.message_edit(self.message, embed=embed)
            except BaseException as err:
                self.task_flag = GUI_STATE_CANCELLED
                self.cancel()
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message already deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                # We definitedly do not want to silence `ERROR_CODES.invalid_form_body`
                await client.events.error(client, f'{self!r}.__call__', err)
                return
            
            self.task_flag = GUI_STATE_READY
            self.timeouter.set_timeout(300.0)
        
    async def _canceller(self, exception,):
        IN_GAME_IDS.remove(self.user.id)
        
        client = self.client
        message = self.message
        
        client.events.reaction_add.remove(message, self)
        client.events.reaction_delete.remove(message, self)
        
        if self.task_flag == GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return

        self.task_flag = GUI_STATE_CANCELLED

        if self.channel.cached_permissions_for(client).can_manage_messages:
            task = Task(client.reaction_clear(message), KOKORO)
            if __debug__:
                task.__silence__()
        
        if exception is None:
            return
        
        if isinstance(exception, TimeoutError):
            IN_GAME_IDS.remove(self.user.id)
            
            embed = Embed(f'Timeout occured, you lost your {self.amount} {CURRENCY_EMOJI.as_emoji} forever.')
            
            try:
                await client.message_edit(message, embed=embed)
            except BaseException as err:
                if isinstance(err, ConnectionError):
                    # no internet
                    return
                
                if isinstance(err, DiscordException):
                    if err.code in (
                            ERROR_CODES.unknown_message, # message already deleted
                            ERROR_CODES.unknown_channel, # message's channel deleted
                            ERROR_CODES.invalid_access, # client removed
                                ):
                        return
                
                # We definitedly do not want to silence `ERROR_CODES.invalid_form_body`
                await client.events.error(client, f'{self!r}._canceller', err)
                return
            
            return
        
        timeouter = self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self, exception=None):
        canceller = self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter = self.timeouter
        if (timeouter is not None):
            timeouter.cancel()
        
        return Task(canceller(self,exception), KOKORO)


async def gift_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('gift',(
        'Gifts hearts to your heart\'s chosen one.\n'
        f'Usage: `{prefix}gift *user* *amount*`\n'
        ), color=GAMBLING_COLOR).add_footer(
            f'You must have {WORSHIPPER_ROLE.name} or {DUNGEON_PREMIUM_ROLE.name} role!')


@Koishi.commands(description=gift_description, category='GAMBLING',
    checks=checks.has_any_role([WORSHIPPER_ROLE, DUNGEON_PREMIUM_ROLE]))
@daily.shared(weight=1)
async def gift(client, message, target_user: USER_CONVERTER_EVERYWHERE, amount:int):
    source_user = message.author
    while True:
        if source_user == target_user:
            embed = Embed('BAKA !!','You cannot give love to yourself..', GAMBLING_COLOR)
            break
    
        if amount <= 0:
            embed = Embed('BAKA !!','You cannot gift non-positive amount of hreats..', GAMBLING_COLOR)
            break
            
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(select([currency_model.total_love]).where(currency_model.user_id==source_user.id))
            results = await response.fetchall()
            if results:
                source_user_total_love = results[0][0]
            else:
                source_user_total_love = 0
            
            if source_user_total_love == 0:
                embed = Embed('So lonely...', 'You do not have any hreats to gift.', GAMBLING_COLOR)
                break
            
            response = await connector.execute(select([currency_model.total_love]).where(currency_model.user_id==target_user.id))
            results = await response.fetchall()
            if results:
                target_user_exists = True
                target_user_total_love = results[0][0]
            else:
                target_user_exists = False
                target_user_total_love = 0
            
            if amount > source_user_total_love:
                amount = source_user_total_love
                source_user_new_love = 0
            else:
                source_user_new_love = source_user_total_love-amount
            
            target_user_new_love = target_user_total_love + amount
            
            await connector.execute(CURRENCY_TABLE.update().values(
                    total_love  = source_user_new_love,
                    ).where(currency_model.user_id==source_user.id)
                )
            
            if target_user_exists:
                to_execute = CURRENCY_TABLE.update().values(
                    total_love  = target_user_new_love,
                    ).where(currency_model.user_id==target_user.id)
            else:
                to_execute = CURRENCY_TABLE.insert().values(
                    user_id     = target_user.id,
                    total_love  = target_user_new_love,
                    daily_next  = datetime.utcnow(),
                    daily_streak= 0,)
            
            await connector.execute(to_execute)
            
            embed = Embed('Aww, so lovely', f'You gifted {amount} {CURRENCY_EMOJI.as_emoji} to {target_user.full_name}',
                GAMBLING_COLOR,
                    ).add_field(
                        f'Your {CURRENCY_EMOJI.as_emoji}',
                        f'{source_user_total_love} -> {source_user_new_love}',
                    ).add_field(
                        f'Their {CURRENCY_EMOJI.as_emoji}',
                        f'{target_user_total_love} -> {target_user_new_love}',
                    )
            break
    
    await client.message_create(message.channel, embed=embed)


async def award_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('award',(
        'Awards someone with the given amount of hearts.\n'
        f'Usage: `{prefix}award *user* *amount*`'
        ), color=GAMBLING_COLOR).add_footer(
            f'Owner only.')

async def parser_failure_handler(client, message, command, content, args):
    embed = await command.description(client, message)
    await Closer(client, message.channel, embed)

@Koishi.commands(
    description = gift_description,
    category = 'GAMBLING',
    checks = [checks.owner_only()],
    parser_failure_handler = parser_failure_handler,
        )
async def award(client, message, target_user: USER_CONVERTER_EVERYWHERE, amount:int):
    
    if amount <= 0:
        await award_description(client, message)
        return
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(select([currency_model.total_love]).where(currency_model.user_id==target_user.id))
        results = await response.fetchall()
        if results:
            target_user_exists = True
            target_user_total_love = results[0][0]
        else:
            target_user_exists = False
            target_user_total_love = 0
        
        target_user_new_love = target_user_total_love+amount
        
        if target_user_exists:
            to_execute = CURRENCY_TABLE.update().values(
                total_love  = target_user_new_love,
                ).where(currency_model.user_id==target_user.id)
        else:
            to_execute = CURRENCY_TABLE.insert().values(
                user_id     = target_user.id,
                total_love  = target_user_new_love,
                daily_next  = datetime.utcnow(),
                daily_streak= 0,)
        
        await connector.execute(to_execute)
    
    embed = Embed(f'You awarded {target_user.full_name} with {amount} {CURRENCY_EMOJI.as_emoji}',
        f'Now they are up from {target_user_total_love} to {target_user_new_love} {CURRENCY_EMOJI.as_emoji}',
        color=GAMBLING_COLOR)
    
    await client.message_create(message.channel, embed=embed)


async def take_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('take',(
        'Takes the given amount of hearts from someone.\n'
        f'Usage: `{prefix}take *user* *amount*`'
        ), color=GAMBLING_COLOR).add_footer(
            f'Owner only.')

@Koishi.commands(
    description = take_description,
    category = 'GAMBLING',
    checks = [checks.owner_only()],
    parser_failure_handler = parser_failure_handler,
        )
async def take(client, message, target_user: USER_CONVERTER_EVERYWHERE, amount:int):
    
    if amount <= 0:
        await take_description(client, message)
        return
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(select([currency_model.total_love]).where(currency_model.user_id==target_user.id))
        results = await response.fetchall()
        if results:
            target_user_total_love = results[0][0]
            if target_user_total_love == 0:
                target_user_new_love = 0
            else:
                target_user_new_love = target_user_total_love-amount
                if target_user_new_love < 0:
                    target_user_new_love = 0
                
                await connector.execute(CURRENCY_TABLE.update().values(
                    total_love  = target_user_new_love,
                    ).where(currency_model.user_id==target_user.id))
        else:
            target_user_total_love = 0
            target_user_new_love = 0
    
    embed = Embed(f'You took {amount} {CURRENCY_EMOJI.as_emoji} away from {target_user.full_name}',
        f'Theiy got down from {target_user_total_love} to {target_user_new_love} {CURRENCY_EMOJI.as_emoji}',
        color=GAMBLING_COLOR)
    
    await client.message_create(message.channel, embed=embed)


async def top_description(client, message):
    prefix = client.command_processer.get_prefix_for(message)
    return Embed('top',(
        'Shows the most favored persons by myself.\n'
        f'Usage: `{prefix}top`'
        ), color=GAMBLING_COLOR)


@Koishi.commands(description=top_description, category='GAMBLING', aliases='top-list')
@daily.shared(weight=1)
async def top(client, message):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select([currency_model.user_id, currency_model.total_love])
                .where(currency_model.total_love != 0)
                .order_by(desc(currency_model.total_love))
                .limit(20)
                    )
        results = await response.fetchall()
        
        parts = []
        total_hearts_longest = 1
        
        for index, (user_id, total_hearts) in enumerate(results, 1):
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
                            # Should not happen, but can, so lets handle it
                            await connector.execute(CURRENCY_TABLE.delete().where(currency_model.user_id==user_id))
                            user = ZEROUSER
                        else:
                            raise
                    
                    else:
                        raise
            
            total_hearts_length = ceil(log(total_hearts, 10))
            if total_hearts_length > total_hearts_longest:
                total_hearts_longest = total_hearts_length
            parts.append((index, total_hearts, user.full_name))
    
    result_lines = [f'{CURRENCY_EMOJI.as_emoji} **Toplist** {CURRENCY_EMOJI.as_emoji}\n```cs\n']
    for index, total_hearts, full_name in parts:
        result_lines.append(f'{index:>2}.: {total_hearts:>{total_hearts_longest}} {full_name}\n')
    
    result_lines.append('```')
    
    await client.message_create(message.channel, ''.join(result_lines))


HEART_GENERATOR_COOLDOWNS = set()
HEART_GENERATOR_COOLDOWN = 3600.0
HEART_GENERATION_AMOUNT = 5

async def heart_generator(client, message):
    user = message.author
    if user.is_bot:
        return
    
    if random() >= 0.01:
        return
    
    user_id = user.id
    if user_id in HEART_GENERATOR_COOLDOWNS:
        return
    
    HEART_GENERATOR_COOLDOWNS.add(user_id)
    
    KOKORO.call_later(HEART_GENERATOR_COOLDOWN, set.remove, HEART_GENERATOR_COOLDOWNS, user_id)
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(select([currency_model.total_love]).where(currency_model.user_id==user_id))
        results = await response.fetchall()
        if results:
            target_user_exists = True
            target_user_total_love = results[0][0]
        else:
            target_user_exists = False
            target_user_total_love = 0
        
        target_user_new_love = target_user_total_love+HEART_GENERATION_AMOUNT
        
        if target_user_exists:
            to_execute = CURRENCY_TABLE.update().values(
                total_love  = target_user_new_love,
                ).where(currency_model.user_id==user_id)
        else:
            to_execute = CURRENCY_TABLE.insert().values(
                user_id     = user_id,
                total_love  = target_user_new_love,
                daily_next  = datetime.utcnow(),
                daily_streak= 0,)
        
        await connector.execute(to_execute)
