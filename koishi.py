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

from image_handler import on_command_upload,on_command_image
from help_handler import on_command_help
from pers_data import TOKEN,PREFIX
from infos import infos


Koishi=Client(TOKEN)

@Koishi.events
async def ready(client):
    print(f'{client.name} ({client.id}) logged in')


with Koishi.events(bot_message_event(PREFIX)) as on_message:

    on_message.extend(infos)
    
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
        search_result=re.match(r'([0-9]*) [.]*',content)
        if search_result:
            times=int(search_result[1])
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
                luck_text='.'
            text='Rolled {result} {luck_text}'
            
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
                await client.message_create(message.channel,user.mention(guild))
        
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
            
start_clients()

