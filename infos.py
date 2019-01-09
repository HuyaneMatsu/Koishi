# -*- coding: utf-8 -*-
from discord_uwu.parsers import eventlist
from discord_uwu.channel import get_message
from discord_uwu.prettyprint import chunkify
import asyncio

infos=eventlist()

@infos.add('roles')
async def list_roles(client,message,content):
    guild=message.guild
    if guild is None:
        return

    result=[]
    if message.mentions:
        user=message.mentions[0]
        guild_mode=False
        try:
            roles=user.guild_profiles[guild].roles
        except KeyError:
            roles=[]
        result.append(f'{user.display_name(guild)}\'s roles:\n')
    else:
        guild_mode=True
        roles=guild.roles
    if roles:
        ln=len(roles)
        for index in range(1,ln+1-guild_mode):
            role=roles[ln-index]
            result.append(f'Role {index} : `{role.name}`')
            if role.separated or role.mentionable:
                extra=[]
                if role.separated:
                    extra.append('separated')
                if role.mentionable:
                    extra.append('mentionable')
                result.append(f'({", ".join(extra)})\n')
            else:
                result.append('\n')
    else:
        result.append('*(none)*')
    await client.message_create(message.channel,''.join(result))

@infos.add('emojis')
async def list_emojis(client,message,content):
    guild=message.guild
    if guild is None:
        return
    result=[str(emoji) for emoji in guild.emojis.values()]
    if len(result)>50:
        await client.message_create(message.channel,' '.join(result[:50]))
        await client.message_create(message.channel,' '.join(result[50:]))
    else:
        await client.message_create(message.channel,' '.join(result))

@infos
async def message_details(client,message,content):
    if not content:
        index=1
    elif content.isdecimal():
        index=int(content)
    else:
        await client.message_create(message.channel,'Invalid index')
        return
    if index>500:
        await client.message_create(message.channel,'NO U will read that!')
        return
    try:
        target_message = await get_message(client,message.channel,index)
    except IndexError:
        await client.message_create(message.channel,'I am not able to reach that message!')
        return
    
    for chunk in chunkify(target_message):
        await client.message_create(message.channel,chunk)
        await asyncio.sleep(0.3)
    
    
