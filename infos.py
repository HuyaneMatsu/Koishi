# -*- coding: utf-8 -*-
import asyncio

from discord_uwu.parsers import eventlist
from discord_uwu.channel import get_message
from discord_uwu.prettyprint import pchunkify
from discord_uwu.others import filter_content,chunkify,cchunkify
from discord_uwu.exceptions import Forbidden,HTTPException
from help_handler import HELP

infos=eventlist()

@infos.add('list')
async def parse_list_command(client,message,content):
    guild=message.guild
    if guild is None:
        return
    key=''
    text=''
    while True:
        content=filter_content(content)
        if len(content)==0:
            break
        key=content.pop(0)
        if key=='emojis':
            list_=[str(emoji) for emoji in guild.emojis.values()]
            iterator=iter(list_)
            lines=[''.join(v for v,c in zip(iterator,range(10))) for i in range((len(list_)+9)//10)]
            text=chunkify(lines)
            break
        if key=='channels':
            text=pchunkify(guild.channels,write_parents=False)
            break
        if key=='roles':
            text=pchunkify(guild.roles,write_parents=False)
            break
        if key=='pins':
            messages = await client.channel_pins(message.channel)
            if not messages:
                text='There are no pinned messages at the channel.'
                break
            ln_c_l=len(str(len(messages)-1))+2
            lines=[f'{f"{index}.:" >ln_c_l} {message:c} id={message.id} length={len(message)} author={message.author:f}' for message in messages]
            text=cchunkify(lines)
            break
        break
    if type(text) is not str:
        for chunk in text:
            await client.message_create(message.channel,chunk)
            await asyncio.sleep(0.3)
    else:
        if not text:
            text=HELP['list']
        await client.message_create(message.channel,)

@infos.add('details')
async def parse_details_command(client,message,content):
    guild=message.guild
    if guild is None:
        return
    text=''
    key=''
    while True:
        content=filter_content(content)
        if len(content)==0:
            break
        key=content.pop(0)
        if key=='message':
            #alternative function definition right here
            while True:
                if not content:
                    index=1
                elif content[0].isdecimal():
                    index=int(content[0])
                else:
                    text='Invalid index'
                    break
                if index>4194304:
                    #id propably
                    try:
                        target_message = await client.message_get(message.channel,message_id)
                    except (Forbidden,HTTPException):
                        text='Acces denied or not existing message'
                        break
                else:
                    if index>500:
                        text='NO U will read that!'
                        break
                    try:
                        target_message = await get_message(client,message.channel,index)
                    except IndexError:
                        text='I am not able to reach that message!'
                        break
                text=pchunkify(target_message)
                break
            break
        
        if key=='guild':
            text=pchunkify(guild)
            break

        if key=='pin':
            while True:
                if not content:
                    index=0
                elif content[0].isdecimal():
                    index=int(content[0])
                else:
                    text='Invalid index'
                    break
                messages = await client.channel_pins(message.channel)
                if not messages:
                    text='There are no pins at this channel'
                    break
                if len(messages)<=index:
                    text=f'Index out of range, there is only {len(messages)} pins at the channel'
                    break
                text=pchunkify(messages[index])
                break
            break
        break
    
    if type(text) is not str:
        for chunk in text:
            await client.message_create(message.channel,chunk)
            await asyncio.sleep(0.3)
    else:
        if not text:
            text=HELP['details']
        await client.message_create(message.channel,text)
    

