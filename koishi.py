# -*- coding: utf-8 -*-
import sys
from random import randint as random
import os
import re
import asyncio

#moving to the outer folder, so uwu ll count as a package
sys.path.append(os.path.abspath('..'))

from discord_uwu import Client,start_clients
from discord_uwu.parsers import bot_message_event,bot_reaction_waitfor,waitfor_reaction_wrapper
from discord_uwu.exceptions import Forbidden
from discord_uwu.emoji import BUILTIN_EMOJIS
from discord_uwu.activity import activity_game
from discord_uwu.others import is_channel_mention,is_user_mention,filter_content
from discord_uwu.channel import Channel_voice
from discord_uwu.color import Color
from discord_uwu.permission import Permission

from image_handler import on_command_upload,on_command_image
from help_handler import on_command_help,HELP
from pers_data import TOKEN,PREFIX
from infos import infos
from voice import voice

class reaction_book:
    LEFT2   = BUILTIN_EMOJIS['rewind']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['fast_forward']
    CROSS   = BUILTIN_EMOJIS['x']
    emojis  = [LEFT2,LEFT,RIGHT,RIGHT2,CROSS]
    
    __slots__=['cancel','page', 'pages']
    def __init__(self,pages):
        self.pages=pages
        self.page=0
        self.cancel=type(self)._default_cancel
        
    async def start(self,wrapper):
        client=wrapper.client
        message=wrapper.message
        for emoji in self.emojis:
            await client.reaction_add(message,emoji)

    async def __call__(self,wrapper,emoji,user):
        client=wrapper.client
        message=wrapper.message
        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
            if emoji is self.RIGHT:
                page=self.page+1
                break
            if emoji is self.CROSS:
                try:
                    await client.message_delete(message)
                except Forbidden:
                    pass
                wrapper.cancel(Exception)
                return
            if emoji is self.LEFT2:
                page=self.page-5
                break
            if emoji is self.RIGHT2:
                page=self.page+5
                break
            return
        if page<0:
            page=0
        if page>=len(self.pages):
            page=len(self.pages)-1
        try:
            await client.message_edit(message,**self.pages[page])
        except Forbidden:
            pass
        try:
            await client.reaction_delete(message,emoji,user)
        except Forbidden:
            pass
        self.page=page
        
        if wrapper.timeout<360.:
            wrapper.timeout+=30.
        
    async def _default_cancel(self,wrapper,exception=None):
        if exception==Exception:
            #we delete the message, so no need to remove reactions
            return
        if exception is TimeoutError:
            client=wrapper.client
            message=wrapper.message
            for emoji in self.emojis:
                try:
                    await client.reaction_delete_own(message,emoji)
                except Forbidden:
                    pass
            return
        #we do nothing

class wait_and_continue:
    __slots__=['cancel', 'case', 'future']
    def __init__(self,future,case,cancel=None):
        self.cancel=type(self)._default_cancel
        self.future=future
        self.case=case
    async def start(self,wrapper):
        pass

    async def __call__(self,wrapper,emoji,user):
        if self.case(emoji,user):
            self.future.set_result((emoji,user),)
            wrapper.cancel(Exception)
    async def _default_cancel(self,wrapper,exception=None):
        try:
            await wrapper.client.message_delete(wrapper.message)
        except Forbidden:
            pass
        if exception==Exception:
            return
        self.future.set_exception(exception)
        #we do nothing

        
Koishi=Client(TOKEN)
Koishi.activity=activity_game.create(name='with Satori')

@Koishi.events
async def ready(client):
    print(f'{client.name} ({client.id}) logged in')

Koishi.events(bot_reaction_waitfor())

with Koishi.events(bot_message_event(PREFIX)) as on_message:

    on_message.extend(infos)
    on_message(voice)
    on_message(on_command_image,'image')
    on_message(on_command_upload,'upload')
    on_message(on_command_help,'help')

    @on_message
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


    @on_message
    async def invalid_command(client,message,command,content):
        message = await client.message_create(message.channel,f'Invalid command `{command}`, try using: `{PREFIX}help`')
        await asyncio.sleep(30.)
        await client.message_delete(message,reason='Invalid command messages expire after 30s')

    @on_message
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


    @on_message
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


    @on_message.add('print')
    async def on_print_command(client,message,content):
        try:
            await client.message_delete(message,reason='Used print command')
        except Forbidden:
            pass
        else:
            await client.message_create(message.channel,content)

    @on_message
    async def mention_event(client,message):
        m1=message.author.mention_at(message.guild)
        m2=client.mention_at(message.guild)
        replace={re.escape(m1):m2,re.escape(m2):m1}
        pattern=re.compile("|".join(replace.keys()))
        result=pattern.sub(lambda x: replace[re.escape(x.group(0))],message.content)
        await client.message_create(message.channel,result)

    @on_message
    async def ping(client,message,content):
        guild=message.channel.guild
        if guild:
            user=guild.get_user(content)
            if user:
                await client.message_create(message.channel,user.mention_at(guild))
    
    @on_message.add('emoji')
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


    @on_message
    async def message_me(client,message,content):
        channel = await client.channel_private_create(self,message.author)
        await client.message_create(channel,'Love you!')
            
    @on_message
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
                reason=f'Executed by {message.author:f}).'
                if key=='user':
                    await client.guild_user_edit(guild,text[0],**text[1],reason=reason)
                elif key=='role':
                    await client.role_edit(text[0],**text[1],reason=reason)
            except Forbidden:
                text='Access denied'
            else:
                text='OwO'
        if not text:
            text=HELP['edit']
        await client.message_create(message.channel,text)

    @on_message
    async def move(guild,message,content):
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
                reason=f'Executed by {message.author:f}).'
                if key=='channel':
                    await client.channel_guild_move(*text,reason=reason)
                elif key=='role':
                    await client.role_move(*text,reason=reason)
                elif key=='user':
                    await client.user_move(*text,reason=reason)
            except Forbidden:
                result='Access denied!'
            else:
                result='yayyyy'
        if not text:
            text=HELP['move']
        await client.message_create(message.channel,text)

    @on_message
    async def delete(guild,message,content):
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
                channel=guild.get_channeL(content[0])
                if not channel:
                    text='Channel not found'
                    break
                text=channel
                break
            break
        if type(text) is not str:
            try:
                reason=f'Executed by {message.author:f}).'
                if key=='role':
                    await client.role_delete(text,reason)
                elif key=='channel':
                    await client.channel_delete(text,reason)                    
            except Forbidden:
                text='Access denied!'
            else:
                text='yayyyy'
        if not text:
            text=HELP['delete']
        await client.message_create(message.channel,text)

    @on_message.add('book')
    async def on_command_book(client,message,content):
        pages=({'content':'import base64\n\npage1/3'},{'content':'uwu\n\npage2/3'},{'content':'text2\n\npage3/3'})
        message = await client.message_create(message.channel,**pages[0])
        waitfor_reaction_wrapper(client,message,reaction_book(pages),120.)

    @on_message
    async def satania(client,message,content):
        message = await client.message_create(message.channel,'waiting for satania emote')
        future=asyncio.Future()
        waitfor_reaction_wrapper(client,message,wait_and_continue(future,lambda emoji,user:('satania' in emoji.name)),60.)
        try:
            emoji,user = await future
        except TimeoutError:
            return
        await client.message_create(message.channel,str(emoji)*5)
        
start_clients()

