# -*- coding: utf-8 -*-
from datetime import datetime,timedelta

from hata.parsers import eventlist
from hata.events_compiler import ContentParser
from hata.others import elapsed_time
from hata.events import Cooldown, wait_for_reaction
from hata.embed import Embed
from hata.color import Color
from hata.emoji import Emoji, BUILTIN_EMOJIS
from hata.exceptions import DiscordException
from hata.futures import sleep,Task,Future

from models import DB_ENGINE,currency_model,CURRENCY_TABLE
from tools import CooldownHandler

GAMBLING_COLOR=Color.from_rgb(254,254,164)
CURRENCY_EMOJI=Emoji.precreate(603533301516599296)
DAILY_INTERVAL=timedelta(hours=22)
DAILY_STREAK_BREAK=timedelta(hours=26)
DAILY_STREAK_LOSE=timedelta(hours=12)
DAILY_REWARD=100
DAILY_STREAK_BONUS=5
DAILY_REWARD_LIMIT=300

EVENT_MAX_DURATION=timedelta(hours=24)
EVENT_MIN_DURATION=timedelta(minutes=30)
EVENT_MIN_AMOUNT=DAILY_REWARD//2 #half day of min
EVENT_MAX_AMOUNT=7*DAILY_REWARD_LIMIT #1 week of max
EVENT_OK_EMOJI=BUILTIN_EMOJIS['ok_hand']
EVENT_ABORT_EMOJI=BUILTIN_EMOJIS['x']

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

class heartevent_start_checker:
    __slots__=['client']
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
    
    __slots__=['amount', 'client', 'connector', 'duration', 'message', 'user_ids', 'user_limit', 'waiter']
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
            elif amount>EVENT_MAX_AMOUNT:
                embed=Embed('Amount passed the upper limit\n',
                     f'**>**  upper limit : {EVENT_MAX_AMOUNT}\n'
                     f'**>**  passed : {amount}',
                      color=GAMBLING_COLOR)
            elif amount<EVENT_MIN_AMOUNT:
                embed=Embed('Amount passed the lower limit\n',
                     f'**>**  lower limit : {EVENT_MIN_AMOUNT}\n'
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
        result.append(amount.__str__())
        if user_limit:
            result.append('\n user limit : ')
            result.append(user_limit.__str__())

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

    async def __call__(self,emoji,user):
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
            to_execute=CURRENCY_TABLE.update().values(
                total_love  = results[0].total_love+self.amount,
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
        self.waiter=waiter=Future(self.client.loop)

        sleep_time=(self.duration%update_delta).seconds
        if sleep_time:
            self.duration-=timedelta(seconds=sleep_time)
            await waiter.sleep(sleep_time)
            waiter.clear()

        sleep_time=self._update_time
        while True:
            await waiter.sleep(sleep_time)
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

del Emoji, Color, Cooldown, ContentParser, eventlist, CooldownHandler
