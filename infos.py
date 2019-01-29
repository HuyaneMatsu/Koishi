# -*- coding: utf-8 -*-
import asyncio
import math
from discord_uwu.parsers import eventlist
from discord_uwu.channel import get_message
from discord_uwu.prettyprint import pchunkify
from discord_uwu.others import filter_content,chunkify,cchunkify,is_channel_mention,is_user_mention,time_left
from discord_uwu.exceptions import Forbidden,HTTPException
from discord_uwu.events import pagination
from help_handler import HELP
from discord_uwu.embed import Embed,Embed_thumbnail
from datetime import datetime

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
            lines=[f'{f"{index}.:": >{ln_c_l}} {message:c} id={message.id} length={len(message.content)} author={message.author:f}' for index,message in enumerate(messages,1)]
            text=cchunkify(lines)
            break
        break
    if type(text) is not str:
        pages=[{'content':chunk} for chunk in text]
        pagination(client,message.channel,pages,120.)
    elif text:
        await client.message_create(message.channel,text)
    else:
        await client.message_create(message.channel,embed=HELP['list'])

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
                        target_message = await client.message_get(message.channel,index)
                    except (Forbidden,HTTPException):
                        text='Acces denied or not existing message'
                        break
                else:
                    if index>message.channel.MC_GC_LIMIT:
                        if message.author is not client.owner:
                            text='NO U will read that!'
                            break
                    try:
                        target_message = await get_message(client,message.channel,index)
                    except IndexError:
                        text='I am not able to reach that message!'
                        break
                    except PermissionError:
                        text='Permission denied!'
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

        if key=='role':
            if not content:
                role=guild.roles[0]
            elif content[0].isdecimal():
                index=int(content[0])
                if index>=len(guild.roles):
                    index=len(guild.roles)-1
                role=guild.roles[index]
            else:
                role=guild.get_role(content[0])
                if role is None:
                    text='Couldnt find that role by index/name.'
                    break

            text=pchunkify(role)
            break
        if key=='channel':
            if not content:
                text='Channel name or mention too pls?'
                break
            name=content.pop(0)
            if is_channel_mention(name) and message.channel_mentions:
                channel=message.channel_mentions[0]
            else:
                channel=guild.get_channel(name)
                if not channel:
                    text='Unknown channel name.'
                    
            if len(content)<2:
                text=pchunkify(channel,overwrites=True)
                break
            
            name=content.pop(0)
            if name not in ('ow','overwrite'):
                text='After channel the next posible key is "ow"/"overwrite with an index!'
                break
            if not channel.overwrites:
                text='The channel has no overwrites desu'
                break
            name=content.pop(0)
            if name.isdecimal():
                try:
                    overwrite=channel.overwrites[int(name)]
                except IndexError:
                    text=f'The channel has only {len(channel.overwrites)} overwirtes'
                    break
            else:
                value=guild.get_role(name)
                if value is None:
                    value=guild.get_user(name)
                if value is None:
                    text='There is no user/role like that'
                    break
                overwrite=None
                for x in channel.overwrites:
                    if x.target is value:
                        overwrite=x
                        break
                del x
                if overwrite is None:
                    text='No overwrite found for that user/role'
                    break
            
            text=pchunkify(overwrite,detailed=True)
            break
        
        if key=='permission':
            if len(content)&1 or len(content)>4:
                text='Getting info about sometihing should contain user <user> channel <channel> pairs'
                break
            
            user=None
            channel=None
            
            while True:
                if not content:
                    break
                type_=content.pop(0)
                name=content.pop(0)
                if type_=='user':
                    if user is not None:
                        text='User mentioned more times'
                        break
                    if is_user_mention(name) and message.mentions:
                        user=message.mentions[0]
                    else:
                        user=guild.get_user(name)
                        if not user:
                            text='User not found'
                            break
                    continue
                
                if type_=='channel':
                    if channel is not None:
                        text='Channel mentioned more times'
                        break
                    if is_channel_mention(name) and message.channel.mentions:
                        channel=message.channel_mentions[0]
                    else:
                        channel=guild.get_channel(name)
                        if not channel:
                            text='Channel not found'
                            break
                    continue

                text=f'Invalid key "{type_}"'
                break

            if text:
                break
            
            if user is None:
                user=message.author
            if channel is None:
                channel=message.channel
                
            text=pchunkify(channel.permissions_for(user))
            break
        
        break
    
    if type(text) is not str:
        pages=[{'content':chunk} for chunk in text]
        pagination(client,message.channel,pages,120.)
    elif text:
        await client.message_create(message.channel,text)
    else:
        await client.message_create(message.channel,embed=HELP['details'])
    

@infos.add('user')
async def user_info(client,message,content):
    guild=message.guild

    target=message.author
    if guild and content:
        if is_user_mention(content) and message.mentions:
            target=message.mentions[0]
        else:
            user=guild.get_user(content)
            if user:
                target=user
    
    text=[f'**User Information**\nCreated: {time_left(target)} ago\nProfile: {target:m}\nID: {target.id}']
    
    if guild:
        profile=target.guild_profiles[guild]
        if profile.roles:
            roles=', '.join(role.mention for role in reversed(profile.roles))
        else:
            roles='none'
        text.append('\n**In guild profile**')
        if profile.nick:
            text.append(f'Nick: {profile.nick}')
        text.append(f'Joined: {time_left(profile)} ago\nRoles: {roles}')
        
    embed=Embed( \
        title       = f'{target:f}',
        description = '\n'.join(text),
        color       = target.color(guild),
            )
    embed.thumbnail=Embed_thumbnail( \
        url         = target.avatar_url_as(size=128),
        height      = 128,
        width       = 128,
            )

    await client.message_create(message.channel,embed=embed)


@infos
async def invites(client,message,content):
    guild=message.guild
    if not guild or not guild.permissions_for(message.author).can_administrator:
        return

    channel=None
    if content:
        if is_channel_mention(content) and message.channel_mentions[0]:
            channel=message.channel_mentions[0]
        else:
            channel=guild.get_channel(content)
            
    try:
        if channel:
            invites = await client.invites_of_channel(channel)
        else:
            invites = await client.invites_of_guild(guild)
    except Forbidden:
        return
    
    pages=[{'content':chunk} for chunk in pchunkify(invites,write_parents=False,show_code=False)]
    pagination(client,message.channel,pages,120.)
