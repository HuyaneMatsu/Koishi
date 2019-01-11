# -*- coding: utf-8 -*-
import sys
from random import randint as random
import os
import re

#moving to the outer folder, so uwu ll count as a package
sys.path.append(os.path.abspath('..'))

from discord_uwu import Client,start_clients
from discord_uwu.parsers import bot_message_event
from discord_uwu.exceptions import Forbidden
from discord_uwu.emoji import BUILTIN_EMOJIS
from discord_uwu.activity import activity_game
from image_handler import on_command_upload,on_command_image
from help_handler import on_command_help
from pers_data import TOKEN,PREFIX
from infos import infos
from voice import voice
from discord_uwu.others import is_channel_mention,is_user_mention
from discord_uwu.channel import Channel_voice

Koishi=Client(TOKEN)
Koishi.activity=activity_game.create(name='with Satori')

@Koishi.events
async def ready(client):
    print(f'{client.name} ({client.id}) logged in')
        
with Koishi.events(bot_message_event(PREFIX)) as on_message:

    on_message.extend(infos)
    on_message.extend(voice)
    
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
        await client.message_create(message.channel,f'Invalid command `{command}`, try using: `{PREFIX}help`')


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


    on_message(on_command_image,'image')
    on_message(on_command_upload,'upload')
    on_message(on_command_help,'help')

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


    def deside_on_edit(guild,message,content):
        if not content:
            return 'huh?'
        
        content=re.split('[ \t]+',content)
        limit=len(content)
        if (limit&1)^1:
            return 'Pls send 1 mention, then key, value pairs.'
        if limit==1:
            return 'And anything to change?'
        if message.mentions:
            if len(message.mentions)>1:
                return 'Pls send 1 mention or 1 name and stuffs to change.'
            if not is_user_mention(content[0]):
                return '1st value must be mention,'
            user=message.mentions[0]
        else:
            user=guild.get_user(content[0])
            if not user:
                return 'Could not find a user with that name.'

        if message.channel_mentions:
            if message.channel_mentions>1 or 'voice_channel' not in content[::2]:
                return 'Not in place channel mention found'

        result={}
        
        index=1
        while index!=limit:
            key=content[index]
            index+=1
            value=content[index]
            index+=1

            if key in result:
                return f'Dupe key: "{key}"'

            if key=='nick':
                result[key]=value
                continue
                
            if key in ('deaf','mute'):
                value=value.lower()
                if value=='true':
                    result[key]=True
                    continue
                elif value=='false':
                    result[key]=False
                    continue
                else:
                    return f'Invalid value for {key}, it can be either True or False'
                
            if key=='voice_channel':
                if is_channel_mention(value):
                    channel=message.channel_mentions[0]
                else:
                    channel=guild.get_channel(value)
                    if not channel:
                        return 'Did not find that channel name'
                if type(channel) is not Channel_voice:
                    return 'Bad channel type, it must to be voice channel!'
                result[key]=channel
                continue

            if key=='role':
                role=guild.get_role(value)
                if not role:
                    return 'Didnt fin that role name!'
                
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
            
        return user,result
        
        
    @on_message.add('edit')
    async def command_edit(client,message,content):
        guild=message.guild
        if guild is None:
            return

        result=deside_on_edit(guild,message,content)
        if type(result) is tuple:
            try:
                await client.guild_user_edit(guild,result[0],**result[1])
            except Forbidden:
                result='Access denied'
            else:
                result='OwO'
        await client.message_create(message.channel,result)

start_clients()

