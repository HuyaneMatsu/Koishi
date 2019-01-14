# -*- coding: utf-8 -*-
import sys
from random import randint as random
import os
import re
import asyncio

#moving to the outer folder, so uwu ll count as a package
sys.path.append(os.path.abspath('..'))

from discord_uwu import Client,start_clients
from discord_uwu.parsers import bot_message_event
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


Koishi=Client(TOKEN)
Koishi.activity=activity_game.create(name='with Satori')

@Koishi.events
async def ready(client):
    print(f'{client.name} ({client.id}) logged in')
        
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
                await client.message_reaction_add(message,emoji)
                    
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
    async def edit(client,message,content):
        guild=message.guild
        if guild is None:
            return
        text=''
        content=filter_content(content)
        key=''
        while True:
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
        if type(text) is tuple:
            try:
                if key=='user':
                    await client.guild_user_edit(guild,text[0],**text[1])
                elif key=='role':
                    await client.role_edit(text[0],**text[1])
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
            if key=='channel':
                if not content:
                    break
                key=content.pop(0)
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
            break
        if type(text) is not str:
            try:
                if key=='channel':
                    await client.channel_guild_move(*text)
                elif key=='role':
                    await client.role_move(*result)
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
        if type(text) is not str:
            try:
                if key=='role':
                    await role_delete(text)
            except Forbidden:
                result='Access denied!'
            else:
                result='yayyyy'
        if not text:
            text=HELP['delete']
        await client.message_create(message.channel,text)

    
start_clients()

