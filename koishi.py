# -*- coding: utf-8 -*-
import sys
from random import randint as random
import os
import re
import asyncio
import time
#moving to the outer folder, so uwu ll count as a package
sys.path.append(os.path.abspath('..'))

from discord_uwu import Client,start_clients
from discord_uwu.exceptions import Forbidden,HTTPException
from discord_uwu.emoji import BUILTIN_EMOJIS,parse_emoji
from discord_uwu.activity import activity_game
from discord_uwu.others import is_channel_mention,is_user_mention,filter_content,chunkify
from discord_uwu.channel import Channel_voice,get_message_iterator
from discord_uwu.color import Color
from discord_uwu.permission import Permission
from discord_uwu.embed import Embed,Embed_image
from discord_uwu.events import waitfor_wrapper,pagination,wait_and_continue,bot_reaction_waitfor,bot_message_event,wait_for_message,wait_for_emoji
from discord_uwu.futures import wait_one
from discord_uwu.client_core import GC_client
from discord_uwu.prettyprint import pchunkify

from image_handler import on_command_upload,on_command_image
from help_handler import on_command_help,HELP
from pers_data import TOKEN,PREFIX,TOKEN2
from infos import infos
from voice import voice
#from battleships import battle_manager
    
class schannel:
    __slots__=['channel']
    def __init__(self):
        self.channel=None
        
    async def set_channel(self,client,message,content):
        if message.author==client.owner:
            self.channel=message.channel
            await client.message_create(message.channel,'Now i ll send special messages to this channel')
    
    async def emoji_update(self,client,guild,modifications):
        if self.channel:
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
        if self.channel:
            await client.message_create(self.channel,f'Unknown guild at {parser}: {guild_id}\n data: {data}')

    async def unknown_channel(self,client,parser,channel_id,data):
        if self.channel:
            await client.message_create(self.channel,f'Unknown channel at {parser}: {channel_id}\n data: {data}')

    async def unknown_role(self,client,parser,guild,role_id,data):
        if self.channel:
            await client.message_create(self.channel,f'Unknown guild: {guild} at {parser}; role: {role_id}\n data: {data}')

    async def unknown_voice_client(self,client,parser,voice_client_id,data):
        if self.channel:
            await client.message_create(self.channel,f'Unknown voice client at {parser}: {voice_client_id}\n data: {data}')

schannel=schannel()

        
Koishi=Client(TOKEN,loop=1)
Koishi.activity=activity_game.create(name='with Satori')

Mokou=Client(TOKEN2,loop=2)

GC=GC_client(loop=2) #let it run with Mokou, she does nothing anyways
    
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
    info = await client.client_application_info()
    client.owner=info['owner']
    print(f'{client:f} ({client.id}) logged in\nowner: {client.owner:f} ({client.owner.id})')
    
Koishi.events(bot_reaction_waitfor())

Koishi.events(schannel.emoji_update)
Koishi.events(schannel.unknown_guild)
Koishi.events(schannel.unknown_channel)
Koishi.events(schannel.unknown_role)
Koishi.events(schannel.unknown_voice_client)


with Koishi.events(bot_message_event(PREFIX)) as on_command:

    on_command(schannel.set_channel,'here')
    on_command.extend(infos)
    on_command(voice)
    on_command(on_command_image,'image')
    on_command(on_command_upload,'upload')
    on_command(on_command_help,'help')

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
    async def invalid_command(client,message,command,content):
        message = await client.message_create(message.channel,f'Invalid command `{command}`, try using: `{PREFIX}help`')
        await asyncio.sleep(30.)
        await client.message_delete(message,reason='Invalid command messages expire after 30s')

    @on_command
    async def rate(client,message,content):
        if message.mentions:
            target=message.mentions[0]
        else:
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


    @on_command.add('print')
    async def on_print_command(client,message,content):
        try:
            await client.message_delete(message,reason='Used print command')
        except Forbidden:
            pass
        else:
            await client.message_create(message.channel,content)

    @on_command
    async def mention_event(client,message):
        m1=message.author.mention_at(message.guild)
        m2=client.mention_at(message.guild)
        replace={re.escape(m1):m2,re.escape(m2):m1}
        pattern=re.compile("|".join(replace.keys()))
        result=pattern.sub(lambda x: replace[re.escape(x.group(0))],message.content)
        await client.message_create(message.channel,result)

    @on_command
    async def ping(client,message,content):
        guild=message.channel.guild
        if guild:
            user=guild.get_user(content)
            if user:
                await client.message_create(message.channel,user.mention_at(guild))

    @on_command
    async def pong(client,message,content):
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

    @on_command
    async def pm(client,message,content):
        guild=message.guild
        if not guild:
            return
        content=filter_content(content)
        while True:
            if len(content)!=1:
                text='The 1st line must contain a mention/username of the "lucky" person.'
                break
            content=content[0]
            if message.mentions and is_user_mention(content):
                user=message.mentions[0]
            else:
                user=guild.get_user(content)
                if not user:
                    text='Could not find that user!'
                    break

            index=message.content.find('\n')+1
            if not index:
                text='Unable to send empty message'
                break
            text=message.content[index:]
            if not text:
                text='Unable to send empty message'
                break
            channel = await client.channel_private_create(user)
            try:
                await client.message_create(channel,text)
                text='Big times! Message sent!'
            except Forbidden:
                text='Access denied'
            break
                                    
        await client.message_create(message.channel,text)
        
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
                if message.mentions:
                    if len(message.mentions)>1:
                        text='Pls send 1 mention or 1 name and stuffs to change.'
                        break
                    if not is_user_mention(content[0]):
                        text='1st value must be mention.'
                        break
                    user=message.mentions[0]
                else:
                    user=guild.get_user(content[0])
                    if not user:
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
                            if not channel:
                                text='Did not find that channel name'
                                break
                        if type(channel) is not Channel_voice:
                            text='Bad channel type, it must to be voice channel!'
                            break
                        result[name]=channel
                        continue

                    if name=='role':
                        role=guild.get_role(value)
                        if not role:
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
                if not role:
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
                if not text: 
                    text=(role,result)
                break
            break
        if type(text) is not str:
            try:
                reason=f'Executed by {message.author:f}'
                if key=='user':
                    await client.guild_user_edit(guild,text[0],**text[1],reason=reason)
                elif key=='role':
                    await client.role_edit(text[0],**text[1],reason=reason)
            except Forbidden:
                text='Access denied'
            else:
                text='OwO'
                
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['edit'])


    @on_command
    async def move(client,message,content):
        guild=message.guild
        if not guild:
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
                    if not channel:
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
                        if category.type_lookup!=4:
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
                if not role:
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
                    if message.mentions and is_user_mention(name):
                        user=message.mentions[0]
                    else:
                        user=guild.get_user(name)
                        if not user:
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
                    if not channel:
                        text='Could not find that channel!'
                        break
                if channel.type_lookup!=2:
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
            if not content:
                break
            key=content.pop(0)
            if key=='role':
                if len(content)!=1:
                    text='Role name only!'
                    break
                role=guild.get_role(content[0])
                if not role:
                    text='Role not found'
                    break
                text=role
                break
            if key=='channel':
                if len(content)!=1:
                    text='Channel name only!'
                    break
                channel=guild.get_channel(content[0])
                if not channel:
                    text='Channel not found'
                    break
                text=channel
                break
            break
        if type(text) is not str:
            try:
                reason=f'Executed by {message.author:f}'
                if key=='role':
                    await client.role_delete(text,reason)
                elif key=='channel':
                    await client.channel_delete(text,reason)                    
            except Forbidden:
                text='Access denied!'
            else:
                text='yayyyy'
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['delete'])
        

    @on_command.add('book')
    async def on_command_book(client,message,content):
        pages=({'content':'import base64\n\npage1/3'},{'content':'uwu\n\npage2/3'},{'content':'text2\n\npage3/3'})
        pagination(client,message.channel,pages)


    @on_command
    async def satania(client,message,content):
        message = await client.message_create(message.channel,'waiting for satania emote')
        try:
            emoji,user = await wait_for_emoji(client,message,lambda emoji,user:('satania' in emoji.name.lower()),60.)
        except TimeoutError:
            return
        finally:
            try:
                await client.message_delete(message)
            except Forbidden:
                pass
        await client.message_create(message.channel,str(emoji)*5)

    @on_command.add('embed')
    async def on_command_embed(client,message,content):
        content='Here\'s a hug for Nyansia ! OwO'
        embed=Embed( \
            title='Nyanmatsu hugs Nyansia',
            url='https://discordapp.com',
            color=Color.from_html('#ff4465'),
                )
        embed.image=Embed_image('https://cdn.discordapp.com/embed/avatars/0.png')
        
        await client.message_create(message.channel,content,embed)

    @on_command
    async def clear(client,message,content):
        guild=message.guild
        if not guild:
            return
        
        if not guild.permissions_for(message.author).can_administrator:
            return
            
        channel=message.channel
        author=message.author
        content=filter_content(content)
        
        if not content:
            limit=100
        elif content[0].isdecimal():
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
            if message.mentions and is_user_mention(content):
                target=message.mentions[0]
            elif guild:
                user=guild.get_user(content)
                if user:
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
        while True:
            if not guild.permissions_for(message.author).can_administrator:
                text='You do not have permissions granted to use this command'
                break
            
            key=content.pop(0)
            
            if not content:
                break
            
            if key=='role':
                limit=len(content)
                if (limit&1):
                    text='Key, value pairs.'
                    break
                if limit==1:
                    text='And anything to change?'
                    break

                result={}
                
                index=0
                while index!=limit:
                    name=content[index]
                    index+=1
                    value=content[index]
                    index+=1

                    if name in result:
                        text=f'Dupe key: "{name}"'
                        break

                    if name=='name':
                        role=guild.get_role(name)
                        if role:
                            text='A role already häs that name'
                            break
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
                if not text: 
                    text=result
                break
            break
        if type(text) is not str:
            try:
                reason=f'Executed by {message.author:f}'
                if key=='role':
                    await client.role_create(guild,**text,reason=reason)
            except Forbidden:
                text='Access denied!'
            else:
                text='yayyyy'
        if text:
            await client.message_create(message.channel,text)
        else:
            await client.message_create(message.channel,embed=HELP['create'])
        

    @on_command
    async def subscribe(client,message,content):
        guild=message.guild
        if not guild:
            return
        role=guild.get_role('Announcements')
        if not role:
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
        if not guild or not guild.permissions_for(message.author).can_create_instant_invite:
            return

        if message.author is guild.owner and content=='perma':
            max_age=0
            max_use=0
        else:
            max_age=21600
            max_use=1
        
        try:
            invite = await client.invite_create(guild.system_channel,max_age,max_use)
        except Forbidden:
            return
                                                
        channel = await client.channel_private_create(message.author)
        await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')

    @on_command
    async def invite_by_code(client,message,content):
        guild=message.guild
        if not guild or not guild.permissions_for(message.author).can_administrator:
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
        if not guild or not guild.permissions_for(message.author).can_administrator:
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
        if not guild or not guild.permissions_for(message.author).can_administrator:
            return
        
        try:
            with client.keep_typing(message.channel):
                invites = await client.invites_of_guild(guild)
                for invite in invites:
                    await asyncio.sleep(0.5,loop=client.loop)
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
##        if not guild or not guild.permissions_for(message.author).can_administrator:
##            return
##        
##        try:
##            with client.keep_typing(message.channel):
##                invites = await client.invites_of_guild(guild)
##                for invite in invites:
##                    await asyncio.sleep(0.5,loop=client.loop)
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

    #on_command(battle_manager,case='bs')

            
    @on_command
    async def wait2where(client,message,content):
        channel=message.channel
        private = await client.channel_private_create(message.author)
        await client.message_create(channel,'Waiting on any message from you here and at dm')

        
        future=wait_one(client.loop)
        case=lambda message,author=message.author:message.author is author
        event=client.events.message_create
        
        wrapper1=waitfor_wrapper(client,wait_and_continue(future,case,channel,event),60.)
        wrapper2=waitfor_wrapper(client,wait_and_continue(future,case,private,event),60.)
        
        try:
            result = await future
        except TimeoutError:
            await client.message_create(channel,'Time is over')
            return
        
        wrapper1.cancel()
        wrapper2.cancel()
        
        await client.message_create(channel,result.content)

    @on_command
    async def prune(client,message,content):
        guild=message.guild
        if not guild or not guild.permissions_for(message.author).can_administrator:
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
            
start_clients()

