# -*- coding: utf-8 -*-
from datetime import datetime,timedelta
from random import random

from hata.parsers import eventlist
from hata.events_compiler import ContentParser
from hata.others import elapsed_time
from hata.events import wait_for_reaction, WaitAndContinue, Timeouter,      \
    Cooldown, GUI_STATE_READY, GUI_STATE_SWITCHING_CTX, GUI_STATE_CANCELLED,\
    GUI_STATE_CANCELLING, GUI_STATE_SWITCHING_PAGE

from hata.embed import Embed
from hata.color import Color
from hata.emoji import Emoji, BUILTIN_EMOJIS
from hata.exceptions import DiscordException
from hata.futures import sleep, Task, Future

from models import DB_ENGINE,currency_model,CURRENCY_TABLE
from tools import CooldownHandler
from help_handler import KOISHI_HELP_COLOR, KOISHI_HELPER

GAMBLING_COLOR          = Color.from_rgb(254,254,164)
CURRENCY_EMOJI          = Emoji.precreate(603533301516599296)
DAILY_INTERVAL          = timedelta(hours=22)
DAILY_STREAK_BREAK      = timedelta(hours=26)
DAILY_STREAK_LOSE       = timedelta(hours=12)
DAILY_REWARD            = 100
DAILY_STREAK_BONUS      = 5
DAILY_REWARD_LIMIT      = 300

EVENT_MAX_DURATION      = timedelta(hours=24)
EVENT_MIN_DURATION      = timedelta(minutes=30)
EVENT_HEART_MIN_AMOUNT  = DAILY_REWARD//2           #half day of min
EVENT_HEART_MAX_AMOUNT  = 7*DAILY_REWARD_LIMIT      #1 week of max
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

class game_21_checker(object):
    __slots__=('user')
    def __init__(self,user):
        self.user=user
    def __call__(self,emoji,user):
        return (user==self.user) and (emoji in GAME_21_EMOJIS)
    
def wait_for_reaction_any(client,message,case,timeout):
    future=Future(client.loop)
    
    WaitAndContinue(future, case, message, multievent(
        client.events.reaction_add, client.events.reaction_delete
            ), timeout)
    
    return future

gambling=eventlist()

@gambling
@Cooldown('user',40.,limit=4,weight=2,handler=CooldownHandler())
@ContentParser('user, flags=mni, default="message.author"')
async def daily(client,message,target_user):
    source_user=message.author
    if target_user.is_bot:
        target_user=source_user
    now=datetime.utcnow()
    async with DB_ENGINE.connect() as connector:
        while True:
            if source_user is target_user:
                response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==source_user.id))
                results = await response.fetchall()
                if results:
                    source_result=results[0]
                    daily_next=source_result.daily_next
                    if daily_next>now:
                        embed=Embed(
                            'You already claimed your daily love for today~',
                            f'Come back in {elapsed_time(daily_next)}.',
                            GAMBLING_COLOR)
                        break
                    daily_streak=source_result.daily_streak
                    daily_next=daily_next+DAILY_STREAK_BREAK
                    if daily_next<now:
                        daily_streak=daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
                        if daily_streak<0:
                            daily_streak=0
                        streak_text=f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
                    else:
                        streak_text=f'You are in a {daily_streak} day streak! Keep up the good work!'
                    
                    received=DAILY_REWARD+daily_streak*DAILY_STREAK_BONUS
                    if received>DAILY_REWARD_LIMIT:
                        received=DAILY_REWARD_LIMIT
                    total_love=source_result.total_love+received
                    
                    await connector.execute(CURRENCY_TABLE.update().values(
                        total_love  = total_love,
                        daily_next  = now+DAILY_INTERVAL,
                        daily_streak= daily_streak+1,
                            ).where(currency_model.user_id==source_user.id))
                    
                    embed=Embed(
                        'Here, some love for you~\nCome back tomorrow !',
                        f'You received {received} {CURRENCY_EMOJI:e} and now have {total_love} {CURRENCY_EMOJI:e}\n{streak_text}',
                        GAMBLING_COLOR)
                    break
                
                await connector.execute(CURRENCY_TABLE.insert().values(
                    user_id     = source_user.id,
                    total_love  = DAILY_REWARD,
                    daily_next  = now+DAILY_INTERVAL,
                    daily_streak= 1,))
                
                embed=Embed(
                    'Here, some love for you~\nCome back tomorrow !',
                    f'You received {DAILY_REWARD} {CURRENCY_EMOJI:e} and now have {DAILY_REWARD} {CURRENCY_EMOJI:e}',
                    GAMBLING_COLOR)
                break
            
            response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id.in_([source_user.id,target_user.id,])))
            results = await response.fetchall()
            if len(results)==0:
                source_result=None
                target_result=None
            elif len(results)==1:
                if results[0].user_id==source_user.id:
                    source_result=results[0]
                    target_result=None
                else:
                    source_result=None
                    target_result=results[0]
            else:
                if results[0].user_id==source_user.id:
                    source_result=results[0]
                    target_result=results[1]
                else:
                    source_result=results[1]
                    target_result=results[0]
                    
            now=datetime.utcnow()
            if source_result is None:
                daily_streak=0
                streak_text='I am happy you joined the sect too.'

                await connector.execute(CURRENCY_TABLE.insert().values(
                    user_id     = source_user.id,
                    total_love  = 0,
                    daily_next  = now+DAILY_INTERVAL,
                    daily_streak= 1,))
            else:
                daily_next=source_result.daily_next
                if daily_next>now:
                    embed=Embed(
                        'You already claimed your daily love for today~',
                        f'Come back in {elapsed_time(daily_next)}.',
                        GAMBLING_COLOR)
                    break
                daily_streak=source_result.daily_streak
                daily_next=daily_next+DAILY_STREAK_BREAK
                if daily_next<now:
                    daily_streak=daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
                    if daily_streak<0:
                        daily_streak=0
                    streak_text=f'You did not claim daily for more than 1 day, you got down to {daily_streak}.'
                else:
                    streak_text=f'You are in a {daily_streak} day streak! Keep up the good work!'
                
                await connector.execute(CURRENCY_TABLE.update().values(
                    daily_next  = now+DAILY_INTERVAL,
                    daily_streak= daily_streak+1,
                        ).where(currency_model.user_id==source_user.id))
                
            received=DAILY_REWARD+daily_streak*DAILY_STREAK_BONUS
            if received>DAILY_REWARD_LIMIT:
                received=DAILY_REWARD_LIMIT
            if target_result is None:
                await connector.execute(CURRENCY_TABLE.insert().values(
                    user_id     = target_user.id,
                    total_love  = received,
                    daily_next  = now,
                    daily_streak= 0,))

                total_love=received
            else:
                total_love=target_result.total_love+received

                await connector.execute(CURRENCY_TABLE.update().values(
                    total_love  = total_love,
                        ).where(currency_model.user_id==target_user.id))
            
            embed=Embed(
                f'Awww, you claimed your daily love for {target_user:f}, how sweet~',
                f'You gifted {received} {CURRENCY_EMOJI:e} and they have {total_love} {CURRENCY_EMOJI:e}\n{streak_text}',
                GAMBLING_COLOR)
            break
    
    await client.message_create(message.channel,embed=embed)

async def _help_daily(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('daily',(
        'Claim everyday your share of my love!\n'
        f'Usage: `{prefix}daily <user>`\n'
        'You can also gift your daily reward to your lovely imouto.'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('daily',_help_daily)

@gambling
@daily.shared(weight=1)
@ContentParser('user, flags=mni, default="message.author"')
async def hearts(client,message,target_user):
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==target_user.id))
        results = await response.fetchall()
    
    if results:
        total_love=results[0].total_love
    else:
        total_love=0

    if message.author is target_user:
        embed=Embed(
            f'You have {total_love} {CURRENCY_EMOJI:e}',
            '' if total_love else 'Awww, you seem so lonely..',
            GAMBLING_COLOR)
    else:
        embed=Embed(
            f'{target_user:f} has {total_love} {CURRENCY_EMOJI:e}',
            '' if total_love else 'Awww, they seem so lonely..',
            GAMBLING_COLOR)
        
    await client.message_create(message.channel,embed=embed)

async def _help_hearts(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('hearts',(
        'How many hearts do you have?\n'
        f'Usage: `{prefix}hearts <user>`\n'
        'You can also check other user\'s hearts too.'
            ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('hearts',_help_hearts)

def convert_tdelta(delta):
    result=[]
    rest=delta.days
    if rest:
        result.append(f'{rest} days')
    rest=delta.seconds
    amount=rest//3600
    if amount:
        result.append(f'{amount} hours')
        rest%=3600
    amount=rest//60
    if amount:
        result.append(f'{amount} minutes')
        rest%=60
    if rest:
        result.append(f'{rest} seconds')
    return ', '.join(result)

class heartevent_start_checker(object):
    __slots__=('client',)
    def __init__(self,client):
        self.client=client

    def __call__(self,emoji,user):
        return self.client.is_owner(user) and ((emoji is EVENT_OK_EMOJI) or (emoji is EVENT_ABORT_EMOJI))

@gambling
@ContentParser('condition, flags=r, default="not client.is_owner(message.author)"',
    'tdelta','int','int, default=0')
class heartevent(object):
    _update_time=60.
    _update_delta=timedelta(seconds=_update_time)
    
    __slots__=('amount', 'client', 'connector', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    async def __new__(cls,client,message,duration,amount,user_limit):
        self=object.__new__(cls)
        self.connector=None
        channel=message.channel
        while True:
            if duration>EVENT_MAX_DURATION:
                embed=Embed('Duration passed the upper limit\n',
                     f'**>**  upper limit : {convert_tdelta(EVENT_MAX_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif duration<EVENT_MIN_DURATION:
                embed=Embed('Duration passed the lower limit\n',
                     f'**>**  lower limit : {convert_tdelta(EVENT_MIN_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif amount>EVENT_HEART_MAX_AMOUNT:
                embed=Embed('Amount passed the upper limit\n',
                     f'**>**  upper limit : {EVENT_HEART_MAX_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif amount<EVENT_HEART_MIN_AMOUNT:
                embed=Embed('Amount passed the lower limit\n',
                     f'**>**  lower limit : {EVENT_HEART_MIN_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif user_limit<0:
                embed=Embed('User limit passed the lower limit\n',
                      '**>** lower limit : 0\n'
                     f'**>**  - passed : {user_limit}',
                      color=GAMBLING_COLOR)
            else:
                break

            to_delete = await client.message_create(channel,embed=embed)
            await sleep(30.,client.loop)
            try:
                await client.message_delete(to_delete)
                await client.message_delete(message)
            except DiscordException:
                pass
            return

        result=[]
        result.append('Duration: ')
        result.append(convert_tdelta(duration))
        result.append('\n Amount : ')
        result.append(str(amount))
        if user_limit:
            result.append('\n user limit : ')
            result.append(str(user_limit))

        embed=Embed('Is everything correct?',''.join(result),color=GAMBLING_COLOR)
        del result
        
        to_check = await client.message_create(channel,embed=embed)
        await client.reaction_add(to_check,EVENT_OK_EMOJI)
        await client.reaction_add(to_check,EVENT_ABORT_EMOJI)
        try:
            emoji,_ = await wait_for_reaction(client,to_check,heartevent_start_checker(client),1800.)
        except TimeoutError:
            return
        finally:
            try:
                await client.message_delete(to_check)
                await client.message_delete(message)
            except DiscordException:
                pass

        if emoji is EVENT_ABORT_EMOJI:
            return

        self.user_ids=set()
        self.user_limit=user_limit
        self.client=client
        self.duration=duration
        self.amount=amount
        self.waiter=Future(client.loop)
        
        self.connector = await DB_ENGINE.connect()
        
        message = await client.message_create(channel,embed=self.generate_embed())
        message.weakrefer()
        self.message=message
        client.events.reaction_add.append(self,message)
        Task(self.countdown(client,message),client.loop)
        await client.reaction_add(message,CURRENCY_EMOJI)
        return self
    
    def generate_embed(self):
        title=f'React with {CURRENCY_EMOJI:e} to receive {self.amount}'
        if self.user_limit:
            description=f'{convert_tdelta(self.duration)} left or {self.user_limit-len(self.user_ids)} users'
        else:
            description=f'{convert_tdelta(self.duration)} left'
        return Embed(title,description,color=GAMBLING_COLOR)

    async def __call__(self,client,emoji,user):
        if user.is_bot or (emoji is not CURRENCY_EMOJI):
            return
        
        user_id=user.id
        user_ids=self.user_ids
        
        old_ln=len(user_ids)
        user_ids.add(user_id)
        new_ln=len(user_ids)
        
        if new_ln==old_ln:
            return

        if new_ln==self.user_limit:
            self.duration=timedelta()
            self.waiter.set_result(None)
        
        connector=self.connector
        
        response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==user_id))
        results = await response.fetchall()
        if results:
            result=results[0]
            to_execute=CURRENCY_TABLE.update().values(
                total_love  = result.total_love+self.amount,
                    ).where(currency_model.user_id==user_id)
        else:
            to_execute=CURRENCY_TABLE.insert().values(
                user_id     = user_id,
                total_love  = self.amount,
                daily_next  = datetime.utcnow(),
                daily_streak= 0,)
        await connector.execute(to_execute)

    async def countdown(self,client,message):
        update_delta=self._update_delta
        loop=client.loop
        waiter=self.waiter

        sleep_time=(self.duration%update_delta).seconds
        if sleep_time:
            self.duration-=timedelta(seconds=sleep_time)
            loop.call_later(sleep_time,waiter.__class__.set_result_if_pending,waiter,None)
            await waiter
            waiter.clear()

        sleep_time=self._update_time
        while True:
            loop.call_later(sleep_time,waiter.__class__.set_result_if_pending,waiter,None)
            await waiter
            waiter.clear()
            self.duration-=update_delta
            if self.duration<update_delta:
                break
            try:
                await client.message_edit(message,embed=self.generate_embed())
            except DiscordException:
                break

        client.events.reaction_add.remove(self,message)
        try:
            await client.message_delete(message)
        except DiscordException:
            pass
        await self.connector.close()
        self.connector=None

    def __del__(self):
        connector=self.connector
        if connector is None:
            return
        Task(connector.close(),self.client.loop)
        self.connector=None

async def _help_heartevent(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('heartevent',(
        'Starts a heart event at the channel.\n'
        f'Usage: `{prefix}heartevent *duration* *amount* <users_limit>`\n'
        f'Min `duration`: {convert_tdelta(EVENT_MIN_DURATION)}\n'
        f'Max `duration`: {convert_tdelta(EVENT_MAX_DURATION)}\n'
        f'Min `amount`: {EVENT_HEART_MIN_AMOUNT}\n'
        f'Max `amount`: {EVENT_HEART_MAX_AMOUNT}\n'
        'If `user_imit` is not included, the event will have no user limit.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('heartevent',_help_heartevent,KOISHI_HELPER.check_is_owner)

@gambling
@ContentParser('condition, flags=r, default="not client.is_owner(message.author)"',
    'tdelta','int','int, default=0')
class dailyevent(object):
    _update_time=60.
    _update_delta=timedelta(seconds=_update_time)

    __slots__=('amount', 'client', 'connector', 'duration', 'message', 'user_ids', 'user_limit', 'waiter',)
    async def __new__(cls,client,message,duration,amount,user_limit):
        self=object.__new__(cls)
        self.connector=None
        channel=message.channel
        while True:
            if duration>EVENT_MAX_DURATION:
                embed=Embed('Duration passed the upper limit\n',
                     f'**>**  upper limit : {convert_tdelta(EVENT_MAX_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif duration<EVENT_MIN_DURATION:
                embed=Embed('Duration passed the lower limit\n',
                     f'**>**  lower limit : {convert_tdelta(EVENT_MIN_DURATION)}\n'
                     f'**>**  passed : {convert_tdelta(duration)}',
                      color=GAMBLING_COLOR)
            elif amount>EVENT_DAILY_MAX_AMOUNT:
                embed=Embed('Amount passed the upper limit\n',
                     f'**>**  upper limit : {EVENT_DAILY_MAX_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif amount<EVENT_DAILY_MIN_AMOUNT:
                embed=Embed('Amount passed the lower limit\n',
                     f'**>**  lower limit : {EVENT_DAILY_MIN_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif user_limit<0:
                embed=Embed('User limit passed the lower limit\n',
                      '**>** lower limit : 0\n'
                     f'**>**  - passed : {user_limit}',
                      color=GAMBLING_COLOR)
            else:
                break

            to_delete = await client.message_create(channel,embed=embed)
            await sleep(30.,client.loop)
            try:
                await client.message_delete(to_delete)
                await client.message_delete(message)
            except DiscordException:
                pass
            return

        result=[]
        result.append('Duration: ')
        result.append(convert_tdelta(duration))
        result.append('\n Amount : ')
        result.append(str(amount))
        if user_limit:
            result.append('\n user limit : ')
            result.append(str(user_limit))

        embed=Embed('Is everything correct?',''.join(result),color=GAMBLING_COLOR)
        del result

        to_check = await client.message_create(channel,embed=embed)
        await client.reaction_add(to_check,EVENT_OK_EMOJI)
        await client.reaction_add(to_check,EVENT_ABORT_EMOJI)
        try:
            emoji,_ = await wait_for_reaction(client,to_check,heartevent_start_checker(client),1800.)
        except TimeoutError:
            return
        finally:
            try:
                await client.message_delete(to_check)
                await client.message_delete(message)
            except DiscordException:
                pass

        if emoji is EVENT_ABORT_EMOJI:
            return

        self.user_ids=set()
        self.user_limit=user_limit
        self.client=client
        self.duration=duration
        self.amount=amount
        self.waiter=Future(client.loop)

        self.connector = await DB_ENGINE.connect()

        message = await client.message_create(channel,embed=self.generate_embed())
        message.weakrefer()
        self.message=message
        client.events.reaction_add.append(self,message)
        Task(self.countdown(client,message),client.loop)
        await client.reaction_add(message,CURRENCY_EMOJI)
        return self

    def generate_embed(self):
        title=f'React with {CURRENCY_EMOJI:e} to increase your daily streak by {self.amount}'
        if self.user_limit:
            description=f'{convert_tdelta(self.duration)} left or {self.user_limit-len(self.user_ids)} users'
        else:
            description=f'{convert_tdelta(self.duration)} left'
        return Embed(title,description,color=GAMBLING_COLOR)

    async def __call__(self,client,emoji,user):
        if user.is_bot or (emoji is not CURRENCY_EMOJI):
            return

        user_id=user.id
        user_ids=self.user_ids

        old_ln=len(user_ids)
        user_ids.add(user_id)
        new_ln=len(user_ids)

        if new_ln==old_ln:
            return

        if new_ln==self.user_limit:
            self.duration=timedelta()
            self.waiter.set_result(None)

        connector=self.connector

        response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==user_id))
        results = await response.fetchall()
        if results:
            result=results[0]
            now=datetime.utcnow()
            daily_next=result.daily_next+DAILY_STREAK_BREAK
            if daily_next>now:
                to_execute=CURRENCY_TABLE.update().values(
                    daily_streak  = result.daily_streak+self.amount,
                        ).where(currency_model.user_id==user_id)
            else:
                daily_streak=result.daily_streak-((now-daily_next)//DAILY_STREAK_LOSE)-1
                if daily_streak<0:
                    daily_streak=self.amount
                else:
                    daily_streak=daily_streak+self.amount

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

    async def countdown(self,client,message):
        update_delta=self._update_delta
        loop=client.loop
        waiter=self.waiter
        
        sleep_time=(self.duration%update_delta).seconds
        if sleep_time:
            self.duration-=timedelta(seconds=sleep_time)
            loop.call_later(sleep_time,waiter.__class__.set_result_if_pending,waiter,None)
            await waiter
            waiter.clear()

        sleep_time=self._update_time
        while True:
            loop.call_later(sleep_time,waiter.__class__.set_result_if_pending,waiter,None)
            await waiter
            waiter.clear()
            self.duration-=update_delta
            if self.duration<update_delta:
                break
            try:
                await client.message_edit(message,embed=self.generate_embed())
            except DiscordException:
                break

        client.events.reaction_add.remove(self,message)
        try:
            await client.message_delete(message)
        except DiscordException:
            pass
        await self.connector.close()
        self.connector=None

    def __del__(self):
        connector=self.connector
        if connector is None:
            return
        Task(connector.close(),self.client.loop)
        self.connector=None

async def _help_dailyevent(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('dailyevent',(
        'Starts a daily event at the channel.\n'
        f'Usage: `{prefix}dailyevent *duration* *amount* <users_limit>`\n'
        f'Min `duration`: {convert_tdelta(EVENT_MIN_DURATION)}\n'
        f'Max `duration`: {convert_tdelta(EVENT_MAX_DURATION)}\n'
        f'Min `amount`: {EVENT_DAILY_MIN_AMOUNT}\n'
        f'Max `amount`: {EVENT_DAILY_MAX_AMOUNT}\n'
        'If `user_imit` is not included, the event will have no user limit.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('dailyevent',_help_dailyevent,KOISHI_HELPER.check_is_owner)

@gambling(case='21')
@ContentParser('int, default=0')
class _21(object):
    NEW     = BUILTIN_EMOJIS['new']
    STOP    = BUILTIN_EMOJIS['octagonal_sign']
    EMOJIS  = (NEW,STOP)
    
    __slots__ = ('all_pulled', 'amount', 'canceller', 'channel', 'client',
        'client_applied', 'client_hand', 'message', 'task_flag', 'timeouter',
        'user', 'user_ace', 'user_hand', 'user_total')
    
    def pull_card(all_pulled):
        card = int((DECK_SIZE-len(all_pulled))*random())
        for pulled in all_pulled:
            if pulled>card:
                break
            
            card=card+1
            continue
        
        all_pulled.append(card)
        all_pulled.sort()
        
        return card
    
    async def __new__(cls,client,source_message,amount):
        user=source_message.author
        channel=source_message.channel
        
        while True:
            if user.id in IN_GAME_IDS:
                error_msg=f'You are already at a game.'
                break
            
            if amount < BET_MIN:
                error_msg=f'You must bet at least {BET_MIN} {CURRENCY_EMOJI.as_emoji}'
                break
        
            if not channel.cached_permissions_for(client).can_add_reactions:
                error_msg='I cannot start this command here, not enough permissions provided.'
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
            
            error_msg=None
            break
        
        if (error_msg is not None):
            await client.message_create(channel,
                embed=Embed(error_msg,color=GAMBLING_COLOR))
            return None
        
        IN_GAME_IDS.add(user.id)
        
        all_pulled  = []
        
        user_hand   = []
        user_total  = 0
        user_ace    = 0
        
        client_hand = []
        client_total= 0
        client_ace  = 0
        
        while True:
            card = cls.pull_card(all_pulled)
            
            client_hand.append(card)
            
            number_index=card%len(CARD_NUMBERS)
            if number_index==ACE_INDEX:
                client_ace+=1
                card_weight=1
            elif number_index>7:
                card_weight=10
            else:
                card_weight=number_index+2
            client_total+=card_weight
            
            client_applied = client_total
            free_ace = client_ace
            while free_ace:
                if client_applied>13:
                    break
                
                client_applied=client_applied+9
                free_ace=free_ace-1
                continue
            
            if free_ace:
                if client_applied>17:
                    break
                continue
            
            if client_applied>15:
                break
            
            continue
        
        
        for _ in range(2):
            card = cls.pull_card(all_pulled)
            
            user_hand.append(card)
            
            number_index=card%len(CARD_NUMBERS)
            if number_index==ACE_INDEX:
                user_ace+=1
                card_weight=1
            elif number_index>7:
                card_weight=10
            else:
                card_weight=number_index+2
            user_total+=card_weight
        
        applied=user_total+user_ace*9
        embed=Embed(f'How to lose {amount} {CURRENCY_EMOJI.as_emoji}',
            f'You have cards equal to {applied} weight at your hand',
            color=GAMBLING_COLOR)
        
        for round_,card in enumerate(user_hand,1):
            type_index, number_index = divmod(card,len(CARD_NUMBERS))
            embed.add_field(f'Round {round_}',
                f'You pulled {CARD_TYPES[type_index]} {CARD_NUMBERS[number_index]}')
        
        try:
            message = await client.message_create(channel,embed=embed)
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
                    to_execute=CURRENCY_TABLE.update().values(
                        total_love  = total_love,
                            ).where(currency_model.user_id==user.id)
                else:
                    to_execute=CURRENCY_TABLE.insert().values(
                        user_id     = user.id,
                        total_love  = amount,
                        daily_next  = datetime.utcnow(),
                        daily_streak= 0,)
                
                await connector.execute(to_execute)
            
            if isinstance(err,(DiscordException, ConnectionError)):
                return
            raise
        
        message.weakrefer()
        
        self=object.__new__(cls)
        self.client=client
        self.channel=channel
        self.canceller=cls._canceller
        self.task_flag=GUI_STATE_READY
        self.message=message
        self.user=user
        self.amount=amount
        self.all_pulled=all_pulled
        self.user_hand=user_hand
        self.user_total=user_total
        self.user_ace=user_ace
        self.client_hand=client_hand
        self.client_applied=client_applied
        self.timeouter=Timeouter(client.loop,self,timeout=300.)
        client.events.reaction_add.append(self,message)
        client.events.reaction_delete.append(self,message)
        return self
    
    async def __call__(self,client,emoji,user):
        if user!=self.user or emoji not in self.EMOJIS:
            return
        
        message=self.message
        
        if self.channel.cached_permissions_for(client).can_manage_messages:
            if not message.did_react(emoji,user):
                return
            
            task = Task(client.reaction_delete(message,emoji,user),client.loop)
            if __debug__:
                task.__silence__()
        
        task_flag=self.task_flag
        if task_flag!=GUI_STATE_READY:
            if task_flag==GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self.task_flag=GUI_STATE_CANCELLING
                return

            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
            
        if emoji is self.NEW:
            # It is enough to delete the reaction at this ase if needed,
            # because after the other cases we will delete them anyways.
            card = type(self).pull_card(self.all_pulled)
            
            self.user_hand.append(card)
            
            number_index=card%len(CARD_NUMBERS)
            if number_index==ACE_INDEX:
                self.user_ace+=1
                card_weight=1
            elif number_index>7:
                card_weight=10
            else:
                card_weight=number_index+2
                
            user_total=self.user_total
            user_total+=card_weight
            self.user_total=user_total
            
            game_ended = (user_total>21)
            
        elif emoji is self.STOP:
            game_ended=True
        
        else:
            # should not happen
            return
        
        if game_ended:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            
            user_applied = self.user_total
            free_ace = self.user_ace
            while free_ace:
                if user_applied>13:
                    break
                
                user_applied=user_applied+9
                free_ace=free_ace-1
                continue
            
            client_applied=self.client_applied
            
            if client_applied>21:
                if user_applied>21:
                    winner=None
                else:
                    winner=user
            else:
                if user_applied>21:
                    winner=client
                else:
                    if client_applied>user_applied:
                        winner=client
                    elif client_applied<user_applied:
                        winner=user
                    else:
                        winner=None
            
            if (winner is not client):
                if winner is None:
                    bonus=self.amount
                else:
                    bonus=self.amount*2
                    
                async with DB_ENGINE.connect() as connector:
                    response = await connector.execute(CURRENCY_TABLE.select(currency_model.user_id==user.id))
                    results = await response.fetchall()

                    if results:
                        total_love = results[0].total_love
                        
                        to_execute=CURRENCY_TABLE.update().values(
                            total_love  = total_love+bonus,
                                ).where(currency_model.user_id==user.id)
                    else:
                        to_execute=CURRENCY_TABLE.insert().values(
                            user_id     = user.id,
                            total_love  = bonus,
                            daily_next  = datetime.utcnow(),
                            daily_streak= 0,)
                    
                    await connector.execute(to_execute)
                    
            if winner is None:
                title=f'How to draw.'
            elif winner is client:
                title=f'How to lose {self.amount} {CURRENCY_EMOJI.as_emoji}'
            else:
                title=f'How to win {self.amount} {CURRENCY_EMOJI.as_emoji}'
            
            embed=Embed(title,color=GAMBLING_COLOR)
            
            field_content=[]
            
            for round_,card in enumerate(self.user_hand,1):
                type_index, number_index = divmod(card,len(CARD_NUMBERS))
                field_content.append('Round ')
                field_content.append(str(round_))
                field_content.append(': ')
                field_content.append(CARD_TYPES[type_index])
                field_content.append(' ')
                field_content.append(CARD_NUMBERS[number_index])
                field_content.append('\n')
                
            embed.add_field(f'{user.name_at(message.guild)}\'s cards\' weight: {user_applied}',
                ''.join(field_content))
            field_content.clear()
            
            for round_,card in enumerate(self.client_hand,1):
                type_index, number_index = divmod(card,len(CARD_NUMBERS))
                field_content.append('Round ')
                field_content.append(str(round_))
                field_content.append(': ')
                field_content.append(CARD_TYPES[type_index])
                field_content.append(' ')
                field_content.append(CARD_NUMBERS[number_index])
                field_content.append('\n')
            
            embed.add_field(f'{client.name_at(message.guild)}\'s cards\' weight: {client_applied}',
                ''.join(field_content))
            field_content=None
            
            try:
                await client.message_edit(message,embed=embed)
            except BaseException as err:
                if isinstance(err,(DiscordException, ConnectionError)):
                    return
                raise
            
        else:
            applied = user_total
            free_ace = self.user_ace
            while free_ace:
                if applied>13:
                    break
                
                applied=applied+9
                free_ace=free_ace-1
                continue
            
            embed=Embed(f'How to lose {self.amount} {CURRENCY_EMOJI.as_emoji}',
                f'You have cards equal to {applied} weight at your hand',
                color=GAMBLING_COLOR)
            
            for round_,card in enumerate(self.user_hand,1):
                type_index, number_index = divmod(card,len(CARD_NUMBERS))
                embed.add_field(f'Round {round_}',
                    f'You pulled {CARD_TYPES[type_index]} {CARD_NUMBERS[number_index]}')
            
            self.task_flag=GUI_STATE_SWITCHING_PAGE
            
            try:
                await client.message_edit(message,embed=embed)
            except BaseException as err:
                self.task_flag=GUI_STATE_CANCELLED
                self.cancel()
                if isinstance(err,(DiscordException, ConnectionError)):
                    return
                raise
                
            self.task_flag=GUI_STATE_READY
            self.timeouter.set_timeout(300.0)
        
    async def _canceller(self,exception,):
        IN_GAME_IDS.remove(self.user.id)
        
        client=self.client
        message=self.message
        
        client.events.reaction_add.remove(self,message)
        client.events.reaction_delete.remove(self,message)
        
        if self.task_flag==GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return

        self.task_flag=GUI_STATE_CANCELLED

        if self.channel.cached_permissions_for(client).can_manage_messages:
            task = Task(client.reaction_clear(message),client.loop)
            if __debug__:
                task.__silence__()
                
        if exception is None:
            return
        
        if isinstance(exception,TimeoutError):
            IN_GAME_IDS.remove(self.user.id)
            
            embed=Embed(f'Timeout occured, you lost your {self.amount} {CURRENCY_EMOJI.as_emoji} forever.')
            
            try:
                await client.message_edit(message,embed=embed)
            except (DiscordException, ConnectionError):
                return
            
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self,exception=None):
        canceller=self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,exception),self.client.loop)
    
async def _help_21(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('21',(
        'Starts a 21 game at the channel.\n'
        f'Usage: `{prefix}21 *amount*`\n'
        'Your chalange is to collect cards with weight up to 21. Each card '
        'with number 2-10 has the same weight as their number says, meanwhile '
        'J, Q and K has fix weight of 10. Ace has weight of 10, but if You '
        'whould pass 21, it loses 9 of it.\n'
        'At this game you are fighting me, so if we boss lose, it is a draw.\n'
        'You start with 2 cards initially drawed and at every round, you have '
        'option to draw a new card, or to stop.'),
            color=KOISHI_HELP_COLOR)
    
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('21',_help_21)

del Emoji, Color, Cooldown, ContentParser, eventlist, CooldownHandler
