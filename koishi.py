# -*- coding: utf-8 -*-
import sys
from random import randint as random,choice
import os
import re
import asyncio
import time
import json
#import pickle
#moving to the outer folder, so uwu ll count as a package
sys.path.append(os.path.abspath('..'))

from discord_uwu import Client,start_clients
from discord_uwu.exceptions import Forbidden,HTTPException
from discord_uwu.emoji import BUILTIN_EMOJIS,parse_emoji
from discord_uwu.activity import activity_game
from discord_uwu.others import ( \
    is_channel_mention,is_user_mention,filter_content,chunkify,is_id,
    guild_features,message_notification_levels,voice_regions, Unknown,
    verification_levels,content_filter_levels,audit_log_events,
    is_role_mention,ext_from_base64)
from discord_uwu.channel import Channel_voice,get_message_iterator,cr_pg_channel_object,Channel_text
from discord_uwu.color import Color
from discord_uwu.permission import Permission
from discord_uwu.embed import Embed,Embed_image,Embed_field,Embed_footer,Embed_author
from discord_uwu.events import ( \
    waitfor_wrapper,pagination,wait_and_continue,bot_reaction_waitfor,
    bot_message_event,wait_for_message,wait_for_emoji,cooldown,prefix_by_guild)
from discord_uwu.futures import wait_one,CancelledError,sleep
from discord_uwu.prettyprint import pchunkify,connect
from discord_uwu.http import VALID_ICON_FORMATS,VALID_ICON_FORMATS_EXTENDED
from discord_uwu.webhook import Webhook
from discord_uwu.audit_logs import Audit_log_iterator
from discord_uwu.guild import GUILDS

from image_handler import on_command_upload,on_command_image
from help_handler import on_command_help,HELP,invalid_command
from pers_data import TOKEN,PREFIX,TOKEN2
from infos import infos
from voice import voice
from battleships import battle_manager,bot_reaction_delete_waitfor

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

class schannel:
    __slots__=['channel']
    def __init__(self):
        self.channel=None
        
    async def set_channel(self,client,message,content):
        if message.author is client.owner:
            self.channel=message.channel
            await client.message_create(message.channel,'I ll send special messages to this channel')
    
    async def emoji_update(self,client,guild,modifications):
        if self.channel is not None:
            result=[]
            for modtype,emoji,diff in modifications:
                if modtype=='n':
                    result.append(f'New emoji: "{emoji.name}" : {emoji}')
                    continue
                if modtype=='d':
                    result.append(f'Deleted emoji: "{emoji.name}" : {emoji}')
                    continue
                if modtype=='e':
                    result.append(f'Emoji edited: "{emoji.name}" : {emoji}\n{diff}')
                    continue
                raise RuntimeError #bugged?
        
            pages=[{'content':chunk} for chunk in chunkify(result)]
            await client.message_create(self.channel,**pages[0])
            
    async def unknown_guild(self,client,parser,guild_id,data):
        if self.channel is not None:
            await client.message_create(self.channel,f'Unknown guild at {parser}: {guild_id}\n data: {data}')

    async def unknown_channel(self,client,parser,channel_id,data):
        if self.channel is not None:
            await client.message_create(self.channel,f'Unknown channel at {parser}: {channel_id}\n data: {data}')

    async def unknown_role(self,client,parser,guild,role_id,data):
        if self.channel is not None:
            await client.message_create(self.channel,f'Unknown guild: {guild} at {parser}; role: {role_id}\n data: {data}')

    async def unknown_voice_client(self,client,parser,voice_client_id,data):
        if self.channel is not None:
            await client.message_create(self.channel,f'Unknown voice client at {parser}: {voice_client_id}\n data: {data}')

    async def guild_user_delete(self,client,guild,user,profile):
        if self.channel is not None:
            await client.message_create(self.channel,f'A user left a guild: {guild.name} : {user:f}')

    async def guild_user_add(self,client,guild,user):
        if self.channel is not None:
            await client.message_create(self.channel,f'A user joined the guild: {guild.name} :  {user:f}')
            
    async def guild_ban_add(self,client,guild,user):
        if self.channel is not None:
            await client.message_create(self.channel,f'A user got banned from the guild: {guild.name} :  {user:f}')

    async def guild_ban_delete(self,client,guild,user):
        if self.channel is not None:
            await client.message_create(self.channel,f'A user got unbanned from the guild: {guild.name} :  {user:f}')
    
            
schannel=schannel()

##class pinner:
##    reset=BUILTIN_EMOJIS['arrows_counterclockwise']
##    __slots__=['cancel', 'channel',]
##    def __init__(self,client,channel):
##        self.channel=channel
##        self.cancel=type(self)._default_cancel
##        waitfor_wrapper(client,self,240.)
##        
##    async def start(self,wrapper):
##        client=wrapper.client
##
##        #we add the finishing details to the wrapper
##        wrapper.event=client.events.reaction_add
##        wrapper.target=message= await client.message_create(self.channel,content='Click on the emoji bellow')
##        
##        await client.reaction_add(message,self.reset)
##
##    async def __call__(self,wrapper,args):
##        emoji,user=args
##        if emoji is not self.reset or not self.channel.guild.permissions_for(user).can_administrator:
##            return
##        
##        client=wrapper.client
##        message=wrapper.target
##
##        try:
##            await client.reaction_delete(message,emoji,user)
##        except (Forbidden,HTTPException):
##            pass
##        
##        if message.pinned:
##            await client.message_unpin(message)
##        else:
##            await client.message_pin(message)
##
##        if wrapper.timeout<240.:
##            wrapper.timeout+=30.
##    
##    _default_cancel=pagination._default_cancel

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
    
Koishi=Client(TOKEN,loop=1)
Koishi.activity=activity_game.create(name='with Satori')

Mokou=Client(TOKEN2,loop=2)
    
@Mokou.events
async def message_create(client,message):
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
    else:
        if random(0,2):
            return
        if 'fire' in content and re.match(r'\b(i|u|you|we|iam)\b',content):
            text='BURN!!!'
        elif re.match(r'(\b|[^\s\d])(moko[u]{0,1})\b',content):
            text='Yes, its me..'
        else:
            return
    await client.message_create(message.channel,text)
        


@Koishi.events
async def ready(client):
    print(f'{client:f} ({client.id}) logged in')
    await client.update_application_info()
    print(f'owner: {client.owner:f} ({client.owner.id})')
    
Koishi.events(bot_reaction_waitfor())
Koishi.events(bot_reaction_delete_waitfor())

Koishi.events(schannel.emoji_update)
Koishi.events(schannel.unknown_guild)
Koishi.events(schannel.unknown_channel)
Koishi.events(schannel.unknown_role)
Koishi.events(schannel.unknown_voice_client)
Koishi.events(schannel.guild_user_delete)
Koishi.events(schannel.guild_user_add)
Koishi.events(schannel.guild_ban_add)
Koishi.events(schannel.guild_ban_delete)

with Koishi.events(bot_message_event(PREFIXES)) as on_command:

    on_command(schannel.set_channel,'here')
    on_command.extend(infos)
    on_command(voice)
    on_command(on_command_image,'image')
    on_command(on_command_upload,'upload')
    on_command(on_command_help,'help')
    on_command(invalid_command)
    
    on_command(battle_manager,case='bs')
    
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
    async def rate(client,message,content):
        target=None
        if content:
            if message.user_mentions:
                target=message.user_mentions[0]
            else:
                guild=message.guild
                if guild is not None:
                    target=guild.get_user(content)
        if target is None:
            target=message.author
            
        #nickname check
        name=target.display_name(message.guild)

        if target==client:
            result=10
        else:
            result=target.id%11

        await client.message_create(message.channel,f'I rate {name} {result}/10')


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
                result+=random(1,6)
                
            if result<=2.5*times:
                luck_text=', better luck next time!'
            elif result>=5.5*times:
                luck_text=', so BIG,.. thats what she said... *cough*'
            else:
                luck_text=''
            text=f'Rolled {result} {luck_text}'
            
        await client.message_create(message.channel,text)


##    @on_command.add('print')
##    async def on_print_command(client,message,content):
##        try:
##            await client.message_delete(message,reason='Used print command')
##        except Forbidden:
##            pass
##        else:
##            await client.message_create(message.channel,content)

    @on_command
    async def mention_event(client,message):
        m1=message.author.mention_at(message.guild)
        m2=client.mention_at(message.guild)
        replace={re.escape(m1):m2,re.escape(m2):m1}
        pattern=re.compile("|".join(replace.keys()))
        result=pattern.sub(lambda x: replace[re.escape(x.group(0))],message.content)
        await client.message_create(message.channel,result)

##    @on_command
##    async def pong(client,message,content):
##        guild=message.channel.guild
##        if guild is not None:
##            user=guild.get_user(content)
##            if user is not None:
##                await client.message_create(message.channel,user.mention_at(guild))

    @on_command
    async def ping(client,message,content):
        await client.message_create(message.channel,f'{int(client.websocket.kokoro.latency*1000.)} ms')
                              
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

##    @on_command
##    async def pm(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        content=filter_content(content)
##        while True:
##            if len(content)!=1:
##                text='The 1st line must contain a mention/username of the "lucky" person.'
##                break
##            content=content[0]
##            if message.user_mentions and is_user_mention(content):
##                user=message.user_mentions[0]
##            else:
##                user=guild.get_user(content)
##                if user is None:
##                    text='Could not find that user!'
##                    break
##
##            index=message.content.find('\n')+1
##            if not index:
##                text='Unable to send empty message'
##                break
##            text=message.content[index:]
##            if not text:
##                text='Unable to send empty message'
##                break
##            if user is client:
##                text='Ok, i got it!'
##                break
##            channel = await client.channel_private_create(user)
##            try:
##                await client.message_create(channel,text)
##                text='Big times! Message sent!'
##            except Forbidden:
##                text='Access denied'
##            break
##                                    
##        await client.message_create(message.channel,text)
        
    @on_command
    async def message_me(client,message,content):
        channel = await client.channel_private_create(message.author)
        try:
            await client.message_create(channel,'Love you!')
        except Forbidden:
            await client.message_create(message.channel,'Pls turn on private messages from this server!')
            
    @on_command
    async def edit(client,message,content):
        guild=message.guild
        if guild is None:
            return
        text=''
        content=filter_content(content)
        key=''
        reason=''
        
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            if not content:
                break
            key=content.pop(0)
            if key=='user':
                if not content:
                    text='You can edit "nick", "role", "deaf", "mute", "voice_channel".'
                    break
                limit=len(content)
                if (limit&1)^1:
                    text='Pls send 1 mention, then key, value pairs.'
                    break
                if limit==1:
                    text='You can edit "nick", "role", "deaf", "mute", "voice_channel".'
                    break
                if message.user_mentions:
                    if len(message.user_mentions)>1:
                        text='Pls send 1 mention or 1 name and stuffs to change.'
                        break
                    if not is_user_mention(content[0]):
                        text='1st value must be mention.'
                        break
                    user=message.user_mentions[0]
                else:
                    user=guild.get_user(content[0])
                    if user is None:
                        text='Could not find a user with that name.'
                        break

                if message.channel_mentions:
                    if message.channel_mentions>1 or 'voice_channel' not in content[::2]:
                        text='Not in place channel mention found'
                        break

                result={}
                
                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break

                    if name=='nick':
                        result[name]=value
                        continue
                        
                    if name in ('deaf','mute'):
                        value=value.lower()
                        if value=='true':
                            result[name]=True
                            continue
                        elif value=='false':
                            result[name]=False
                            continue
                        else:
                            text=f'Invalid value for {name}, it can be either True or False'
                            break
                        
                    if name=='voice_channel':
                        if is_channel_mention(value):
                            channel=message.channel_mentions[0]
                        else:
                            channel=guild.get_channel(value)
                            if channel is None:
                                text='Did not find that channel name'
                                break
                        if type(channel) is not Channel_voice:
                            text='Bad channel type, it must to be voice channel!'
                            break
                        result[name]=channel
                        continue

                    if name=='role':
                        role=guild.get_role(value)
                        if role is None:
                            text='Did not find that role name!'
                            break
                        user_roles=user.guild_profiles[guild].roles
                            
                        if role in user_roles:
                            new_roles=user_roles.copy()
                            new_roles.remove(role)
                            result['roles']=new_roles
                        else:
                            new_roles=user_roles.copy()
                            new_roles.append(role)
                            result['roles']=new_roles
                        continue

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text=f'Invalid attribute to change {name}. You can change "nick", "deaf", "mute", "voice channel", "role" of a user. Additionally you can add "reason" too.'
                    break
                
                if not text:
                    text=(user,result)
                break
            
            if key=='role':
                limit=len(content)
                if (limit&1)^1:
                    text='Pls write a role\'s name, then key, value pairs.'
                    break
                if limit==1:
                    text='And anything to change?'
                    break
                role=guild.get_role(content[0])
                if role is None:
                    text='Could not find a role with that name.'
                    break

                result={}
                
                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break

                    if name=='name':
                        result[name]=value
                        continue
                        
                    if name in ('mentionable','separated'):
                        value=value.lower()
                        if value=='true':
                            result[name]=True
                            continue
                        elif value=='false':
                            result[name]=False
                            continue
                        else:
                            text=f'Invalid value for {name}, it can be either True or False'
                            break
                        
                    if name=='color':
                        try:
                            result[name]=Color.from_html(value)
                        except ValueError:
                            text='Invalid color'
                            break
                        continue

                    if name=='permissions':
                        if value=='voice':
                            result[name]=Permission.voice
                            continue
                        if value=='text':
                            result[name]=Permission.text
                            continue
                        if value=='none':
                            result[name]=Permission.none
                            continue
                        if value=='general':
                            result[name]=Permission.general
                            continue
                        text='Not predefined permission name'
                        break

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text='Invalid attribute to change. You can change a role\'s name, "separated" and "mentonable" "value", "color" and "permissions" (to preset "voice", "text", "none", "general".'
                    break
                
                if not text: 
                    text=(role,result)
                break

            if key=='emoji':
                if not len(content)&1:
                    text='After emoji pls type key-value pairs'
                    break
                if len(content)==1:
                    text='Done!!'
                    break

                value=content.pop(0)
                
                emoji=parse_emoji(value)
                if emoji:
                    try:
                        emoji=guild.emojis[emoji.id]
                    except KeyError:
                        text='Can not edit that emoji'
                        break
                else:
                    emoji=guild.get_emoji(value)
                    if emoji is None:
                        text='Thats not an emoji'
                        break

                roles=[]
                ename=None

                while content:
                    name=content.pop(0)
                    value=content.pop(0)

                    if name=='name':
                        if not (1<len(value)<33):
                            text='Name too long or short'
                            break
                        
                        if ename is not None:
                            text='Name cannot be duped only role.'

                        ename=value
                        continue

                    if name=='role':
                        role=guild.get_role(value)
                        if role is None:
                            text=f'Could not find role {value}.'
                            break
                        
                        if role in roles:
                            text='You cant add 1 role more times'
                            break

                        roles.append(role)
                        continue

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text=f'Invalid value to change {name}, you can change an emoji\'s "name", "role" (more too) and give a "reason" too.'
                    break


                if not text: 
                    text=(emoji,ename,roles)
                break
                
            if key=='guild':
                limit=len(content)
                if limit&1:
                    text='Pls write key, value pairs.'
                    break
                if limit==0:
                    text='And anything to change?'
                    break

                result={}
                
                index=0
                attach_index=0
                channel_index=0
                
                while index!=limit:
                    name=content[index].lower()
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break

                    if name=='owner':
                        if message.user_mentions and is_user_mention(value):
                            user=message.user_mentions[0]
                        else:
                            user=guild.get_user(value)
                            if user is None:
                                text='Could not find that user!'
                                break
                        
                        if client is guild.owner:
                            if message.author is client.owner:
                                result[name]=user
                            else:
                                text='You do not have permission to do it'
                                break
                        else:
                            'I must be the server owner to change the ownership.'
                            break
                        
                        continue
                    
                    if name=='name':
                        result[name]=value
                        continue

                    if name=='icon':

                        if value.lower()=='none':
                            result[name]=None
                            continue
                            
                        if len(message.attachments)<=attach_index:
                            text='The message has no attachments to change icon'
                            break
                        
                        ext=os.path.splitext(message.attachments[attach_index].name)[1]
                        if len(ext)<2:
                            text='Missing extension.'
                            break
                        ext=ext[1:].lower()
                        
                        if ext not in VALID_ICON_FORMATS:
                            text='Invalid format.'
                            break
                        
                        result[name] = await client.download_attachment(message.attachments[attach_index])
                        attach_index+=1
                        continue

                    if name=='splash':
                        if guild_features.splash not in guild.features:
                            text='The guild has no splash feature.'
                            break

                        if value.lower()=='none':
                            result[name]=None
                            continue

                        if len(message.attachments)<=attach_index:
                            text='The message has no attachments to change splash'
                            break
                        
                        ext=os.path.splitext(message.attachments[attach_index].name)[1]
                        if len(ext)<2:
                            text='Missing extension.'
                            break
                        ext=ext[1:].lower()
                        
                        if ext not in VALID_ICON_FORMATS:
                            text='Invalid format'
                            break
                        
                        result[name] = await client.download_attachment(message.attachments[attach_index])
                        attach_index+=1
                        continue

                    if name=='afk_channel':
                        
                        if value.lower()=='none':
                            result[name]=None
                            continue

                        if message.channel_mentions and is_channel_mention(value):
                            channel=message.channel_mentions[channel_index]
                        else:
                            channel=guild.get_channel(value)
                            if channel is None:
                                text='Could not find that channel!'
                                break

                        if type(channel) is not Channel_voice:
                            text='Afk channel can be only voice channel'
                            break
                        
                        result[name]=channel
                        channel_index+=1
                        continue

                    if name=='system_channel':
                        
                        if value.lower()=='none':
                            result[name]=None
                            continue

                        if message.channel_mentions and is_channel_mention(value):
                            channel=message.channel_mentions[channel_index]
                        else:
                            channel=guild.get_channel(value)
                            if channel is None:
                                text='Could not find that channel!'
                                break

                        if type(channel) is not Text_voice:
                            text='System channel can be only text channel'
                            break
                        
                        result[name]=channel
                        channel_index+=1
                        continue

                    if name in ('region','voice_region'):
                        try:
                            region=voice_regions.values[value.lower()]
                        except KeyError:
                            text='Unknown voice region'
                            continue

                        result[name]=region
                        continue

                    if name=='afk_timeout':
                        try:
                            afk_timeout=int(value)
                        except ValueError:
                            text='Timeout must be integer.'
                            break

                        if afk_timeout not  in (60,300,900,1800,3600):
                            text='Afk timeout should be 60, 300, 900, 1800, 3600 seconds.'
                            break

                        result[name]=afk_timeout
                        continue

                    if name in ('verification','verification_level'):
                        try:
                            level=verification_levels.values[int(value)]
                        except KeyError:
                            text='Invalid verification_level'
                            break
                        except ValueError:
                            for element in verification_levels.values.values():
                                if value in element.names:
                                    level=element
                                    break
                            else:
                                text='Invalid verification_level'
                                break
                            
                        result['verification_level']=level
                        continue

                    if name=='content_filter': 
                        try:
                            level=content_filter_levels.values[int(value)]
                        except KeyError:
                            text='Invalid content filter'
                            break
                        except ValueError:
                            for element in content_filter_levels.values.values():
                                if value in element.names:
                                    level=element
                                    break
                            else:
                                text='Invalid content filter'
                                break
                            
                        result[name]=level
                        continue
                        
                    if name in ('message_notification_level','message_notification'):
                        try:
                            level=message_notification_levels.values[int(value)]
                        except KeyError:
                            text='Invalid message notification level'
                            break
                        except ValueError:
                            for element in message_notification_levels.values.values():
                                if value in element.names:
                                    level=element
                                    break
                            else:
                                text='Invalid message notification level'
                                break
                            
                        result['message_notification_level']=level
                        continue
                    
                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text='Invalid attribute to change. You can change: "name", "icon", "splash", ' \
                        '"afk_channel", "system_channel", "owner", "region", "afk_timeout", ' \
                        '"verification_level", "content_filter", "message_notification_level", ' \
                        'and add an additional "reason" too.'
                    break
                
                if not text: 
                    text=result
                break
            
            break
        if type(text) is not str:
            try:
                if reason:
                    reason=smart_join([f'Executed by {message.author:f}, with reason:',*reason.split()],255)
                else:
                    reason=f'Executed by {message.author:f}'
                if key=='user':
                    await client.guild_user_edit(guild,text[0],**text[1],reason=reason)
                elif key=='role':
                    await client.role_edit(text[0],**text[1],reason=reason)
                elif key=='emoji':
                    await client.emoji_edit(*text,reason=reason)
                elif key=='guild':
                    await client.guild_edit(guild,**text,reason=reason)
            except Forbidden:
                text='Access denied'
            except ValueError as err:
                text=err.args[0]
            else:
                text='OwO'
                
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['edit'])


    @on_command
    async def move(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        key=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            if not content:
                break
            key=content.pop(0)
            if key=='channel':
                if len(content) not in (2,3):
                    text='Moving channel\ss formula: "channel name" ("category name") "position"'
                    break
                if is_channel_mention(content[0]):
                    channel=message.channel_mentions[0] 
                else:
                    channel=guild.get_channel(content[0])
                    if channel is None:
                        text='Channel not found.'
                        break
                if len(content)==3:
                    index=content[2]
                else:
                    index=content[1]
                try:
                    index=int(index)
                except KeyError:
                    text='Index should be number, right?'
                    break
                if len(content)==2:
                    category=None
                else:
                    category=content[1]
                    if category=='guild':
                        category=guild
                    else:
                        if is_channel_mention(content[2]):
                            category=message.channel_mentions[-1]
                        else:
                            category=guild.get_channel(category)
                        if not category:
                            text='Cagory not found.'
                            break
                        if category.type!=4:
                            text='You can move channels only to Category channel or to the guild.'
                            break

                if not text:
                    text=(channel,index,category)
                break
            if key=='role':
                if len(content)!=2:
                    text='"Role name" and "index" please!'
                    break
                role=guild.get_role(content[0])
                if role is None:
                    text='Role not found.'
                    break
                try:
                    index=int(content[1])
                except ValueError:
                    text='Valid number desu!'
                    break
                text=(role,index)
                break
            if key=='user':
                if len(content) not in (1,2):
                    text='("user name/ping") and "Channel name/ping" desu!'
                    break

                if len(content)==2:
                    name=content.pop(0)
                    if message.user_mentions and is_user_mention(name):
                        user=message.user_mentions[0]
                    else:
                        user=guild.get_user(name)
                        if user is None:
                            text='Could not find a user with that name!'
                            break
                else:
                    user=message.author
                    
                state=guild.voice_states.get(user.id,None)
                if not state:
                    text='Can move only a user from voice channel'
                    break
                
                name=content[0]
                if message.channel_mentions and is_channel_mention(name):
                    channel=message.channel_mentions[0]
                else:
                    channel=guild.get_channel(name)
                    if channel is None:
                        text='Could not find that channel!'
                        break
                if channel.type!=2:
                    text='Can move user only from voice channel to voice channel!'
                    break
                if channel is state.channel:
                    text='Done, i guess (?)'
                    break
                text=(user,channel)
                
            break
        
        if type(text) is not str:
            try:
                reason=f'Executed by {message.author:f}'
                if key=='channel':
                    await client.channel_guild_move(*text,reason=reason)
                elif key=='role':
                    await client.role_move(*text,reason=reason)
                elif key=='user':
                    await client.user_move(*text,reason=reason)
            except Forbidden:
                text='Access denied!'
            else:
                text='yayyyy'
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['move'])

    
    @on_command
    async def delete(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        key=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            if len(content) not in (2,3):
                text='type, value, then reason if you wish to.'
                break
            
            key=content.pop(0)
            value=content.pop(0)
            if key=='role':
                role=guild.get_role(value)
                if role is None:
                    text='Role not found'
                    break
                text=role
                break
            if key=='channel':
                channel=guild.get_channel(value)
                if channel is None:
                    text='Channel not found'
                    break
                text=channel
                break
            if key=='emoji':
                text=parse_emoji(value)
                if text:
                    try:
                        text=guild.emojis[text.id]
                    except KeyError:
                        text='Can not edit that emoji'
                        break
                else:
                    text=guild.get_emoji(value)
                    if text is None:
                        text='Thats not an emoji'
                        break

                break
            
            break
        
        if type(text) is str:
            if text:
                await client.message_create(message.channel,text)
            else:
                await client.message_create(message.channel,embed=HELP['delete'])
            return
        
        if content:
            reason=smart_join([f'Executed by {message.author:f}, with reason:',*content[0].split()],255)
        else:
            reason=f'Executed by {message.author:f}'
            
        try:
            if key=='role':
                await client.role_delete(text,reason)
            elif key=='channel':
                await client.channel_delete(text,reason)
            elif key=='emoji':
                await client.emoji_delete(text,reason)
        except Forbidden:
            text='Access denied!'
        else:
            text='yayyyy'
        await client.message_create(message.channel,text)
            
        

##    @on_command.add('book')
##    async def on_command_book(client,message,content):
##        pages=({'content':'import base64\n\npage1/3'},{'content':'uwu\n\npage2/3'},{'content':'text2\n\npage3/3'})
##        pagination(client,message.channel,pages)


##    @on_command
##    async def satania(client,message,content):
##        message = await client.message_create(message.channel,'waiting for satania emote')
##        try:
##            emoji,user = await wait_for_emoji(client,message,lambda emoji,user:('satania' in emoji.name.lower()),60.)
##        except TimeoutError:
##            return
##        finally:
##            try:
##                await client.message_delete(message)
##            except (Forbidden,HTTPException):
##                pass
##        await client.message_create(message.channel,str(emoji)*5)

##    @on_command.add('embed')
##    async def on_command_embed(client,message,content):
##        content='Here\'s a hug for Nyansia ! OwO'
##        embed=Embed( \
##            title='Nyanmatsu hugs Nyansia',
##            url='https://discordapp.com',
##            color=Color.from_html('#ff4465'),
##                )
##        embed.image=Embed_image('https://cdn.discordapp.com/embed/avatars/0.png')
##        
##        await client.message_create(message.channel,content,embed)

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
        async for message in get_message_iterator(client,message.channel):
            messages.append(message)
            limit-=1
            if limit:
                continue
            break

        await client.message_delete_multiple(messages,reason=f'Called by {author:f}')

    MAGIC_PATTERN=re.compile('.*?(p[lw][sz]|p[lw]ea[sz]e|desu|kudasai)[\.\!]*?',re.I)
    
    @on_command
    async def hug(client,message,content):
        channel=message.channel
        guild=message.guild
        target=message.author
        if content:
            if message.user_mentions and is_user_mention(content):
                target=message.user_mentions[0]
            elif guild is not None:
                user=guild.get_user(content)
                if user is not None:
                    target=user
            
        await client.message_create(channel,'And what is the magic word?')
        try:
            await wait_for_message(client,message.channel,lambda message,pattern=MAGIC_PATTERN,author=message.author:message.author is author and re.match(pattern,message.content),30.)
        except TimeoutError:
            return
        await client.message_create(channel,f'{client.mention_at(guild)} hugs {target.mention_at(guild)}')

    @on_command
    async def say(client,message,content):
        channel=message.channel
        
        message_to_delete1 = await client.message_create(channel,'prepared')

        try:
            message_to_delete2 = await wait_for_message(client,channel,lambda message:True,30.)
        except TimeoutError:
            try:
                await client.message_delete(message_to_delete1)
            except Forbidden:
                pass
            return
        try:
            await client.message_delete_multiple([message_to_delete1,message_to_delete2])
        except Forbidden:
            pass
            
        await client.message_create(channel,message_to_delete2.content)


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
    async def create(client,message,content):
        guild=message.guild
        if guild is None:
            return
        text=''
        content=filter_content(content)
        key=''
        reason=''
        
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            
            key=content.pop(0)
            
            if not content:
                break
            
            if key=='role':
                limit=len(content)
                if limit&1==0:
                    text='role name, then key-value pairs.'
                    break

                result={}
                
                value=content[0]
                
                role=guild.get_role(value)
                if role is not None:
                    text='A role already has that name!'
                    break
                
                result[key]=value
                    
                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break
                        
                    if name in ('mentionable','separated'):
                        value=value.lower()
                        if value=='true':
                            result[name]=True
                            continue
                        elif value=='false':
                            result[name]=False
                            continue
                        else:
                            text=f'Invalid value for {name}, it can be either True or False'
                            break
                        
                    if name=='color':
                        try:
                            result[name]=Color.from_html(value)
                        except ValueError:
                            text='Invalid color'
                            break
                        continue

                    if name=='permissions':
                        if value=='voice':
                            result[name]=Permission.voice
                            continue
                        if value=='text':
                            result[name]=Permission.text
                            continue
                        if value=='none':
                            result[name]=Permission.none
                            continue
                        if value=='general':
                            result[name]=Permission.general
                            continue
                        text='Not predefined permission name'
                        break

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue
                    
                    text=f'You can not set {key}, but you can set additionally: "mentionable", "separated",' \
                          '"color" <html format>, "permissions" <voice/text/nne/genera>, "reason" for now'
                    break
                
                if not text: 
                    text=result
                    
                break
            if key=='emoji':
                limit=len(content)
                
                if limit&1==0:
                    text='Emoji name followed by key - value pairs (role <rolename> / reason <reason>)'
                
                value=content[0]
                
                if not (1<len(value)<33):
                    text='Too short or too long name'
                    break
                
                count_animated=0
                for emoji in guild.emojis.values():
                    if emoji.name==value:
                        exists=True
                        break
                    if emoji.animated:
                        count_animated+=1
                else:
                    exists=False

                if exists:
                    text='An emoji already exists with that name at the guild'
                    break
                
                if not message.attachments:
                    text='The message has no attachments'
                    break

                ext=os.path.splitext(message.attachments[0].name)[1]
                if len(ext)<2:
                    text='Missing extension'
                    break
                ext=ext[1:].lower()
                
                if ext in VALID_ICON_FORMATS:
                    if len(guild.emojis)-count_animated==50:
                        text='The guild already reached the limit of non animated emojis'
                        break
                    
                elif ext in VALID_ICON_FORMATS_EXTENDED:
                    if count_animated==50:
                        text='The guild already reached the limit of animated emojis'
                        break
                else:
                    text='Invalid format'
                    break

                roles=[]
                ename=value

                index=1
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1
                    
                    if name=='role':
                        role=guild.get_role(value)
                        if role is None:
                            text=f'Could not find role: {value}.'
                            break
                        
                        if role in roles:
                            text='You cant add 1 role more times'
                            break

                        roles.append(role)
                        continue

                    if name=='reason':
                        if reason:
                            text='Reason key can not be duped.'
                        reason=value
                        continue

                    text=f'Invalid value {name}, you can use "role" (more too) and give a "reason" too.'
                    break

                if text:
                    break
                
                image = await client.download_attachment(message.attachments[0])
                
                text=(ename,image,roles)

                break
                
            break
        
        if type(text) is not str:
            try:
                if reason:
                    reason=smart_join([f'Executed by {message.author:f}, with reason:',*reason.split()],255)
                else:
                    reason=f'Executed by {message.author:f}'
                
                if key=='role':
                    await client.role_create(guild,**text,reason=reason)
                elif key=='emoji':
                    await client.emoji_create(guild,*text,reason)
                    
            except Forbidden:
                text='Access denied!'
            except ValueError as err:
                text=err.args[0]
            else:
                text='yayyyy'
        
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['create'])
        

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

    @on_command.add('type')
    async def on_command_type(client,message,content):
        await client.typing(message.channel)

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

##    @on_command
##    async def owner_invite(client,message,content):
##        if message.author is not client.owner:
##            return
##        
##        guild=client.get_guild(content)
##        
##        if guild is None:
##            return
##        
##        try:
##            invite = await client.invite_create(guild.channels[0],0,1)
##        except Forbidden:
##            return
##        
##        channel = await client.channel_private_create(message.author)
##        await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')
        
    @on_command
    async def invite_by_code(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return
        
        err=False
        if not content:
            err=True
        elif len(content)>8:
            err=True
        else:
            try:
                invite = await client.invite_get(content)
            except Forbidden:
                invite=None
            except HTTPException:
                err=True

        if err:
            text='Invalid Invite code'
        elif invite:
            text=f'{pchunkify(invite,show_code=True)[0]}\n{invite.url}'
        else:
            text='Permissions denied'

        await client.message_create(message.channel,text)

    @on_command
    async def invite_delete_by_code(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return

        err=False
        if not content:
            err=True
        elif len(content)>16:
            err=True
        else:
            try:
                invite = await client.invite_delete_by_code(content)
            except Forbidden:
                invite=None
            except HTTPException:
                err=True

        if err:
            text='Invalid Invite code'
        elif invite:
            text=f'{pchunkify(invite,show_code=True)[0]}\n{invite.url}'
        else:
            text='Permissions denied'

        await client.message_create(message.channel,text)

    @on_command
    async def invite_clear(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return
        
        try:
            with client.keep_typing(message.channel):
                invites = await client.invites_of_guild(guild)
                for invite in invites:
                    await sleep(0.5,client.loop)
                    try:
                        await client.invite_delete(invite)
                    except HTTPException:
                        pass
        except Forbidden:
            text='Failed'
        else:
            text=f'Succes, {len(invites)} got deleted'
            
        await client.message_create(message.channel,text)

    #client side only. Discord clients request with_count always anyways
##    @on_command
##    async def invite_mod(client,message,content):
##        guild=message.guild
##        if guild is None or not guild.permissions_for(message.author).can_administrator:
##            return
##        
##        try:
##            with client.keep_typing(message.channel):
##                invites = await client.invites_of_guild(guild)
##                for invite in invites:
##                    await sleep(0.5,client.loop)
##                    if invite.online_count is not None:
##                        value=False
##                    else:
##                        value=True
##                    try:
##                        await client.invite_update(invite,value)
##                    except HTTPException:
##                        pass
##        except Forbidden:
##            text='Failed'
##        else:
##            text=f'Succes'
##            
##        await client.message_create(message.channel,text)
            
##    @on_command
##    async def wait2where(client,message,content):
##        channel=message.channel
##        private = await client.channel_private_create(message.author)
##        await client.message_create(channel,'Waiting on any message from you here and at dm')
##
##        
##        future=wait_one(client.loop)
##        case=lambda message,author=message.author:message.author is author
##        event=client.events.message_create
##        
##        wrapper1=waitfor_wrapper(client,wait_and_continue(future,case,channel,event),60.)
##        wrapper2=waitfor_wrapper(client,wait_and_continue(future,case,private,event),60.)
##        
##        try:
##            result = await future
##        except TimeoutError:
##            await client.message_create(channel,'Time is over')
##            return
##        
##        wrapper1.cancel()
##        wrapper2.cancel()
##        
##        await client.message_create(channel,result.content)

    @on_command
    async def prune(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_administrator:
            return
        try:
            if len(content)==5 and content.lower()=='prune':
                result = await client.guild_prune(guild,16,reason=f'Executed by {message.author:f}.')
                text=f'Pruned {result} users.'
            else:
                result = await client.guild_prune_estimate(guild,16)
                text=f'{result} users to be pruned'
        except Forbidden:
            text='Acces denied'

        await client.message_create(message.channel,text)

    @on_command
    async def kick(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_kick_user:
            return

        content=filter_content(content)
        if not content:
            await client.message_create(message.channel,'And who, if i can ask so?')
            return

        name=content.pop(0)
        if is_user_mention(name) and message.user_mentions:
            user=message.user_mentions[0]
        else:
            user=guild.get_user(name)
            if user is None:
                await client.message_create(message.channel,'Could not find that user')
                return

        reason=smart_join(content,170)
            
        if content:
            reason=f'Executed by {message.author:f}, reason: {reason}'
        else:
            reason=f'Executed by {message.author:f}'

        await client.guild_user_kick(guild,user,reason)
        await client.message_create('ExeCUTEd')

##    @on_command
##    async def language(client,message,content):
##        guild=message.guild
##        target=None
##        if content:
##            if message.user_mentions:
##                target=message.user_mentions[0]
##            elif guild is not None:
##                target=guild.get_user(content)
##        if target is None:
##            target=message.author
##        
##        await client.message_create(message.channel,f'If i can have a guess {target.mention_at(guild)}\' client\'s language is: {target.language}')

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
            x=random(0,9)
            y=random(0,9)
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

##    @on_command.add('pinner')
##    async def on_command_pinner(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if guild.permissions_for(message.author).can_administrator:
##            pinner(client,message.channel)

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
    async def ban(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_ban_user:
            return

        content=filter_content(content)
        if not content:
            await client.message_create(message.channel,'And who, if i can ask so?')
            return

        name=content.pop(0)
        if is_user_mention(name) and message.user_mentions:
            user=message.user_mentions[0]
        else:
            user=guild.get_user(name)
            if user is None:
                await client.message_create(message.channel,'Could not find that user')
                return
        days=0
        if content and content[0].isdigit():
            value=int(content[0])
            if -1<value<8:
                content.pop(0)
                days=value

        if content:
            content.insert(0,'Executed by {message.author:f}, reason:')
            reason=smart_join(content,255)
        else:
            reason=f'Executed by {message.author:f}'

        await client.guild_user_ban(guild,user,days,reason)
        await client.message_create('ExeCUTEd')

    @on_command
    async def ban_get_by_id(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_ban_user:
            return
        
        if not is_id(content):
            message = await client.message_create('Pls type an id too')
            await sleep(30.,client.loop)
            try:
                await client.message_delete(message)
            except (Forbidden,HTTPException):
                pass
            return
        
        id_=int(content)
        
        try:
            user,reason = await client.guild_ban_get_by_id(guild,id_)
        except HTTPException:
            embed=Embed(description=f'{guild.name} {guild.id} has no ban for id: {id_}')
        except Forbidden:
            return
        else:
            if reason is None:
                embed=Embed()
            else:
                embed=Embed(title='Reason:',description=reason)
            embed.author=Embed_author(user.avatar_url_as(size=64),user.full_name)

        await client.message_create(message.channel,embed=embed)

    @on_command
    async def unban(client,message,content):
        guild=message.guild
        if guild is None or not guild.permissions_for(message.author).can_ban_user or not content:
            return
        
        content=filter_content(content)
        value=content.pop(0)
        
        if not is_id(value):
            message = await client.message_create('Pls type an id too')
            await sleep(30.,client.loop)
            try:
                await client.message_delete(message)
            except (Forbidden,HTTPException):
                pass
            return

        id_=int(value)

        try:
            await client.guild_user_unban_by_id(guild,id_,reason)
        except HTTPException:
            embed=Embed(description=f'{guild.name} {guild.id} has no ban for id: {id_}')
        except Forbidden:
            return
        else:
            user = await client.user_get_by_id(id_)
            if len(content):
                embed=Embed('Unbanned with reason:',smart_join(content.split(),255))
            else:
                embed=Embed('Unbanned')
            embed.author=Embed_author(user.avatar_url_as(size=64),user.full_name)
        await client.message_create(message.channel,embed=embed)


    @on_command
    async def leave_guild(client,message,content):
        guild=message.guild
        if guild is None or guild.owner is not message.author:
            return
        await client.guild_leave(guild)

##    @on_command
##    async def guild_delete(client,message,content):
##        guild=message.guild
##        if guild is None or guild.owner is not client or message.author is not client.owner:
##            return
##        await client.guild_delete(guild)

##    @on_command
##    async def guild_create(client,message,content):
##        if message.author is not client.owner and len(client.guilds)>9:
##            return
##        guild = await client.guild_create(name='uwu yayyyy',
##            channels=[cr_pg_channel_object(name='channel1',type_=Channel_text),
##                      cr_pg_channel_object(name='channel2',type_=Channel_text),
##                      cr_pg_channel_object(name='channel3',type_=Channel_text),])
##
##        await sleep(2.,client.loop) #wait for dispatch
##        invite = await client.invite_create_pref(guild,0,0)
##        channel = await client.channel_private_create(message.author)
##        await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')

##    @on_command
##    async def load_emotes(client,message,content):
##        with client.keep_typing(message.channel):
##            while True:
##                try:
##                    id_=int(content)
##                except ValueError:
##                    text='Thats not an id.'
##                    break
##                try:
##                    message = await client.message_get(message.channel,id_)
##                except Forbidden:
##                    text='I have no permission to do that!'
##                    break
##                except HTTPException:
##                    text='The message does not exsists!'
##                    break
##                
##                #this might take for a while
##                await client.reaction_load_all(message)
##
##                if message.reactions is None:
##                    text='None'
##                    break
##
##                result=[]
##                for emoji,line in message.reactions.items():
##                    for user in line:
##                        if len(result)==20:
##                            break
##                        result.append(f'{emoji:e} - {user:f}')
##
##                text='\n'.join(result)
##                break
##
##        await client.message_create(message.channel,text)
##
##    @on_command
##    async def webhook_test(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##        
##        webhooks = await client.webhook_get_guild(guild)
##
##        if not webhooks:
##            return
##        
##        webhook=webhooks[0]
##        
##        await client.webhook_send(webhook,embed=Embed('OwO whats this?'),name=message.author.name,avatar_url=message.author.avatar_url,file=b'UwU',filename='UwU')
##
##    @on_command
##    async def webhook_get_by_id(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        try:
##            id_=int(content)
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_get_by_token(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        await client.message_delete(message)
##        
##        content=filter_content(content)
##        try:
##            id_=int(content[0])
##        except ValueError:
##            return
##
##        token=content[1]
##        
##        webhook = await client.webhook_get_token(id_,token)
##
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_create(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        if not (1<len(content)<33):
##            return
##        
##        if message.attachments:
##            ext=os.path.splitext(message.attachments[0].name)[1]
##            if len(ext)<2:
##                return
##            ext=ext[1:].lower()
##            
##            if ext not in VALID_ICON_FORMATS:
##                return
##            
##            image = await client.download_attachment(message.attachments[0])
##        else:
##            image=b''
##
##        webhook = await client.webhook_create(message.channel,content,image)
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_delete_by_id(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##        
##        try:
##            id_=int(content)
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##        
##        await client.webhook_delete(webhook)
##
##        await client.message_create(message.channel,webhook.name)
##        
##        
##    @on_command
##    async def webhook_delete_by_token(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##        
##        content=filter_content(content)
##        try:
##            id_=int(content[0])
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##
##        await client.webhook_delete_token(webhook)
##
##        await client.message_create(message.channel,webhook.name)
##
##    @on_command
##    async def webhook_edit(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        content=filter_content(content)
##
##        if len(content)<2:
##            return
##
##        try:
##            id_=int(content[0])
##        except ValueError:
##            return
##
##        webhook = await client.webhook_get(id_)
##        
##        if 'name' in content:
##            name=''.join([chr(random(65,90)) for i in range(10)])
##        else:
##            name=''
##
##        if 'avatar' in content:
##            if message.attachments:
##                ext=os.path.splitext(message.attachments[0].name)[1]
##                if len(ext)<2:
##                    return
##                ext=ext[1:].lower()
##                
##                if ext not in VALID_ICON_FORMATS:
##                    return
##                    
##                avatar = await client.download_attachment(message.attachments[0])
##            else:
##                avatar=None
##        else:
##            avatar=b''
##
##        token=('token' in content)
##
##        if 'channel' in content:
##            channels=guild.text_channels
##            try:
##                channels.remove(webhook.channel)
##            except ValueError:
##                pass
##            channel=choice(channels)
##        else:
##            channel=None
##         
##        if token:
##            await client.webhook_edit_token(webhook,name,avatar,channel)
##        else:
##            await client.webhook_edit(webhook,name,avatar,channel)
##
##        await client.message_create(message.channel,webhook.name,)
##
##    @on_command
##    async def webhook_from_url(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        await client.message_delete(message)
##        
##        webhook = await client.webhook_get(Webhook.from_url(content).id)
##
##        await client.message_create(message.channel,webhook.name,)

#TODO: get a working integation id for make tests with it

##    @on_command
##    async def create_integration(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        integration = await client.integration_create(guild,'twitch',456456)
##
##        await client.message_create('owo')


    @on_command
    async def logs(client,message,content):
        guild=message.guild
        if guild is None:
            return
        if message.author is not client.owner:
            return

        kwargs={}
        all_=0
        text=''
        
        while True:
            if not content:
                break
            content=filter_content(content)
            if len(content)&1:
                text='key value pairs please'
                break
            index=0
            while index<len(content):
                key=content[index].lower()
                index+=1
                value=content[index]
                index+=1

                if key=='user':
                    if key in kwargs:
                        text=f'dupe key {key}'
                        break
                    if message.user_mentions is not None and is_user_mention(value):
                        user=message.user_mentions[0]
                    else:
                        user=guild.get_user(value)
                        if user is None and value.isdigit():
                            user=guild.users.get(int(value))
                    if user is None:
                        text='Could not find that user'
                        break
                    kwargs[key]=user
                    continue
                
                if key=='event':
                    if key in kwargs:
                        text=f'dupe key {key}'
                        break
                    if value.isdigit():
                        try:
                            event=audit_log_events.values[int(value)]
                        except KeyError:
                            text=f'Unknown event {value}'
                            break
                    else:
                        try:
                            event=getattr(audit_log_events,value.upper())
                        except AttributeError:
                            text=f'Unknown event {value}'
                            break

                        if type(event) is not audit_log_events:
                            text=f'Unknown event {value}'
                            break
                        continue

                    kwargs[key]=event
                    continue

                if key=='all':
                    if all_:
                        text=f'dupe key {key}'
                        break
                    value=value.lower()
                    if value=='now':
                        all_=1
                    elif value=='1b1':
                        all_=2
                    else:
                        text=f'Unknown value {value}'
                        break
                    continue
                
                text=f'Unknown key {key}'
                break
            break
        
        if text:
            await client.message_create(message.channel,text)
            return

        if all_==0:
            logs = await client.guild_audit_logs(guild,**kwargs)
        elif all_==1:
            iterator=Audit_log_iterator(client,guild,**kwargs)
            await iterator.load_all()
            logs=iterator.transform()
        else: #all_==2
            iterator=Audit_log_iterator(client,guild,**kwargs)
            async for entry in iterator:
                pass
            logs=iterator.transform()
            
        pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(logs)])

##    @on_command
##    async def guild_get(client,message,content):
##        guild=message.guild
##        if guild is None:
##            return
##        if message.author is not client.owner:
##            return
##
##        if not content:
##            return
##        
##        try:
##            id_=int(content)
##        except ValueError:
##            return
##
##        try:
##            guild = await client.guild_get(id_)
##        except Forbidden:
##            return
##        
##        await client.message_create(message.channel,f'{guild.name}\n{guild.icon_url}')

##    @on_command
##    async def emoji_get(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None or not content:
##            return
##
##        content=filter_content(content)
##        
##        try:
##            emoji_id=int(content[0])
##        except ValueError:
##            pass
##
##        #for testing purpose
##        if len(content)>1:
##            try:
##                guild_id=int(content[1])
##            except ValueError:
##                pass
##            try:
##                guild=GUILDS[guild_id]
##            except KeyError:
##                guild=Unknown('Guild',guild_id) #we will get forbidden
##        try:
##            emoji = await client.emoji_get(guild,emoji_id)
##        except Forbidden:
##            await client.message_create(message.channel,'not part of that guild')
##        else:
##            await client.message_create(message.channel,emoji.as_emoji)
##
##    @on_command
##    async def all_emojis(client,message,content):
##        guild=message.guild
##        if message.author is not client.owner or guild is None:
##            return
##
##        emojis = await client.emoji_get_all(guild)
##        await client.message_create(message.channel,smart_join((emoji.as_emoji for emoji in emojis),2000))

    @on_command
    @cooldown(30.,'user',handler=cooldown_handler())
    async def cheer(client,message,content):
        await client.message_create(message.channel,embed=Embed('CHEERS!',color=Color.d_purple))

    @on_command
    @cooldown(60.,'c',case='cheers')
    async def almost_cheer(client,message,content):
        await client.message_create(message.channel,embed=Embed(BUILTIN_EMOJIS['cheese'].as_emoji,color=Color.d_purple))

    @on_command
    @cooldown(60.,'g',)
    async def cheese(client,message,content):
        await client.message_create(message.channel,embed=Embed(BUILTIN_EMOJIS['cheese'].as_emoji,color=Color.d_purple))

##    #if we use prefix as str/list
##    @on_command
##    async def add_prefix(client,message,content):
##        if message.author is not client.owner:
##            return
##        prefixes=client.events.message_create.prefix
##        if type(prefixes) is str:
##            prefixes=[prefixes]
##        prefixes.append(content)
##        client.events.message_create.update_prefix(prefixes)
##        await client.message_create(message.channel,'OwO')

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
    async def create_pow(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command.'
                break
            if len(content)<4:
                text='And who\'s / what\'s to change and to what to change?\nThe correct formula is the following:\n"Channel Target Allow Deny <reason>".'
                break

            channel_name=content[0]                            
            
            target_name=content[1]

            try:
                allow=int(content[2])
            except ValueError:
                text='Allow must be number'
                break

            try:
                deny=int(content[3])
            except ValueError:
                text='Deny must be number'
                break

            if message.channel_mentions is not None and is_channel_mention(channel_name):
                channel=message.channel_mentions[0]
            else:
                if channel_name.isdigit():
                    try:
                        channel=guild.all_channel[int(channel_name)]
                    except KeyError:
                        channel=guild.get_channel(channel_name)
                        if channel is None:
                            text='Could not find that channel'
                            break
            while True:
                if target_name.isdigit():
                    target_id=int(target_name)
                    try:
                        target=guild.users[target_id]
                        break
                    except KeyError:
                        pass
                    try:
                        target=guild.all_role[target_id]
                        break
                    except KeyError:
                        pass

                if message.role_mentions is not None and is_role_mention[target_name]:
                    target=message.role_mentions[0]
                    break
                
                if message.user_mentions is not None and is_user_mention(target_name):
                    target=message.user_mentions[0]
                    break
                
                target=guild.get_role(target_name)
                if target is not None:
                    break

                target=guild.get_user(target_name)
                if target is not None:
                    break
                
                text='Could not find that target!'
                break
            
            if text:
                break

            if len(content)>4:
                reason=content[4]
            else:
                reason=None

            try:
                await client.permission_ow_create(channel,target,allow,deny,reason)
            except Forbidden:
                text='Access denied'
            except HTTPException:
                text='Cannot do that!'
            else:
                text='Pat me!'
            break

        await client.message_create(message.channel,text)

    @on_command
    async def edit_pow(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command.'
                break
            if len(content)<4:
                text='And who\'s / what\'s to change and to what to change?\nThe correct formula is the following:\n"Channel Target Allow Deny <reason>".'
                break

            channel_name=content[0]                            
            
            target_name=content[1]

            try:
                allow=int(content[2])
            except ValueError:
                text='Allow must be number'
                break

            try:
                deny=int(content[3])
            except ValueError:
                text='Deny must be number'
                break

            if message.channel_mentions is not None and is_channel_mention(channel_name):
                channel=message.channel_mentions[0]
            else:
                if channel_name.isdigit():
                    try:
                        channel=guild.all_channel[int(channel_name)]
                    except KeyError:
                        channel=guild.get_channel(channel_name)
                        if channel is None:
                            text='Could not find that channel'
                            break
            while True:
                if target_name.isdigit():
                    target_id=int(target_name)
                    try:
                        target=guild.users[target_id]
                        break
                    except KeyError:
                        pass
                    try:
                        target=guild.all_role[target_id]
                        break
                    except KeyError:
                        pass

                if message.role_mentions is not None and is_role_mention[target_name]:
                    target=message.role_mentions[0]
                    break
                
                if message.user_mentions is not None and is_user_mention(target_name):
                    target=message.user_mentions[0]
                    break
                
                target=guild.get_role(target_name)
                if target is not None:
                    break

                target=guild.get_user(target_name)
                if target is not None:
                    break
                
                text='Could not find that target!'
                break
            
            if text:
                break

            for overwrite in channel.overwrites:
                if overwrite.target is target:
                    break
            else:
                text='Could not find permission overwrite on that user'
                break
            
            if len(content)>4:
                reason=content[4]
            else:
                reason=None

            try:
                await client.permission_ow_edit(channel,overwrite,allow,deny,reason)
            except Forbidden:
                text='Access denied'
            except HTTPException:
                text='Cannot do that!'
            else:
                text='Pat me!'
            break

        await client.message_create(message.channel,text)

    @on_command
    async def delete_pow(client,message,content):
        guild=message.guild
        if guild is None:
            return
        content=filter_content(content)
        text=''
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command.'
                break
            if len(content)<4:
                text='And who\'s / what\'s to change and to what to change?\nThe correct formula is the following:\n"Channel Target Allow Deny <reason>".'
                break

            channel_name=content[0]                            
            
            target_name=content[1]

            if message.channel_mentions is not None and is_channel_mention(channel_name):
                channel=message.channel_mentions[0]
            else:
                if channel_name.isdigit():
                    try:
                        channel=guild.all_channel[int(channel_name)]
                    except KeyError:
                        channel=guild.get_channel(channel_name)
                        if channel is None:
                            text='Could not find that channel'
                            break
            while True:
                if target_name.isdigit():
                    target_id=int(target_name)
                    try:
                        target=guild.users[target_id]
                        break
                    except KeyError:
                        pass
                    try:
                        target=guild.all_role[target_id]
                        break
                    except KeyError:
                        pass

                if message.role_mentions is not None and is_role_mention[target_name]:
                    target=message.role_mentions[0]
                    break
                
                if message.user_mentions is not None and is_user_mention(target_name):
                    target=message.user_mentions[0]
                    break
                
                target=guild.get_role(target_name)
                if target is not None:
                    break

                target=guild.get_user(target_name)
                if target is not None:
                    break
                
                text='Could not find that target!'
                break
            
            if text:
                break

            for overwrite in channel.overwrites:
                if overwrite.target is target:
                    break
            else:
                text='Could not find permission overwrite on that user'
                break
            
            if len(content)>2:
                reason=content[2]
            else:
                reason=None

            try:
                await client.permission_ow_delete(channel,overwrite,reason)
            except Forbidden:
                text='Access denied'
            except HTTPException:
                text='Cannot do that!'
            else:
                text='Pat me!'
            break

        await client.message_create(message.channel,text)

    @on_command
    async def test_download(client,message,content):
        if message.attachments is None or message.author is not client.owner:
            return

        file = await client.download_url(message.attachments[0].url)
        await client.message_create_file(message.channel,file,filename=message.attachments[0].name,content='Here is your file!')

    @on_command
    async def test_files(client,message,content):
        if message.author is not client.owner:
            return
        files=[(b'UwU','UwU'),(b'OwO','OwO'),(b'0w0',None)]
        await client.message_create_files(message.channel,files,'Did it work OwO?')

    @on_command
    async def test_files1(client,message,content):
        if message.author is not client.owner:
            return
        files=[(b'UwU','UwU')]
        await client.message_create_files(message.channel,files,'Did it work OwO?')
        
    @on_command
    async def bypass_connection_check(client,message,content):
        if message.author is not client.owner:
            return
        try:
            data = await client.http.client_connections(client)
        except Exception as err:
            content=repr(err)
        else:
            content=repr(data)
            
        await client.message_create(message.channel,content)

    @on_command
    async def test_connection(client,message,content):
        if message.author is not client.owner:
            return
        try:
            connections = await client.client_connections()
        except Exception as err:
            content=repr(err)
        else:
            content=connect(connections.values)

        await client.message_create(message.channel,content)

    @on_command
    async def edit_name(client,message,content):
        try:
            await client.client_edit(name=content)
        except ValueError as err:
            text=err.args[0]
        except HTTPException as err:
            text=err.args[0]
        except Forbidden:
            text='Forbidden'
        else:
            text='Kyaaaa'
        await client.message_create(message.channel,text)

    @on_command
    async def edit_avatar(client,message,content):
        if message.author is not client.owner:
            return

        if message.attachments is not None:
            file = await client.download_url(message.attachments[0].url)
        else:
            file=None

        try:
            await client.client_edit(avatar=file)
        except ValueError as err:
            text=err.args[0]
        except HTTPException as err:
            text=err.args[0]
        except Forbidden:
            text='Forbidden'
        else:
            text='Kyaaaa'
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


start_clients()

