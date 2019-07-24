# -*- coding: utf-8 -*-
from datetime import datetime,timedelta

from hata.parsers import eventlist
from hata.events_compiler import content_parser
from hata.others import elapsed_time
from hata.events import cooldown
from hata.embed import Embed
from hata.color import Color
from hata.emoji import Emoji

from models import DB_ENGINE,currency_model,CURRENCY_TABLE
from tools import cooldown_handler

GAMBLING_COLOR=Color.from_rgb(254,254,164)
CURRENCY_EMOJI=Emoji.precreate(603533301516599296)
DAILY_INTERVAL=timedelta(hours=22)
DAILY_STREAK_BREAK=timedelta(hours=26)
DAILY_REWARD=100
DAILY_STREAK_BONUS=10

gambling=eventlist()

@gambling
@cooldown(30.,'user',handler=cooldown_handler())
@content_parser('user, flags=mni, default="message.author"')
async def daily(client,message,target_user):
    source_user=message.author
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
                    
                    if daily_next+DAILY_STREAK_BREAK<now:
                        daily_streak=0
                        streak_text='You did not claim daily for more than 1 day, so your streak broke :c'
                    else:
                        daily_streak=source_result.daily_streak
                        streak_text=f'You are in a {daily_streak} day streak! Keep up the good work!'
                    
                    received=DAILY_REWARD+daily_streak*DAILY_STREAK_BONUS
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
                
                if daily_next+DAILY_STREAK_BREAK<now:
                    daily_streak=0
                    streak_text='You did not claim daily for more than 1 day, so your streak broke :c'
                else:
                    daily_streak=source_result.daily_streak
                    streak_text=f'You are in a {daily_streak} day streak! Keep up the good work!'
                
                await connector.execute(CURRENCY_TABLE.update().values(
                    user_id     = source_user.id,
                    total_love  = 0,
                    daily_streak= daily_streak,
                        ).where(currency_model.user_id==source_user.id))
                
            received=DAILY_REWARD+daily_streak*DAILY_STREAK_BONUS

            if target_result is None:
                await connector.execute(CURRENCY_TABLE.insert().values(
                    user_id     = target_user.id,
                    total_love  = received,
                    daily_next  = now,
                    daily_streak= 0,))

                total_love=received
            else:
                total_love=target_result.total_love+received

                await connector.execute(CURRENCY_TABLE.insert().update(
                    total_love  = total_love,
                        ).where(currency_model.user_id==target_user.id))
            
            embed=Embed(
                f'Awww, you claimed your daily love for {target_user:f}, how sweet~',
                f'You gifted {received} {CURRENCY_EMOJI:e} and they have {total_love} {CURRENCY_EMOJI:e}\n{streak_text}',
                GAMBLING_COLOR)
            break
    
    await client.message_create(message.channel,embed=embed)

        
@gambling
@cooldown(20.,'user',handler=cooldown_handler())
@content_parser('user, flags=mni, default="message.author"')
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
