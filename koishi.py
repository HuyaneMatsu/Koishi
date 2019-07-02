# -*- coding: utf-8 -*-
import sys
from random import randint
import os
import re
import time
from weakref import WeakKeyDictionary

#moving to the outer folder, so hata ll count as a package
sys.path.append(os.path.abspath('..'))
from collections import deque
from datetime import timedelta
import traceback

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup=None

from hata.dereaddons_local import inherit
from hata import Client,start_clients
from hata.exceptions import DiscordException
from hata.emoji import BUILTIN_EMOJIS,parse_emoji
from hata.activity import Activity_game
from hata.others import filter_content
from hata import others

from hata.channel import cr_pg_channel_object,Channel_text,Channel_private,Message_iterator
from hata.embed import Embed
from hata.events import (
    pagination,bot_reaction_waitfor,bot_message_event,wait_for_message,
    wait_for_emoji,prefix_by_guild,bot_reaction_delete_waitfor,cooldown,
    waitfor_wrapper)
from hata.futures import CancelledError,sleep,wait_more
from hata.prettyprint import pchunkify
from hata.user import USERS,User
from hata.client_core import KOKORO,stop_clients,CLIENTS
from hata.oauth2 import SCOPES
from hata.events_compiler import content_parser
from hata.webhook import Webhook
from hata.role import Role
from hata.guild import Guild

from image_handler import on_command_upload,on_command_image
from help_handler import on_command_help,HELP,invalid_command
import pers_data
from infos import infos,update_about
from voice import voice
from battleships import battle_manager
from dispatch_tests import dispatch_tester
from ratelimit_tests import ratelimit_commands
from kanako import kanako_manager
from dungeon_sweeper import ds_manager,_DS_modify_best
import models

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
        except DiscordException:
            pass

PREFIXES=prefix_by_guild(pers_data.PREFIX,models.DB_ENGINE,models.PREFIX_TABLE,models.pefix_model)

Koishi=Client(pers_data.TOKEN1,
    secret=pers_data.CLIENT_SECRET,
    client_id=pers_data.ID1,
    activity=Activity_game.create(name='with Satori'),
        )

Mokou=Client(pers_data.TOKEN2,
    client_id=pers_data.ID2,
        )

TYPINGS={}
class typing_counter:
    __slots__=['duration', 'timestamp', 'user']
    def __init__(self,user,timestamp):
        self.user=user
        self.timestamp=timestamp
        self.duration=8.

_MOKOU_FIRE_RP=re.compile('i|u|you|we|iam')
_MOKOU_MOKOU_RP=re.compile('mokou?')

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
        
        index=0
        while True:
            element=channel_q[index]
            if element.user is user:
                del channel_q[index]
                ln-=1
            else:
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
            if not channel.cached_permissions_for(client).can_read_message_history:
                parts.append('I have no permission to read older messages.')
            if channel.turn_GC_on_at:
                now=time.monotonic()
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
            if 'fire' in content and _MOKOU_FIRE_RP.search(content) is not None:
                text='BURN!!!'
            elif _MOKOU_MOKOU_RP.search(content) is not None:
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
    limit=timestamp-timedelta(seconds=40)
    
    while True:
        index-=1
        if channel_q[index].timestamp<limit:
            del channel_q[index]
            if index:
                continue
            channel_q.appendleft(typing_counter(user,timestamp),)
            return
        break

    ln=len(channel_q)
    index=0
    limit=timestamp-timedelta(seconds=8)
    while True:
        element=channel_q[index]
        if element.timestamp<=limit:
            break
        
        if element.user is user:
            element.duration=(timestamp-element.timestamp).total_seconds()
            break

        index+=1
        if index==ln:
            channel_q.appendleft(typing_counter(user,timestamp),)
            return
        
    index=ln-1
    duration=0
    found=0
    while index:
        element=channel_q[index]
        if element.user is user:
            duration+=element.duration
            found+=1
            if duration>=30:
                break
        index-=1
    
    if duration<30 or found==len(channel_q):
        channel_q.appendleft(typing_counter(user,timestamp),)
        return

    channel_q.clear()
    if not randint(0,3):
        await self.message_create(channel,f'**{user.name_at(channel.guild)}** is typing...')

@Mokou.events
async def channel_delete(self,channel):
    try:
        del TYPINGS[channel.id]
    except KeyError:
        pass

class commit_extractor:
    _GIT_RP=re.compile('^\[`[\da-f]*`\]\((https://github.com/[^/]*/[^/]*/)commit')
    __slots__=['channel', 'client', 'color', 'role', 'webhook']
    def __init__(self,client,channel,webhook,role=None,color=0):
        self.client=client
        self.channel=channel
        self.webhook=webhook
        self.role=role
        self.color=color

    async def __call__(self,message):
        webhook=self.webhook
        client=self.client

        if message.author!=webhook or message.author.name!='GitHub':
            return
        
        embed=message.embeds[0]

        if ':master' not in embed.title:
            return

        url=self._GIT_RP.match(embed.description).group(1)+'commit/master'
        result = await client.download_url(url)
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

        embed_text=others.chunkify(description_container.getText('\n').splitlines())
        result_embed=Embed(
            title       = title_container.getText('\n').strip(),
            description = embed_text[0],
            color       = self.color,
            url         = url,
                )

        extra_embeds=[]
        for index in range(1,min(len(embed_text),9)):
            extra_embeds.append(
                Embed(
                    title       = '',
                    description = embed_text[index],
                    color       = self.color,
                    url         = '',
                        )
                )
            
        webhook_name = embed.author.name
        webhook_avatar_url = embed.author.proxy_icon_url

        if needs_unlock:
            try:
                await Koishi.role_edit(self.role,mentionable=True)
                await sleep(0.8,client.loop)
                await client.webhook_send(webhook,
                    result_content,
                    result_embed,
                    name=webhook_name,
                    avatar_url=webhook_avatar_url
                        )
                for embed in extra_embeds:
                    await client.webhook_send(webhook,
                        '',
                        embed,
                        name=webhook_name,
                        avatar_url=webhook_avatar_url
                            )
                await sleep(0.8,client.loop)
            finally:
                await Koishi.role_edit(self.role,mentionable=False)

        else:
            await client.webhook_send(webhook,
                result_content,
                result_embed,
                name=webhook_name,
                avatar_url=webhook_avatar_url
                    )

@inherit(bot_message_event)
class message_delete_waitfor():
    __slots__=['waitfors']
    __event_name__='message_delete'
    def __init__(self):
        self.waitfors=WeakKeyDictionary()

    async def __call__(self,client,message):
        try:
            event=self.waitfors[message.channel]
        except KeyError:
            return
        await event(message)

class Channeller_v_del():
    __slots__=['parent']
    def __init__(self,parent):
        self.parent=parent

    async def __call__(self,message):
        nonwebhook=(Client,User)
        if type(message.author) not in nonwebhook:
            return

        client=self.parent.client
        source_channel=message.channel
        user=message.author
        
        content     = message.clean_content
        embed       = message.clean_embeds
        file        = None if message.attachments is None else [attachment.name for attachment in message.attachments]
        tts         = message.tts
        #avatar_url  = message.author.avatar_url #cannot compare avatar urls.
                
        for channel,webhook in self.parent.pairs:
            if channel is source_channel:
                continue
        
            for message in channel.messages:
                if type(message.author) in nonwebhook:
                    continue
                if (user.name_at(webhook.guild) != message.author.name or \
                    #avatar_url  != message.author.avatar_url or \
                    content     != message.clean_content or \
                    file        != (None if message.attachments is None else [attachment.name for attachment in message.attachments]) or \
                    embed       != message.clean_embeds or \
                    tts         != message.tts \
                        ):
                    
                    continue

                client.loop.create_task(client.message_delete(message))
                break
                    
class Channeller():
    __slots__=['client', 'deleter', 'pairs']
    def __init__(self,client,pairs):
        self.client=client
        self.pairs=pairs
        self.deleter=deleter=Channeller_v_del(self)
        
        event_1=client.events.message_create
        event_2=client.events.message_delete
        for pair in pairs:
            channel=pair[0]
            event_1.append(self,channel)
            event_2.append(deleter,channel)
            CHANNELINGS[channel.id]=self

    def cancel(self,channel):
        event_1=self.client.events.message_create
        event_2=self.client.events.message_delete
        pairs=self.pairs
        deleter=self.deleter
        if channel is None:
            pass
        elif len(pairs)<3:
            for pair in pairs:
                del CHANNELINGS[pair[0].id]
        else:
            for index,pair in enumerate(pairs):
                if pair[0] is channel:
                    del pairs[index]
                    break
            event_1.remove(self,channel)
            event_2.remove(deleter,channel)
            del CHANNELINGS[channel.id]
            return

        for pair in pairs:
            channel=pair[0]
            event_1.remove(self,channel)
            event_2.remove(deleter,channel)
            
        deleter.parent=None
        self.deleter=None

    
    async def __call__(self,message):
        if type(message.author) not in (Client,User):
            return

        client=self.client
        
        attachments=message.attachments
        if attachments is None:
            files=None
        else:
            files=[]
            for attachment in attachments:
                file = await client.download_attachment(attachment)
                files.append((attachment.name,file))

        source_channel=message.channel
        
        for channel,webhook in self.pairs:
            if channel is source_channel:
                continue
            client.loop.create_task(
                client.webhook_send(webhook,
                    content     = message.clean_content,
                    embed       = message.clean_embeds,
                    file        = files,
                    tts         = message.tts,
                    name        = message.author.name_at(webhook.guild),
                    avatar_url  = message.author.avatar_url,
                        )
                    )

CHANNELINGS={}

@content_parser('condition, default="message.author is not client.owner"',
                'int, flags="g"',)
async def channeling_start(client,message,channel_id):
    channel_1=message.channel
    while True:
        permission=channel_1.cached_permissions_for(client)
        if not (permission.can_manage_webhooks and permission.can_manage_messages):
            text='I have no permission at this channel to invoke this command!'
            break

        try:
            channel_2=client.channels[channel_id]
        except KeyError:
            text=f'Unknown channel : {channel_id}'
            break
        
        if channel_1 is channel_2:
            text='Same channel...'
            break
        
        permission=channel_2.cached_permissions_for(client)
        if not (permission.can_manage_webhooks and permission.can_manage_messages):
            text='I have no permission at that channel to invoke this command!'
            break

        channeling_1=CHANNELINGS.get(channel_1.id,None)
        channeling_2=CHANNELINGS.get(channel_2.id,None)
        
        if channeling_1 is not None and channeling_2 is not None and channeling_1 is channeling_2:
            text='This connection is already set up'
            break

        pairs=[]
        if channeling_1 is None:
            webhooks = await client.webhook_get_channel(channel_1)
            if webhooks:
                webhook=webhooks[0]
            else:
                webhook = await client.webhook_create(channel_1,'Love You')
            pairs.append((channel_1,webhook,),)
        else:
            channeling_1.cancel(None)
            pairs.extend(channeling_1.pairs)

        if channeling_2 is None:
            webhooks = await client.webhook_get_channel(channel_2)
            if webhooks:
                webhook=webhooks[0]
            else:
                webhook = await client.webhook_create(channel_2,'Love You')
            pairs.append((channel_2,webhook,),)
        else:
            channeling_2.cancel(None)
            pairs.extend(channeling_2.pairs)


        Channeller(client,pairs)
        text=f'Channelling between `{channel_1.guild}/{channel_1}` and `{channel_2.guild}/{channel_2}`'
        break
    
    await client.message_create(channel_1,text)
    
async def channeling_stop(client,message,content):
    if message.author is not client.owner:
        return
    channel=message.channel
    while True:
        try:
            channeller=CHANNELINGS[channel.id]
        except KeyError:
            text='There is no active channeller at this channel'
            break

        channeller.cancel(channel)
        text='Success'
        break

    await client.message_create(channel,text)
    
    
@Koishi.events
class once_on_ready:
    __slots__ = ['called',]
    __event_name__='ready'
    def __init__(self):
        self.called=False
    async def __call__(self,client):
        if self.called:
            return
        self.called=True

        print(f'{client:f} ({client.id}) logged in')
        await client.update_application_info()
        print(f'owner: {client.owner:f} ({client.owner.id})')
        update_about(client)
    
Koishi.events(bot_reaction_waitfor())
Koishi.events(bot_reaction_delete_waitfor())
Koishi.events(message_delete_waitfor())

AOE2_S=Guild.precreate(564093916152856576)
AOE2_S_role=Role.precreate(566693615544434706)

@Koishi.events
async def guild_user_add(client,guild,user):
    if user.is_bot:
        return
    if guild is AOE2_S:
        await client.user_role_add(user,AOE2_S_role)

with Koishi.events(bot_message_event(PREFIXES)) as on_command:

    webhook_sender=commit_extractor(
        Koishi,
        Channel_text.precreate(555476090382974999),
        Webhook.precreate(555476334210580508),
        role=Role.precreate(538397994421190657),
        color=0x2ad300,
            )
    
    Koishi.events.message_create.append(webhook_sender,webhook_sender.channel)

        
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
    on_command(_DS_modify_best)
    on_command(channeling_start)
    on_command(channeling_stop)

    _KOISHI_NOU_RP=re.compile(r'n+\s*o+\s*u+',re.I)
    _KOISHI_OWO_RP=re.compile('(owo|uwu|0w0)',re.I)
    @on_command
    async def default_event(client,message):
        content=message.content
        text=None
        if _KOISHI_NOU_RP.match(content) is not None:
            parts=[]
            for value in 'nou':
                emoji=BUILTIN_EMOJIS[f'regional_indicator_{value}']
                await client.reaction_add(message,emoji)
                    
        elif len(content)==3:
            matched=_KOISHI_OWO_RP.match(content,)
            if matched is not None:
                text=f'{content[0].upper()}{content[1].lower()}{content[2].upper()}'
        
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
    @content_parser('int, default="1"')
    async def dice(client,message,times):
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
        await client.message_create(message.channel,f'{int(client.kokoro.latency*1000.)} ms')
    

    @on_command
    async def message_me(client,message,content):
        channel = await client.channel_private_create(message.author)
        try:
            await client.message_create(channel,'Love you!')
        except DiscordException:
            await client.message_create(message.channel,'Pls turn on private messages from this server!')

    @on_command
    @content_parser('condition, flags=g, default="not message.channel.permissions_for(message.author).can_manage_messages"',
                    'int, default=1',
                    'rest, default="f\'{message.author:f} asked for it\'"')
    async def clear(client,message,limit,reason):
        await client.message_delete_sequence(channel=message.channel,limit=limit,reason=reason)

    @on_command
    async def waitemoji(client,message,content):
        channel=message.channel
        
        message_to_delete = await client.message_create(channel,'Waiting!')
        
        try:
            _,emoji = await wait_for_message(client,channel,lambda message:parse_emoji(message.content),30.)
        except TimeoutError:
            emoji=None
        except Exception as err:
            return
        
        try:
            await client.message_delete(message_to_delete)
        except DiscordException:
            pass
        
        if emoji is not None:
            await client.message_create(channel,emoji.as_emoji*5)

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
        except DiscordException:
            return
                                                
        channel = await client.channel_private_create(message.author)
        await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')

    mine_mine_clear = (
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
        
        message.weakrefer()
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
            except DiscordException:
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
        if not guild.permissions_for(client).can_ban_user:
            return await client.message_create(message.channel,embed=Embed(description='I have no permissions to check it.'))
                                     
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
                embed.add_field(name,reason)
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
            embed.add_footer(f'Page: {index}/{embed_ln}. Bans {field_count+1}-{field_count+len(embed.fields)}/{limit}')
            field_count+=len(embed.fields)
            
            result.append({'embed':embed})
            
            if index==embed_ln:
                break
        
        await pagination(client,message.channel,result)

    @on_command
    async def leave_guild(client,message,content):
        guild=message.guild
        if guild is None or guild.owner is not message.author:
            return
        await client.guild_leave(guild)
        
    @on_command
    async def change_prefix(client,message,content):
        guild=message.guild
        if (guild is None) or (message.author is not guild.owner) or (not content):
            return
        content=filter_content(content)[0]
        if not (0<len(content)<33):
            text=f'Prefix lenght should be between 1 and 32, got {len(content)}.'
        elif PREFIXES.add(guild,content):
            text='Prefix modified.'
        else:
            text='Thats the frefix already.'
        await client.message_create(message.channel,text)

    @on_command
    async def _change_prefix(client,message,content):
        if message.author is not client.owner:
            return
        content=filter_content(content)
        if len(content)<2:
            return
        if not (0<len(content[1])<33):
            return
        
        try:
            guild=client.guilds[int(content[0])]
        except (ValueError,KeyError):
            guild=client.get_guild(content[0])
            if guild is None:
                return
        if PREFIXES.add(guild,content[1]):
            text='Done.'
        else:
            text='No modifications took place.'

        await client.message_create(message.channel,text)
    
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
            result=others.parse_oauth2_redirect_url(content)
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
            return
        
        await pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(user)])


    @on_command
    async def oa2_connections(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')
            return
        
        connections = await client.user_connections(user.access)
        
        await pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(connections)])
        
        
    @on_command
    async def oa2_guilds(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')
            return
        
        guilds = await client.user_guilds(user.access)
        
        await pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(guilds)])
        
    @on_command
    async def oa2_my_guild(client,message,content):
        user=oa2_query(message,content)
        if user is None:
            await client.message_create(message.channel,'Could not find that user')
            return
        
        if message.author is not client.owner and user!=message.author:
            await client.message_create(message.channel,'NOPE, do it on yourself!')
            return
        
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
            try:
                guild
            except UnboundLocalError:
                return
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
            return
        
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
        
    @on_command
    async def download(self,message,content):
        if message.author is not self.owner:
            return
        data = await self.download_url(content)
        soup = BeautifulSoup(data,'html.parser',from_encoding='utf-8')
        text = soup.prettify()
        result = [{'content':element} for element in others.cchunkify(text.splitlines())]
        await pagination(self,message.channel,result)

    @on_command
    @content_parser('emoji')
    async def se(client,message,emoji):
        if emoji.is_custom_emoji:
            await client.message_create(message.channel,f'**Name:** {emoji:e} **Link:** {emoji.url}')


    @on_command
    async def nitro(client,message,content):
        if message.permissions.can_manage_messages:
            client.loop.create_task(client.message_delete(message))
        content=filter_content(content)
        
        if not content:
            return
        
        text_form=content[0]
        
        emoji=parse_emoji(text_form)
        
        if emoji is None:
            
            for guild in client.guilds.values():
                emoji=guild.get_emoji(text_form)
                if emoji is not None:
                    break
            
            if emoji is None:
                return
            
        else:
            if emoji.is_custom_emoji:
                found=False
                for guild in client.guilds.values():
                    if emoji.id in guild.emojis:
                        found=True
                        break
                
                if found==False:
                    return
        
        await client.message_create(message.channel,emoji.as_emoji)

    @on_command
    @content_parser('condition, default="message.author is not client.owner"',
                    'int',
                    'channel, flags=mnig, default="message.channel"',)
    async def resend_webhook(client,message,message_id,channel):
        try:
            target_message = await client.message_get(channel,message_id)
        except Exception as err:
            await client.message_create(message.channel,err.__class__.__name__)
            return

        webhooks = await client.webhook_get_channel(channel)
        webhook=webhooks[0]

        await client.webhook_send(webhook,
            embed=target_message.embeds,
            name=target_message.author.name,
            avatar_url=target_message.author.avatar_url)

    @on_command
    @content_parser('int', 'int, default="0"',)
    async def random(client,message,v1,v2):
        result=randint(v2,v1) if v1>v2 else randint(v1,v2)
        await client.message_create(message.channel,str(result))

    async def pararell_load(client,channel,future):
        try:
            await client.message_at_index(channel,256256256) #gl
        except (IndexError,PermissionError) as err:
            pass
        except BaseException as err:
            traceback.print_exc()
        finally:
            future.set_result(None)
        
    @on_command
    async def count_messages(client,message,content):
        if message.author is not client.owner:
            return
        source_channel=message.channel
        guild=source_channel.guild
        if guild is None:
            return
        
        loop=client.loop
        channels=guild.messageable_channels
        future=wait_more(loop,len(channels))
        users={}
        
        with client.keep_typing(source_channel):
            for channel in channels:
                client.loop.create_task(pararell_load(client,channel,future))

            await future
            
            for channel in channels:
                for message in channel.messages:
                    user=message.author
                    if type(user) in (Client,User):
                        users[user]=users.get(user,0)+1
        users=list(users.items())
        users.sort(reverse=True,key=lambda item:item[1])
        text=[f'{index}.: {user:f} : {count}' for index,(user,count) in enumerate(users,1)]
        chunks=[{'content':chunk} for chunk in others.chunkify(text)]
        await pagination(client,source_channel,chunks)

    async def pararell_load_reactions(client,channel,future,reactions):
        try:
            await client.message_at_index(channel,256256256) #gl
        except (IndexError,PermissionError) as err:
            pass
        except BaseException as err:
            traceback.print_exc()
        finally:
            messages=[message for message in channel.messages if message.reactions]
            for message in messages:
                try:
                    await client.reaction_load_all(message)
                except DiscordException:
                    continue
                for emoji,reacters in message.reactions.items():
                    for user in reacters:
                        try:
                            user_s=reactions[user]
                        except KeyError:
                            user_s=reactions[user]={}
                        user_s[emoji]=user_s.get(emoji,0)+1

            future.set_result(None)
        
    @on_command
    async def count_reactions(client,message,content):
        if message.author is not client.owner:
            return
        source_channel=message.channel
        guild=source_channel.guild
        if guild is None:
            return
        
        loop=client.loop
        channels=guild.messageable_channels
        future=wait_more(loop,len(channels))
        reactions={}
        
        with client.keep_typing(source_channel):
            for channel in channels:
                client.loop.create_task(pararell_load_reactions(client,channel,future,reactions))

            await future

        sorted_reactions=[]
        for user,emojis in reactions.items():
            emoji_count=sum(emojis.values())
            emojis=list(emojis.items())
            emojis.sort(reverse=True,key=lambda item:item[1])
            sorted_reactions.append((user,emojis,emoji_count),)
            
        sorted_reactions.sort(reverse=True,key=lambda item:item[2])

        text=[]
        for index,(user,emojis,amount) in enumerate(sorted_reactions,1):
            text.append(f'{index}.: {user:f} {amount}')
            for index,(emoji,emoji_count) in enumerate(emojis,1):
                text.append(f' - {index} {emoji:e} {emoji_count}')
        
        chunks=[{'content':chunk} for chunk in others.chunkify(text)]
        await pagination(client,source_channel,chunks)

    @on_command
    @content_parser('delta, default="None"')
    async def parse_timedelta(client,message,delta):
        await client.message_create(message.channel,(repr(delta)))

            
    
##def start_console():
##    import code
##    shell = code.InteractiveConsole(globals().copy())
##    shell.interact()
##    print('closing')
##    stop_clients()
    
start_clients()
#start_console()
