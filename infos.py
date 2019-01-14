# -*- coding: utf-8 -*-
from discord_uwu.parsers import eventlist
from discord_uwu.channel import get_message
from discord_uwu.prettyprint import chunkify
from discord_uwu.others import filter_content
import asyncio

infos=eventlist()

@infos.add('list')
async def parse_list_command(client,message,content):
    guild=message.guild
    if guild is None:
        return
    err_msg='Lists a specific type of objects, it can be "emojis", "roles", "channels".'
    content=filter_content(content)
    if len(content)==0:
        await client.message_create(message.channel,err_msg)
        return
    key=content.pop(0)
    if key=='emojis':
        list_=[str(emoji) for emoji in guild.emojis.values()]
        iterator=iter(list_)
        lines=[''.join(v for v,c in zip(iterator,range(10))) for i in range((len(list_)+9)//10)]
        result=[]
        ln_count=0
        shard=[]
        for line in lines:
            ln=len(line)+1
            if ln_count+ln>2000:
                ln_count=ln
                result.append('\n'.join(shard))
                shard.clear()
            shard.append(line)
        result.append('\n'.join(shard))
        del shard
    elif key=='channels':
        result=chunkify(guild.channels,write_parents=False)
    elif key=='roles':
        result=chunkify(guild.roles,write_parents=False)
    else:
        await client.message_create(message.channel,err_msg)
        return
    for chunk in result:
        await client.message_create(message.channel,chunk)
        await asyncio.sleep(0.3)

@infos.add('details')
async def parse_details_command(client,message,content):
    guild=message.guild
    if guild is None:
        return
    err_msg=text='Shows details about a specific object, it can be "message" +index, "guild".'
    content=filter_content(content)
    if len(content)==0:
        await client.message_create(message.channel,err_msg)
        return
    key=content.pop(0)
    if key=='message':
        text=None
        #alternative function definition right here
        while True:
            if not content:
                index=1
            elif content[0].isdecimal():
                index=int(content[0])
            else:
                text='Invalid index'
                break
            if index>500:
                text='NO U will read that!'
                break
            try:
                target_message = await get_message(client,message.channel,index)
            except IndexError:
                text='I am not able to reach that message!'
                break
            result=chunkify(target_message)
            break
        if text:
            await client.message_create(message.channel,text)
            return
    elif key=='guild':
        result=chunkify(guild)
    else:
        await client.message_create(message.channel,err_msg)
        return
    
    for chunk in result:
        await client.message_create(message.channel,chunk)
        await asyncio.sleep(0.3)
