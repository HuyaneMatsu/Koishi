# -*- coding: utf-8 -*-
import sys
from random import randint
import os
import re
import time
import json
#import pickle
#moving to the outer folder, so hata ll count as a package
sys.path.append(os.path.abspath('..'))
from collections import deque
from datetime import timedelta
import traceback

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup=None
    
from hata import Client,start_clients
from hata.exceptions import Forbidden,HTTPException
from hata.emoji import BUILTIN_EMOJIS,parse_emoji
from hata.activity import activity_game
from hata.others import (filter_content,from_json,to_json,
    parse_oauth2_redirect_url,cchunkify)
from hata.channel import cr_pg_channel_object,Channel_text,Channel_private,Message_iterator
from hata.embed import Embed,Embed_field,Embed_footer
from hata.events import (
    pagination,bot_reaction_waitfor,bot_message_event,wait_for_message,
    wait_for_emoji,prefix_by_guild,bot_reaction_delete_waitfor,cooldown,
    waitfor_wrapper)
from hata.futures import CancelledError,sleep
from hata.prettyprint import pchunkify
from hata.user import USERS
from hata.client_core import KOKORO,stop_clients,CLIENTS
from hata.oauth2 import SCOPES
from hata.events_compiler import content_parser
from hata.webhook import Webhook
from hata.role import Role

from image_handler import on_command_upload,on_command_image
from help_handler import on_command_help,HELP,invalid_command
from pers_data import TOKEN,PREFIX,TOKEN2,CLIENT_SECRET
from infos import infos,update_about
from voice import voice
from battleships import battle_manager
from dispatch_tests import dispatch_tester
from ratelimit_tests import ratelimit_commands
from kanako import kanako_manager
from dungeon_sweeper import ds_manager

def smart_join(list_,limit):
    limit-=4
    result=[]
    for value in list_:
        limit-=(len(value)+1)
        if limit<0:
            break
        result.append(value)
    result.append('...')
    return ' '.join(result)

class cooldown_handler:
    __slots__=['cache']
    def __init__(self):
        self.cache={}
    async def __call__(self,client,message,command,time_left):
        id_=message.author.id
        try:
            notification,waiter=self.cache[id_]
            if notification.channel is message.channel:
                await client.message_edit(notification,f'**{message.author:f}** please cool down, {int(time_left)} seconds left!')
                return
            waiter.cancel()
        except KeyError:
            pass
        notification = await client.message_create(message.channel,f'**{message.author:f}** please cool down, {int(time_left)} seconds left!')
        waiter=client.loop.create_task(self.waiter(client,id_,notification))
        self.cache[id_]=(notification,waiter)
    async def waiter(self,client,id_,notification):
        try:
            await sleep(30.,client.loop)
        except CancelledError:
            pass
        del self.cache[id_]
        try:
            await client.message_delete(notification)
        except (Forbidden,HTTPException):
            pass

PREFIX_FILENAME='prefixes.json'
try:
    with open(PREFIX_FILENAME,'r') as file:
        PREFIXES=prefix_by_guild.from_json_serialization(json.load(file))
except (FileNotFoundError,OSError,PermissionError,json.decoder.JSONDecodeError):
    PREFIXES=prefix_by_guild(PREFIX)

##PREFIX_FILENAME='prefixes.pcl'
##try:
##    with open(PREFIX_FILENAME,'rb') as file:
##        PREFIXES=pickle.load(file)
##except (FileNotFoundError,OSError,PermissionError,pickle.UnpicklingError):
##    PREFIXES=prefix_by_guild(PREFIX)
    
Koishi=Client(TOKEN,CLIENT_SECRET,loop=1)
Koishi.activity=activity_game.create(name='with Satori')

Mokou=Client(TOKEN2,loop=2)

TYPINGS={}
class typing_counter:
    __slots__=['duration', 'timestamp', 'user']
    def __init__(self,user,timestamp):
        self.user=user
        self.timestamp=timestamp
        self.duration=8.

@Mokou.events
async def message_create(client,message):
    while True:
        channel=message.channel
        if type(channel) is Channel_private:
            break
        
        user=message.author
        if user.is_bot:
            break
        
        try:
            channel_q=TYPINGS[channel.id]
        except KeyError:
            TYPINGS[channel.id]=deque()
            break
        ln=len(channel_q)
        if not ln:
            break
        
        timestamp=message.created_at
        limit=timestamp-timedelta(seconds=8)
        index=0
        while True:
            element=channel_q[index]
            if element.timestamp<limit:
                break
            if element.user is user:
                #we dont actually look the corect time, so lets just put there a 0.
                element.duration=0. #(timestamp-element.timestamp).total_seconds() 
                break
            index+=1
            if index==ln:
                break
            
        break
    
    while True:
        content=message.content.lower()
        if 'show' in content and 'amount of loaded messages' in content:
            channel=message.channel
            parts=[f'Amount of loaded messages: {len(channel.messages)}.']
            if channel.message_history_reached_end:
                parts.append('The channel is fully loaded.')
            else:
                parts.append('There is even more message at this channel however.')
            if not channel.permissions_for(client).can_read_message_history:
                parts.append('I have no permission to read older messages.')
            if channel.turn_GC_on_at:
                now=time.time()
                if now>channel.turn_GC_on_at:
                    parts.append('The GC will check the channel at the next cycle.')
                else:
                    parts.append(f'The channel will fall under GC after {round(channel.turn_GC_on_at-now)} seconds')
            else:
                parts.append('There is no reason to run GC on this channel.')
            if channel.messages.maxlen:
                parts.append(f'The lenght of the loaded messages at this channel is limited to: {channel.messages.maxlen}')
            else:
                parts.append('The amount of messages kept from this channel is unlimited right now')
                
            text='\n'.join(parts)
            break
        else:
            if randint(0,2):
                text=''
                break
            if 'fire' in content and re.match(r'\b(i|u|you|we|iam)\b',content):
                text='BURN!!!'
            elif re.match(r'(\b|[^\s\d])(moko[u]{0,1})\b',content):
                text='Yes, its me..'
            else:
                text=''
            break
    if text:    
        await client.message_create(message.channel,text)

@Mokou.events
async def typing(self,channel,user,timestamp):
    if type(channel) is Channel_private:
        return
    
    try:
        channel_q=TYPINGS[channel.id]
    except KeyError:
        channel_q=TYPINGS[channel.id]=deque()
        channel_q.appendleft(typing_counter(user,timestamp),)
        return
    index=len(channel_q)
    if not index:
        channel_q.appendleft(typing_counter(user,timestamp),)
        return
    limit=timestamp-timedelta(seconds=34)
    
    while True:
        index-=1
        if channel_q[index].timestamp<limit:
            del channel_q[index]
            if index:
                continue
            channel_q.appendleft(typing_counter(user,timestamp),)
            return
        break
    
    found=0
    while index:
        element=channel_q[index]
        if element.user is user:
            if element.duration!=8.:
                channel_q.appendleft(typing_counter(user,timestamp),)
                return
            found+=1
            if found==3:
                break
        index-=1
    
    if found!=3 or found==len(channel_q):
        channel_q.appendleft(typing_counter(user,timestamp),)
        return
    
    channel_q.clear()
    await self.message_create(channel,f'**{user.name_at(channel.guild)}** is typing...')

@Mokou.events
async def channel_delete(self,channel):
    try:
        del TYPINGS[channel.id]
    except KeyError:
        pass

class commit_extractor:
    __slots__=['client', 'color', 'role', 'target', 'webhook']
    def __init__(self,client,target,webhook,role=None,color=0):
        self.client=client
        self.target=target
        self.webhook=webhook
        self.role=role
        self.color=color

    async def __call__(self,args):
        message=args[0]
        webhook=self.webhook
        client=self.client

        if message.author!=webhook or message.author.name!='GitHub':
            return
        
        embed=message.embeds[0]

        if ':master' not in embed.title:
            return

        result = await client.download_url(embed.url)
        soup=BeautifulSoup(result,'html.parser',from_encoding='utf-8')
        
        description_container=soup.find(class_='commit-desc')
        if description_container is None:
            return
        
        title_container=soup.find(class_='commit-title')

        if webhook.partial:
            await client.webhook_update(webhook)

        guild=webhook.guild
        
        if self.role is None:
            result_content=''
            needs_unlock=False
        else:
            result_content=self.role.mention
            needs_unlock = (not self.role.mentionable) and guild.permissions_for(Koishi).can_manage_roles
            
        result_embed=Embed(
            title       = title_container.getText('\n'),
            description = description_container.getText('\n'),
            color       = self.color,
            url         = embed.url,
                )
        
        webhook_name = embed.author.name
        webhook_avatar_url = embed.author.proxy_icon
        
        if needs_unlock:
            try:
                await Koishi.role_edit(self.role,mentionable=True)
                await sleep(0.5,client.loop)
                await client.webhook_send(webhook,
                    result_content,
                    result_embed,
                    name=webhook_name,
                    avatar_url=webhook_avatar_url
                        )
                await sleep(0.5,client.loop)
            finally:
                await Koishi.role_edit(self.role,mentionable=False)

        else:
            await client.webhook_send(webhook,
                result_content,
                result_embed,
                name=webhook_name,
                avatar_url=webhook_avatar_url
                    )
        

@Koishi.events
async def ready(client):
    print(f'{client:f} ({client.id}) logged in')
    await client.update_application_info()
    print(f'owner: {client.owner:f} ({client.owner.id})')
    update_about(client)
    
Koishi.events(bot_reaction_waitfor())
Koishi.events(bot_reaction_delete_waitfor())


with Koishi.events(bot_message_event(PREFIXES)) as on_command:
    
    Koishi.events.message_create.append(
        commit_extractor(
            Koishi,
            Channel_text.precreate(555476090382974999),
            Webhook.precreate(555476334210580508),
            role=Role.precreate(538397994421190657),
            color=0x2ad300,
                ))
        
    on_command(dispatch_tester.here)
    on_command(dispatch_tester.switch)
    on_command.extend(infos)
    on_command(voice)
    on_command(on_command_image,'image')
    on_command(on_command_upload,'upload')
    on_command(on_command_help,'help')
    on_command(invalid_command)
    on_command.extend(ratelimit_commands)
    on_command(battle_manager,case='bs')
    on_command(kanako_manager,'kanako')
    on_command(ds_manager,'ds')
    
    @on_command
    async def default_event(client,message):
        content=message.content
        text=None
        if re.match(r'n+\s*o+\s*u+',content,re.IGNORECASE) is not None:
            parts=[]
            for value in 'nou':
                emoji=BUILTIN_EMOJIS[f'regional_indicator_{value}']
                await client.reaction_add(message,emoji)
                    
        elif len(content)==3:
            if re.match(r'^owo$',content,re.IGNORECASE):
                text='OwO'
            elif re.match(r'^uwu$',content,re.IGNORECASE):
                text='UwU'
            elif re.match(r'^0w0$',content,re.IGNORECASE):
                text='0w0'
        
        if text:
            await client.message_create(message.channel,text)

    @on_command
    @content_parser('user, flags=mna, default="message.author"')
    async def rate(client,message,target):
        #nickname check
        if target in CLIENTS or target is client.owner:
            result=10
        else:
            result=target.id%11

        await client.message_create(message.channel,f'I rate {target.name_at(message.guild)} {result}/10')


    @on_command
    async def dice(client,message,content):
        search_result=re.match(r'([0-9]+).*',content)
        if search_result:
            times=int(search_result.groups()[0])
        else:
            times=1

        if times==0:
            text='0 KEK'
        elif times>6:
            text='I have only 6 dices, sorry, no money for more. Sadpanda'
        else:
            result=0
            for x in range(times):
                result+=randint(1,6)
                
            if result<=2.5*times:
                luck_text=', better luck next time!'
            elif result>=5.5*times:
                luck_text=', so BIG,.. thats what she said... *cough*'
            else:
                luck_text=''
            text=f'Rolled {result} {luck_text}'
            
        await client.message_create(message.channel,text)


    @on_command
    async def mention_event(client,message):
        m1=message.author.mention_at(message.guild)
        m2=client.mention_at(message.guild)
        replace={re.escape(m1):m2,re.escape(m2):m1}
        pattern=re.compile("|".join(replace.keys()))
        result=pattern.sub(lambda x: replace[re.escape(x.group(0))],message.content)
        await client.message_create(message.channel,result)

    
    @on_command
    @cooldown(30.,'user',handler=cooldown_handler())
    async def ping(client,message,content):
        kokoro=client.websocket.kokoro
        if kokoro is None:
            text='Disconnecting'
        else:
            text=f'{int(kokoro.latency*1000.)} ms'
        await client.message_create(message.channel,text)
                              
    @on_command.add('emoji')
    async def emoji_command(client,message,content):
        guild=message.guild
        if guild is None:
            return
        
        try:
            await client.message_delete(message,reason='Used emoji command')
        except Forbidden:
            pass
        
        emoji=guild.get_emoji(content)
        if emoji:
            await client.message_create(message.channel,str(emoji))

    @on_command
    async def message_me(client,message,content):
        channel = await client.channel_private_create(message.author)
        try:
            await client.message_create(channel,'Love you!')
        except Forbidden:
            await client.message_create(message.channel,'Pls turn on private messages from this server!')

    @on_command
    async def clear(client,message,content):
        guild=message.guild
        if guild is None:
            return
        
        if not guild.permissions_for(message.author).can_administrator:
            return
            
        channel=message.channel
        author=message.author
        content=filter_content(content)
        
        if not content:
            limit=100
        elif content[0].isdigit():
            limit=int(content[0])
            if limit<=0:
                return
        else:
            await client.message_create(channel,'Excepted int or nothing.')
            return
            
        messages=[]
        async for message in Message_iterator(client,message.channel):
            messages.append(message)
            limit-=1
            if limit:
                continue
            break

        await client.message_delete_multiple(messages,reason=f'Called by {author:f}')

    MAGIC_PATTERN=re.compile('.*?(p[lw][sz]|p[lw]ea[sz]e|desu|kudasai)[\.\!]*?',re.I)


    @on_command
    async def waitemoji(client,message,content):
        channel=message.channel
        
        message_to_delete = await client.message_create(channel,'Waiting!')
        
        try:
            _,emoji = await wait_for_message(client,channel,lambda message:parse_emoji(message.content),30.)
        except TimeoutError:
            return
        finally:
            try:
                await client.message_delete(message_to_delete)
            except Forbidden:
                pass
            
        await client.message_create(channel,str(emoji)*5)

    @on_command
    async def subscribe(client,message,content):
        guild=message.guild
        if guild is None:
            return
        role=guild.get_role('Announcements')
        if role is None:
            return
        if role in message.author.guild_profiles[guild].roles:
            await client.user_role_delete(message.author,role)
            text='You succesfully unsubscribed'
        else:
            await client.user_role_add(message.author,role)
            text='You succesfully subscribed'
        await client.message_create(message.channel,text)

    @on_command
    async def invite(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_create_instant_invite:
            return

        if message.author is guild.owner and content=='perma':
            max_age=0
            max_use=0
        else:
            max_age=21600
            max_use=1
        
        try:
            invite = await client.invite_create_pref(guild,max_age,max_use)
        except Forbidden:
            return
                                                
        channel = await client.channel_private_create(message.author)
        await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')

    mine_mine_clear=( \
        BUILTIN_EMOJIS['white_large_square'].as_emoji,
        BUILTIN_EMOJIS['one'].as_emoji,
        BUILTIN_EMOJIS['two'].as_emoji,
        BUILTIN_EMOJIS['three'].as_emoji,
        BUILTIN_EMOJIS['four'].as_emoji,
        BUILTIN_EMOJIS['five'].as_emoji,
        BUILTIN_EMOJIS['six'].as_emoji,
        BUILTIN_EMOJIS['seven'].as_emoji,
        BUILTIN_EMOJIS['eight'].as_emoji,
        BUILTIN_EMOJIS['bomb'].as_emoji,
            )
    
    mine_mine=tuple(f'||{e}||' for e in mine_mine_clear)
    
    @on_command
    async def mine(client,message,content):
        text_mode=False
        amount=0
        if content:
            content=filter_content(content)
            if content[0]=='text':
                text_mode=True
                content.pop(0)
                
            if content and content[0].isdigit():
                amount=int(content[0])
                if amount>24:
                    amount=24
                elif amount<8:
                    amount=8
        
        if not amount:
            amount=12

            
        data=[0 for x in range(100)]
        
        while amount:
            x=randint(0,9)
            y=randint(0,9)
            position=x+y*10

            value=data[position]
            if value==9:
                continue
            
            local_count=0

            for c_x,c_y in ((-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)):
                local_x=x+c_x
                local_y=y+c_y
                if local_x!=10 and local_x!=-1 and local_y!=10 and local_y!=-1 and data[local_x+local_y*10]==9:
                    local_count+=1
            
            if local_count>3:
                continue

            for c_x,c_y in ((-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)):
                local_x=x+c_x
                local_y=y+c_y
                if local_x!=10 and local_x!=-1 and local_y!=10 and local_y!=-1:
                    local_position=local_x+local_y*10
                    local_value=data[local_position]
                    if local_value==9:
                        continue
                    data[local_position]=local_value+1
                    
            data[position]=9
            
            amount-=1

        result=[]
        result_sub=[]
        y=0
        while True:
            x=0
            while True:
                result_sub.append(mine_mine[data[x+y]])
                x+=1
                if x==10:
                    break
            result.append(''.join(result_sub))
            result_sub.clear()
            y+=10
            if y==100:
                break
        
        if text_mode:
            result.insert(0,'```')
            result.append('```')
        else:
            emoji=BUILTIN_EMOJIS['anger']
            user=message.author
        
        text='\n'.join(result)
        result.clear()
        
        message = await client.message_create(message.channel,text)

        if text_mode:
            return
        
        await client.reaction_add(message,emoji)
        
        try:
            await wait_for_emoji(client,message,
                lambda emoji,user,v0=emoji,v1=user:emoji is v0 and user is v1,
                1200.)
        except TimeoutError:
            return
        finally:
            try:
                await client.reaction_delete_own(message,emoji)
            except (Forbidden,HTTPException):
                pass
        
        y=0
        while True:
            x=0
            while True:
                result_sub.append(mine_mine_clear[data[x+y]])
                x+=1
                if x==10:
                    break
            result.append(''.join(result_sub))
            result_sub.clear()
            y+=10
            if y==100:
                break
        text='\n'.join(result)

        await client.message_edit(message,text)

    @on_command
    async def bans(client,message,content):
        guild=message.guild
        if guild is None:
            return
        ban_data = await client.guild_bans(guild)

        if not ban_data:
            await client.message_create(message.channel,'None')
            return
            
        ban_index=0
        embeds=[]
        maintext=f'Guild bans for {guild.name} {guild.id}:'
        limit=len(ban_data)
        index=0

        while True:
            field_index=0       
            field_count=0
            embed_length=len(maintext)
            embed=Embed(title=maintext)
            embeds.append(embed)
            while True:
                user,reason=ban_data[index]
                if reason is None:
                    reason='Not defined.'
                name=f'{user:f} {user.id}'
                embed_length+=len(reason)+len(name)
                if embed_length>7900:
                    break
                embed.fields.append(Embed_field(name,reason))
                field_count+=1
                if field_count==25:
                    break
                index+=1
                if index==limit:
                    break
            if index==limit:
                break
        
        index=0
        field_count=0
        embed_ln=len(embeds)
        result=[]
        while True:
            embed=embeds[index]
            index+=1
            embed.footer=Embed_footer(f'Page: {index}/{embed_ln}. Bans {field_count+1}-{field_count+len(embed.fields)}/{limit}')
            field_count+=len(embed.fields)
            
            result.append({'embed':embed})
            
            if index==embed_ln:
                break
        
        pagination(client,message.channel,result)

    @on_command
    async def leave_guild(client,message,content):
        guild=message.guild
        if guild is None or guild.owner is not message.author:
            return
        await client.guild_leave(guild)
        
    @on_command
    async def change_prefix(client,message,content):
        guild=message.guild
        if guild is None or message.author is not guild.owner or not content or len(content)>32:
            return
        
        if PREFIXES.add(guild,content):
            try:
                with open(PREFIX_FILENAME,'w') as file:
                    json.dump(PREFIXES.to_json_serializable(),file)
            except (FileNotFoundError,OSError,PermissionError):
                pass
##            try:
##                with open(PREFIX_FILENAME,'wb') as file:
##                    pickle.dump(PREFIXES,file)
##            except (FileNotFoundError,OSError,PermissionError):
##                pass
            
            await client.message_create(message.channel,'OwO')
        else:
            await client.message_create(message.channel,'Thats the actual prefix')

    @on_command
    async def nikki(client,message,content):
        await client.message_create(message.channel,embed=Embed('YUKI YUKI YUKI!','''
            ░░░░░░░░░░░▄▄▀▀▀▀▀▀▀▀▄▄░░░░░░░░░░░░░
            ░░░░░░░░▄▀▀░░░░░░░░░░░░▀▄▄░░░░░░░░░░
            ░░░░░░▄▀░░░░░░░░░░░░░░░░░░▀▄░░░░░░░░
            ░░░░░▌░░░░░░░░░░░░░▀▄░░░░░░░▀▀▄░░░░░
            ░░░░▌░░░░░░░░░░░░░░░░▀▌░░░░░░░░▌░░░░
            ░░░▐░░░░░░░░░░░░▒░░░░░▌░░░░░░░░▐░░░░
            ░░░▌▐░░░░▐░░░░▐▒▒░░░░░▌░░░░░░░░░▌░░░
            ░░▐░▌░░░░▌░░▐░▌▒▒▒░░░▐░░░░░▒░▌▐░▐░░░
            ░░▐░▌▒░░░▌▄▄▀▀▌▌▒▒░▒░▐▀▌▀▌▄▒░▐▒▌░▌░░
            ░░░▌▌░▒░░▐▀▄▌▌▐▐▒▒▒▒▐▐▐▒▐▒▌▌░▐▒▌▄▐░░
            ░▄▀▄▐▒▒▒░▌▌▄▀▄▐░▌▌▒▐░▌▄▀▄░▐▒░▐▒▌░▀▄░
            ▀▄▀▒▒▌▒▒▄▀░▌█▐░░▐▐▀░░░▌█▐░▀▄▐▒▌▌░░░▀
            ░▀▀▄▄▐▒▀▄▀░▀▄▀░░░░░░░░▀▄▀▄▀▒▌░▐░░░░░
            ░░░░▀▐▀▄▒▀▄░░░░░░░░▐░░░░░░▀▌▐░░░░░░░
            ░░░░░░▌▒▌▐▒▀░░░░░░░░░░░░░░▐▒▐░░░░░░░
            ░░░░░░▐░▐▒▌░░░░▄▄▀▀▀▀▄░░░░▌▒▐░░░░░░░
            ░░░░░░░▌▐▒▐▄░░░▐▒▒▒▒▒▌░░▄▀▒░▐░░░░░░░
            ░░░░░░▐░░▌▐▐▀▄░░▀▄▄▄▀░▄▀▐▒░░▐░░░░░░░
            ░░░░░░▌▌░▌▐░▌▒▀▄▄░░░░▄▌▐░▌▒░▐░░░░░░░
            ░░░░░▐▒▐░▐▐░▌▒▒▒▒▀▀▄▀▌▐░░▌▒░▌░░░░░░░
            ░░░░░▌▒▒▌▐▒▌▒▒▒▒▒▒▒▒▐▀▄▌░▐▒▒▌░░░░░░░
            ''',0xffafde,'https://www.youtube.com/watch?v=NI_fgwbmJg0&t=0s'))
    valuable_scopes=[scope for scope in SCOPES if scope[0] not in 'mrw']

    OA2_accesses={}

    @on_command
    async def oa2_link(client,message,content): #just a test link
        await client.message_create(message.channel,'https://discordapp.com/oauth2/authorize?client_id=486565096164687885&redirect_uri=https%3A%2F%2Fgithub.com%2FHuyaneMatsu&response_type=code&scope=identify%20connections%20guilds%20guilds.join%20email')
    
    @on_command
    async def oa2_feed(client,message,content):
        client.loop.create_task(client.message_delete(message))
        try:
            result=parse_oauth2_redirect_url(content)
        except ValueError:
            await client.message_create(message.channel,'Bad link')
            return

        access = await client.activate_authorization_code(*result,valuable_scopes)

        if access is None:
            await client.message_create(message.channel,'Too old link')
            return
        user = await client.user_info(access)
        OA2_accesses[user.id]=user
        await client.message_create(message.channel,'Thanks')
        
    def oa2_query(message,content):
        author_id=message.author.id
        if not (16<len(content)<33):
            return OA2_accesses.get(author_id,None)
        try:
            user_id=int(content)
        except ValueError:
            return OA2_accesses.get(author_id,None)
        
        user=OA2_accesses.get(user_id,None)
        if user is None:
            user=OA2_accesses.get(author_id,None)
        return user

    @on_command
    async def oa2_user(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')

        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(user)])


    @on_command
    async def oa2_connections(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')

        connections = await client.user_connections(user.access)
        
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(connections)])
        
        
    @on_command
    async def oa2_guilds(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')

        guilds = await client.user_guilds(user.access)
        
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(guilds)])
        
    @on_command
    async def oa2_my_guild(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')
        
        if message.author is not client.owner and user!=message.author:
            await client.message_create(message.channel,'NOPE, do it on yourself!')
        
        try:
            guild = await client.guild_create(name='Luv ya',
                channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=Channel_text),])

            await sleep(1.,client.loop)
            await client.guild_user_add(guild,user)
            await sleep(1.,client.loop)
            await client.guild_edit(guild,owner=user)
        except Exception as err:
            print(err)
            traceback.print_exc()
        finally:
            await sleep(1.,client.loop)
            if client is guild.owner:
                await client.guild_delete(guild)
            else:
                await client.guild_leave(guild)
            
    @on_command
    async def oa2_owners(client,message,content):
        if message.author is not client.owner:
            return

        access = await client.owners_access(valuable_scopes)
        user = await client.user_info(access)
        OA2_accesses[user.id]=user
        result=[f'queried {user:f}']
        for scope in access.scopes:
            result.append(f'- {scope}')

        text='\n'.join(result)
                     
        await client.message_create(message.channel,text)
        
    @on_command
    async def oa2_renew(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')
        access=user.access
        last=access.created_at
        await client.renew_access_token(access)
        new=access.created_at
        await client.message_create(message.channel,f'{user:f}\' access token got renewed.\nFrom creation time at: {last:%Y.%m.%d-%H:%M:%S}\nTo creation time at: {new:%Y.%m.%d-%H:%M:%S}')

    @on_command
    async def OG(client,message,content):
        if message.author is not client.owner:
            return
        
        access = await client.owners_access(valuable_scopes)
        user = await client.user_info(access)

        guild = await client.guild_create(name=content,
            channels=[cr_pg_channel_object(name='general',type_=Channel_text),])

        await sleep(1.,client.loop)
        role = await client.role_create(guild,'my dear',8)
        await client.guild_user_add(guild,user,roles=[role])
        await sleep(1.,client.loop)


    
##def start_console():
##    import code
##    shell = code.InteractiveConsole(globals().copy())
##    shell.interact()
##    print('closing')
##    stop_clients()
    
start_clients()
#start_console()
