# -*- coding: utf-8 -*-
import asyncio
import math
from random import choice

from discord_uwu.parsers import eventlist
from discord_uwu.channel import get_message,Channel_text,Channel_category
from discord_uwu.prettyprint import pchunkify
from discord_uwu.others import filter_content,chunkify,cchunkify,is_channel_mention,is_user_mention,time_left,statuses
from discord_uwu.exceptions import Forbidden,HTTPException
from discord_uwu.events import pagination
from discord_uwu.embed import Embed,Embed_thumbnail,Embed_field
from discord_uwu.emoji import BUILTIN_EMOJIS
from discord_uwu.color import Color
from discord_uwu.user import USERS

from help_handler import HELP

infos=eventlist()

@infos.add('list')
async def parse_list_command(client,message,content):
    guild=message.guild
    if guild is None or not guild.permissions_for(message.author).can_administrator:
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
        if key=='webhooks':
            channel=None
            if content:
                if message.channel_mentions and is_channel_mention(content[0]):
                    channel=message.channel_mentions[0]
                else:
                    channel=guild.get_channel(channel)
            if channel is None:
                webhooks = await client.webhook_get_guild(guild)
            else:
                webhooks = await client.webhook_get_channel(channel)

            text=pchunkify(webhooks,write_parents=False)
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
    if guild is None or not guild.permissions_for(message.author).can_administrator:
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
                elif content[0].isdigit():
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
                    if index>=message.channel.MC_GC_LIMIT and message.author is not client.owner:
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
                elif content[0].isdigit():
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
            elif content[0].isdigit():
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
                if channel is None:
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
            if name.isdigit():
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
                    if is_user_mention(name) and message.user_mentions:
                        user=message.user_mentions[0]
                    else:
                        user=guild.get_user(name)
                        if user is None:
                            text='User not found'
                            break
                    continue
                
                if type_=='channel':
                    if channel is not None:
                        text='Channel mentioned more times'
                        break
                    if is_channel_mention(name) and message.channel.user_mentions:
                        channel=message.channel_mentions[0]
                    else:
                        channel=guild.get_channel(name)
                        if channel is not None:
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

    target=None
    if content:
        if guild is not None:
            if is_user_mention(content) and message.user_mentions:
                target=message.user_mentions[0]
            else:
                user=guild.get_user(content)
                if user is not None:
                    target=user
            
        if target is None:
            if content.isdigit():
                user=USERS.get(int(content),None)
                if user is None:
                    try:
                        target = await client.user_get_by_id(int(content))
                    except HTTPException:
                        pass
                else:
                    target=user
        else:
            target=user

    if target is None:
        target=message.author
    
    text=[f'**User Information**\nCreated: {time_left(target)} ago\nProfile: {target:m}\nID: {target.id}']
    
    if guild in target.guild_profiles:
        color=target.color(guild)
        profile=target.guild_profiles[guild]
        if profile.roles:
            roles=', '.join(role.mention for role in reversed(profile.roles))
        else:
            roles='none'
        text.append('\n**In guild profile**')
        if profile.nick:
            text.append(f'Nick: {profile.nick}')
        text.append(f'Joined: {time_left(profile)} ago\nRoles: {roles}')
    else:
        if target.avatar:
            color=target.avatar&0xFFFFFF
        else:
            color=target.default_avatar.color
        
    embed=Embed(f'{target:f}','\n'.join(text),color)
    embed.thumbnail=Embed_thumbnail(url=target.avatar_url_as(size=128))

    await client.message_create(message.channel,embed=embed)

@infos.add('guild')
async def guild_info(client,message,content):
    guild=message.guild
    if guild is None:
        return

    #most usual first
    s_grey  = statuses.offline
    s_green = statuses.online
    s_yellow= statuses.idle
    s_red   = statuses.dnd
    
    v_grey  = 0
    v_green = 0
    v_yellow= 0
    v_red   = 0

    for user in guild.users.values():
        status=user.status
        if   status is s_grey:
            v_grey+=1
        elif status is s_green:
            v_green+=1
        elif status is s_yellow:
            v_yellow+=1
        elif status is s_red:
            v_red+=1
        else: #if we change our satus to invisible, it will be invisible till we get the dispatch event, then it turns offline.
            v_grey+=1
        
    del s_grey
    del s_green
    del s_yellow
    del s_red

    channel_text    = 0
    channel_category= 0
    channel_voice   = 0

    for channel in guild.all_channel.values():
        if type(channel) is Channel_text:
            channel_text+=1
        elif type(channel) is Channel_category:
            channel_category+=1
        else:
            channel_voice+=1

    if guild.features:
        features=', '.join(feature.value for feature in guild.features)
    else:
        features='none'

    if guild.icon:
        color=guild.icon&0xFFFFFF
    else:
        color=0
        
    embed=Embed('',f'''
        **Guild information**
        Created: {time_left(guild)} ago
        Voice region: {guild.region}
        Features: {features}

        **Counts**
        Users: {guild.user_count}
        Roles: {len(guild.roles)}
        Text channels: {channel_text}
        Voice channels: {channel_voice}
        Category channels: {channel_category}

        **Users**
        {BUILTIN_EMOJIS["green_heart"]} {v_green}
        {BUILTIN_EMOJIS["yellow_heart"]} {v_yellow}
        {BUILTIN_EMOJIS["heart"]} {v_red}
        {BUILTIN_EMOJIS["black_heart"]} {v_grey}
        ''',color)
    
    embed.thumbnail=Embed_thumbnail(guild.icon_url_as(size=128))

    await client.message_create(message.channel,embed=embed)

@infos
async def invites(client,message,content):
    guild=message.guild
    if guild is None or not guild.permissions_for(message.author).can_administrator:
        return

    channel=None
    if content:
        if is_channel_mention(content) and message.channel_mentions[0]:
            channel=message.channel_mentions[0]
        else:
            channel=guild.get_channel(content)
            
    try:
        if channel is not None:
            invites = await client.invites_of_channel(channel)
        else:
            invites = await client.invites_of_guild(guild)
    except Forbidden:
        return
    
    pages=[{'content':chunk} for chunk in pchunkify(invites,write_parents=False,show_code=False)]
    pagination(client,message.channel,pages,120.)

def generate_love_level():
    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["blue_heart"]} There\'s no real connection between you two {BUILTIN_EMOJIS["blue_heart"]}',
                ),
        'text': ( \
            'The chance of this relationship working out is really low. You '
            'can get it to work, but with high costs and no guarantee of '
            'working out. Do not sit back, spend as much time together as '
            'possible, talk a lot with each other to increase the chances of '
            'this relationship\'s survival.'
                ),
            }

    for x in range(0,2):
        yield value

    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["blue_heart"]} A small acquaintance {BUILTIN_EMOJIS["blue_heart"]}',
                ),
        'text':( \
            'There might be a chance of this relationship working out somewhat '
            'well, but it is not very high. With a lot of time and effort '
            'you\'ll get it to work eventually, however don\'t count on it. It '
            'might fall apart quicker than you\'d expect.'
                ),
            }
    
    for x in range(2,6):
        yield value

    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["purple_heart"]} You two seem like casual friends {BUILTIN_EMOJIS["purple_heart"]}',
                ),
        'text':( \
            'The chance of this relationship working is not very high. You both '
            'need to put time and effort into this relationship, if you want it '
            'to work out well for both of you. Talk with each other about '
            'everything and don\'t lock yourself up. Spend time together. This '
            'will improve the chances of this relationship\'s survival by a lot.'
                ),
            }

    for x in range(6,21):
        yield value

    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["heartpulse"]} You seem like you are good friends {BUILTIN_EMOJIS["heartpulse"]}',
                ),
        'text':( \
            'The chance of this relationship working is not very high, but its '
            'not that low either. If you both want this relationship to work, '
            'and put time and effort into it, meaning spending time together, '
            'talking to each other etc., than nothing shall stand in your way.'
                ),
            }

    for x in range(21,31):
        yield value


    value={ \
        'titles':(
            f'{BUILTIN_EMOJIS["cupid"]} You two are really close aren\'t you? {BUILTIN_EMOJIS["cupid"]}',
                ),
        'text':( \
            'Your relationship has a reasonable amount of working out. But do '
            'not overestimate yourself there. Your relationship will suffer '
            'good and bad times. Make sure to not let the bad times destroy '
            'your relationship, so do not hesitate to talk to each other, '
            'figure problems out together etc.'
                ),
            }

    for x in range(31,46):
        yield value
    
    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["heart"]} So when will you two go on a date? {BUILTIN_EMOJIS["heart"]}',
                ),
        'text':( \
            'Your relationship will most likely work out. It won\'t be perfect '
            'and you two need to spend a lot of time together, but if you keep '
            'on having contact, the good times in your relationship will '
            'outweigh the bad ones.'
                ),
            }

    for x in range(46,61):
        yield value

    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["two_hearts"]} Aww look you two fit so well together {BUILTIN_EMOJIS["two_hearts"]}',
                ),
        'text':( \
            'Your relationship will most likely work out well. Don\'t hesitate '
            'on making contact with each other though, as your relationship '
            'might suffer from a lack of time spent together. Talking with '
            'each other and spending time together is key.'
                ),
            }

    for x in range(61,86):
        yield value

    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["sparkling_heart"]} Love is in the air {BUILTIN_EMOJIS["sparkling_heart"]}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]} Planned your future yet? {BUILTIN_EMOJIS["sparkling_heart"]}',
                ),
        'text':( \
            'Your relationship will most likely work out perfect. This '
            'doesn\'t mean thought that you don\'t need to put effort into it. '
            'Talk to each other, spend time together, and you two won\'t have '
            'a hard time.'
                ),
            }

    for x in range(86,96):
        yield value

    value={ \
        'titles':( \
            f'{BUILTIN_EMOJIS["sparkling_heart"]} When will you two marry? {BUILTIN_EMOJIS["sparkling_heart"]}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]} Now kiss already {BUILTIN_EMOJIS["sparkling_heart"]}',
                ),
        'text':( \
            'You two will most likely have the perfect relationship. But don\'t '
            'think that this means you don\'t have to do anything for it to '
            'work. Talking to each other and spending time together is key, '
            'even in a seemingly perfect relationship.'
                ),
            }

    for x in range(96,101):
        yield value

LOVE_VALUES=tuple(generate_love_level())
del generate_love_level

@infos
async def love(client,message,content):
    guild=message.guild
    if guild is None or not content:
        return
    
    name=filter_content(content)[0]
    if message.user_mentions is not None and is_user_mention(name):
        target=message.user_mentions[0]
    else:
        target=guild.get_user(name)
        if target is None:
            if name.isdigit():
                target=USERS.get(int(name),None)
                if target is None:
                    try:
                        target = await client.user_get_by_id(int(name))
                    except HTTPException:
                        return
            else:
                return

    source=message.author

    if target is source:
        return
    
    percent=((source.id&0x1111111111111111111111)+(target.id&0x1111111111111111111111))%101
            
    embed=Embed( \
        choice(LOVE_VALUES[percent]['titles']),
        f'{source:f} {BUILTIN_EMOJIS["heart"]} {target:f} scored {percent}%!',
        Color.d_magenta,
            )
    embed.fields.append(Embed_field('My advice:',LOVE_VALUES[percent]['text']))

    await client.message_create(message.channel,embed=embed)
