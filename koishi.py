import re, sys
from random import randint

from hata.parsers import eventlist
from hata.client_core import CLIENTS
from hata.permission import Permission
from hata.events_compiler import ContentParser
from hata.user import User
from hata.client import Client
from hata.prettyprint import pchunkify
from hata.futures import CancelledError,sleep,FutureWM,Task,render_exc_to_list
from hata.events import Pagination,wait_for_message,wait_for_reaction,Cooldown,prefix_by_guild
from hata.channel import cr_pg_channel_object,ChannelText
from hata import others
from hata.exceptions import DiscordException
from hata.emoji import BUILTIN_EMOJIS,parse_emoji
from hata.others import filter_content
from hata.guild import Guild,GUILDS
from hata.role import Role
from hata.embed import Embed

import image_handler
from help_handler import KOISHI_HELP_COLOR, KOISHI_HELPER, invalid_command
from ratelimit_tests import ratelimit_commands
from kanako import kanako_manager
from dungeon_sweeper import ds_manager,_DS_modify_best
from voice import voice
from dispatch_tests import dispatch_tester
from battleships import battle_manager
from infos import infos,update_about
from tools import CooldownHandler, BeautifulSoup
from gambling import gambling
import channeller
import pers_data
import models

from PIL import Image as PIL
from hata.ios import ReuBytesIO

PREFIXES=prefix_by_guild(pers_data.KOISHI_PREFIX,models.DB_ENGINE,models.PREFIX_TABLE,models.pefix_model)

del pers_data
del prefix_by_guild
del models

class once_on_ready(object):
    __slots__ = ('called',)
    __event_name__='ready'
    
    def __init__(self):
        self.called=False
        
    async def __call__(self,client):
        if self.called:
            return
        
        self.called=True
        
        print(f'{client:f} ({client.id}) logged in')
        await client.update_application_info()
        print(f'owner: {client.owner:f} ({client.owner.id})')
        update_about(client)

commands=eventlist()

commands(image_handler.on_command_upload,'upload')
commands(image_handler.on_command_image,'image')
commands(KOISHI_HELPER,'help')
commands(invalid_command)
commands.extend(ratelimit_commands)
commands(kanako_manager,'kanakogame')
commands(voice)
commands(dispatch_tester.here)
commands(dispatch_tester.switch)
commands.extend(infos)
commands(battle_manager,case='bs')
commands(ds_manager,'ds')
commands(_DS_modify_best)
commands(channeller.channeling_start)
commands(channeller.channeling_stop)
commands.extend(gambling)

_KOISHI_NOU_RP=re.compile(r'n+\s*o+\s*u+',re.I)
_KOISHI_OWO_RP=re.compile('(owo|uwu|0w0)',re.I)
_KOISHI_OMAE_RP=re.compile('omae wa mou',re.I)


@commands
async def default_event(client,message):
    if message.user_mentions is not None and client in message.user_mentions:
        m1=message.author.mention_at(message.guild)
        m2=client.mention_at(message.guild)
        replace={re.escape(m1):m2,re.escape(m2):m1}
        pattern=re.compile("|".join(replace.keys()))
        result=pattern.sub(lambda x: replace[re.escape(x.group(0))],message.content)
        await client.message_create(message.channel,result)
    else:
        content=message.content
        if message.channel.cached_permissions_for(client).can_add_reactions and _KOISHI_NOU_RP.match(content) is not None:
            parts=[]
            for value in 'nou':
                emoji=BUILTIN_EMOJIS[f'regional_indicator_{value}']
                await client.reaction_add(message,emoji)
            return
        
        if len(content)==3:
            matched=_KOISHI_OWO_RP.match(content,)
            if matched is None:
                return
            text=f'{content[0].upper()}{content[1].lower()}{content[2].upper()}'

        elif _KOISHI_OMAE_RP.match(content) is not None:
            text='NANI?'

        else:
            return
        
        if text:
            await client.message_create(message.channel,text)

@commands
@ContentParser('user, flags=mna, default="message.author"')
async def rate(client,message,target):
    if target in CLIENTS or client.is_owner(target):
        result=10
    else:
        result=target.id%11
    #nickname check
    await client.message_create(message.channel,f'I rate {target.name_at(message.guild)} {result}/10')

async def _help_rate(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('rate',(
        'Do you want me, to rate someone?\n'
        f'Usage: `{prefix}rate <user>`\n'
        'If no user is passed, I will rate you :3'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('rate',_help_rate)


@commands
@ContentParser('int, default="1"')
async def dice(client,message,times):
    if times==0:
        text='0 KEK'
    elif times>6:
        text='I have only 6 dices, sorry, no money for more. Sadpanda'
    else:
        result=0
        for x in range(times):
            result+=randint(1,6)
            
        if result<=2.5*times:
            luck_text=', better luck next time!'
        elif result>=5.5*times:
            luck_text=', so BIG,.. thats what she said... *cough*'
        else:
            luck_text=''
        text=f'Rolled {result} {luck_text}'
        
    await client.message_create(message.channel,text)

async def _help_dice(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('dice',(
        'I will throw some dice and tell you the sum.\n'
        f'Usage: `{prefix}dice <dice_count>`\n'
        '`dice_count` if optional, but I have only 6 dices...'
        ),color=KOISHI_HELP_COLOR).add_footer(
            'I see you Yukari peeking there! You dice stealer!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('dice',_help_dice)


@commands
@Cooldown('user',30.,handler=CooldownHandler())
async def ping(client,message,content):
    await client.message_create(message.channel,f'{client.gateway.latency*1000.:.0f} ms')

async def _help_ping(client,message):
    prefix=client.events.message_create.prefix(message)
    return Embed('ping',(
        'Do you wanna know how bad my connection is to Discord?\n'
        f'Usage: `{prefix}ping\n'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('ping',_help_ping)


@commands
async def message_me(client,message,content):
    channel = await client.channel_private_create(message.author)
    try:
        await client.message_create(channel,'Love you!')
    except DiscordException:
        await client.message_create(message.channel,'Pls turn on private messages from this server!')

async def _help_message_me(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('message_me',(
        'I ll send you something, from really deep of my heart.\n'
        f'Usage : `{prefix}message_me`'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('message_me',_help_message_me)



@commands
@ContentParser('condition, flags=gr, default="not message.channel.permissions_for(message.author).can_manage_messages"',
                'int, default=1',
                'rest, default="f\'{message.author.full_name} asked for it\'"')
async def clear(client,message,limit,reason):
    if limit>0:
        await client.message_delete_sequence(channel=message.channel,limit=limit,reason=reason)

async def _help_clear(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('clear',(
        'I ll clear up the leftover after your lewd messages O-NEE-CHA-N.'
        f'Usage : `{prefix}clear <amount> <reason>`\n'
        '`amount` is optional, by default it is just 1.\n'
        'The `reason`will show up at the audit logs of the guild.'
        ),color=KOISHI_HELP_COLOR).add_footer(
            'This command can be executed only at a guild, and you must have '
            '`manage messages` permission as well.')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('clear',_help_clear,checker=KOISHI_HELPER.check_permission(Permission().update_by_keys(manage_messages=True)))



def check_message_for_emoji(message):
    parsed=parse_emoji(message.content)
    if parsed is None:
        return False
    return parsed

@commands
async def waitemoji(client,message,content):
    channel=message.channel
    
    message_to_delete = await client.message_create(channel,'Waiting!')
    
    try:
        _,emoji = await wait_for_message(client,channel,check_message_for_emoji,30.)
    except TimeoutError:
        return
    finally:
        await client.message_delete(message_to_delete)
    
    await client.message_create(channel,emoji.as_emoji*5)

async def _help_waitemoji(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('waitemoji',(
        'After using this command, I ll wait some time for you to send '
        'an emoji at this channel. If you sent one, I ll send it back five '
        'times instead.\n'
        f'Usage : `{prefix}waitemoji`'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('waitemoji',_help_waitemoji)


@commands
async def subscribe(client,message,content):
    guild=message.guild
    if guild is None:
        return
    role=guild.get_role('Announcements')
    if role is None:
        return
    if role in message.author.guild_profiles[guild].roles:
        await client.user_role_delete(message.author,role)
        text='You succesfully unsubscribed'
    else:
        await client.user_role_add(message.author,role)
        text='You succesfully subscribed'
    await client.message_create(message.channel,text)

async def _help_subscribe(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('subscribe',(
        'I subscribe you for the guild\' `Announcememnts` role, if aplicable.\n'
        'By calling the command again, I ll unsubscribe you, if that is oki.\n'
        f'Usage : `{prefix}subscribe`'
        ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('subscribe',_help_subscribe)


@commands
async def invite(client,message,content):
    guild=message.channel.guild
    if (guild is None):
        return

    if not guild.cached_permissions_for(client).can_create_instant_invite:
        await client.message_create(message.channel,
            'I do not have permission to create Invite from this guild.')
        return

    user=message.author
    owner=client.is_owner(user)
    if (not owner) and (not guild.permissions_for(user).can_create_instant_invite):
        await client.message_create(message.channel,
            'You do not have permission to invoke this command.')
        return

    if content=='perma':
        user=message.author
        if owner or user==guild.owner:
            max_age=0
            max_use=0
        else:
            await client.message_create(message.channel,
                'You must be the owner of the guild, to create a permanent invite.')
            return
    else:
        max_age=21600
        max_use=1
    
    try:
        invite_ = await client.invite_create_pref(guild,max_age,max_use)
    except DiscordException:
        return
                                            
    channel = await client.channel_private_create(message.author)
    await client.message_create(channel,f'Here is your invite, dear:\n\n{invite_.url}')

async def _help_invite(client,message):
    guild=message.channel.guild
    user=message.author
    if guild is None:
        full=False
    else:
        if user==guild.owner:
            full=True
        else:
            full=False

    if not full:
        full=client.is_owner(user)

    prefix=client.events.message_create.prefix(message)
    if full:
        content=(
            'I create an invite for you, to this guild.\n'
            f'Usage: `{prefix}invite (perma)`\n'
            'By passing `perma` after the command, I ll create for you, my dear '
            'A permanent invite to the guild.'
                )
    else:
        content=(
            'I create an invite for you, to this guild.\n'
            f'Usage: `{prefix}invite \n'
                )

    embed=Embed('invite',content,color=KOISHI_HELP_COLOR).add_footer(
        'Guild only. You must have `create instant invite` permission to '
        'invoke this command.')

    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('invite',_help_invite,checker=KOISHI_HELPER.check_permission(Permission().update_by_keys(create_instant_invite=True)))


MINE_MINE_CLEAR = (
    BUILTIN_EMOJIS['white_large_square'].as_emoji,
    BUILTIN_EMOJIS['one'].as_emoji,
    BUILTIN_EMOJIS['two'].as_emoji,
    BUILTIN_EMOJIS['three'].as_emoji,
    BUILTIN_EMOJIS['four'].as_emoji,
    BUILTIN_EMOJIS['five'].as_emoji,
    BUILTIN_EMOJIS['six'].as_emoji,
    BUILTIN_EMOJIS['seven'].as_emoji,
    BUILTIN_EMOJIS['eight'].as_emoji,
    BUILTIN_EMOJIS['bomb'].as_emoji,
        )

MINE_MINE=tuple(f'||{e}||' for e in MINE_MINE_CLEAR)
MINE_CANCEL=BUILTIN_EMOJIS['anger']

class check_emoji_and_user(object):
    __slots__=('emoji', 'user',)
    def __init__(self,emoji,user):
        self.emoji=emoji
        self.user=user
    def __call__(self,emoji,user):
        return (self.emoji is emoji) and (self.user==user)

@commands
async def mine(client,message,content):
    text_mode=False
    amount=0
    if content:
        content=filter_content(content)
        if content[0]=='text':
            text_mode=True
            content.pop(0)
            
        if content and content[0].isdigit():
            amount=int(content[0])
            if amount>24:
                amount=24
            elif amount<8:
                amount=8
    
    if not amount:
        amount=12

        
    data=[0 for x in range(100)]
    
    while amount:
        x=randint(0,9)
        y=randint(0,9)
        position=x+y*10

        value=data[position]
        if value==9:
            continue
        
        local_count=0

        for c_x,c_y in ((-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)):
            local_x=x+c_x
            local_y=y+c_y
            if local_x!=10 and local_x!=-1 and local_y!=10 and local_y!=-1 and data[local_x+local_y*10]==9:
                local_count+=1
        
        if local_count>3:
            continue

        for c_x,c_y in ((-1,-1),(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0)):
            local_x=x+c_x
            local_y=y+c_y
            if local_x!=10 and local_x!=-1 and local_y!=10 and local_y!=-1:
                local_position=local_x+local_y*10
                local_value=data[local_position]
                if local_value==9:
                    continue
                data[local_position]=local_value+1
                
        data[position]=9
        
        amount-=1

    result=[]
    result_sub=[]
    y=0
    while True:
        x=0
        while True:
            result_sub.append(MINE_MINE[data[x+y]])
            x+=1
            if x==10:
                break
        result.append(''.join(result_sub))
        result_sub.clear()
        y+=10
        if y==100:
            break
    
    if text_mode:
        result.insert(0,'```')
        result.append('```')
    else:
        emoji=MINE_CANCEL
        user=message.author
    
    text='\n'.join(result)
    result.clear()
    
    message = await client.message_create(message.channel,text)

    if text_mode or (not message.channel.cached_permissions_for(client).can_add_reactions):
        return
    
    message.weakrefer()
    await client.reaction_add(message,emoji)

    try:
        await wait_for_reaction(client,message,check_emoji_and_user(emoji,user),1200.)
    except TimeoutError:
        return
    finally:
        await client.reaction_delete_own(message,emoji)

    y=0
    while True:
        x=0
        while True:
            result_sub.append(MINE_MINE_CLEAR[data[x+y]])
            x+=1
            if x==10:
                break
        result.append(''.join(result_sub))
        result_sub.clear()
        y+=10
        if y==100:
            break
    text='\n'.join(result)

    await client.message_edit(message,text)

async def _help_mine(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('mine',(
        'I creates a minesweeper game.\n'
        'If you are mad already from failing, just click on the '
        f'{MINE_CANCEL.as_emoji} under the mine.\n'
        f'Usage : `{prefix}mine (text) <bomb_count>`\n'
        'By passing a `text` keyword, I will send the whole mine in a '
        'codeblock, allowing you, to simply copy-paste it.\n'
        'The default bomb count in 12, but you can change it between '
        '8 and 24.'
            ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('mine',_help_mine)


@commands
async def bans(client,message,content):
    guild=message.channel.guild
    if (guild is None):
        return

    if not guild.cached_permissions_for(client).can_ban_users:
        await client.message_create(message.channel,embed=Embed(
            description='I have no permissions to check it.'))
        return

    user=message.author
    if (not client.is_owner(user)) or (not guild.permissions_for(user).can_ban_users):
        await client.message_create(message.channel,embed=Embed('Permission denied.',
                'You must have `ban user` permission to invoke this command'))
        return

    ban_data = await client.guild_bans(guild)

    if not ban_data:
        await client.message_create(message.channel,'None')
        return

    embeds=[]
    maintext=f'Guild bans for {guild.name} {guild.id}:'
    limit=len(ban_data)
    index=0

    while True:
        field_count=0
        embed_length=len(maintext)
        embed=Embed(title=maintext)
        embeds.append(embed)
        while True:
            user,reason=ban_data[index]
            if reason is None:
                reason='Not defined.'
            name=f'{user:f} {user.id}'
            embed_length+=len(reason)+len(name)
            if embed_length>5900:
                break
            embed.add_field(name,reason)
            field_count+=1
            if field_count==25:
                break
            index+=1
            if index==limit:
                break
        if index==limit:
            break
    
    index=0
    field_count=0
    embed_ln=len(embeds)
    result=[]
    while True:
        embed=embeds[index]
        index+=1
        embed.add_footer(f'Page: {index}/{embed_ln}. Bans {field_count+1}-{field_count+len(embed.fields)}/{limit}')
        field_count+=len(embed.fields)
        
        result.append({'embed':embed})
        
        if index==embed_ln:
            break
    
    await Pagination(client,message.channel,result)

async def _help_bans(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('bans',(
        'I ll show you the banned users at the guild.\n'
        f'Usage: `{prefix}bans`'
        ),color=KOISHI_HELP_COLOR).add_footer(
            'Guild only. You must have `ban user` permission to '
            'invoke this command.')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('bans',_help_bans,checker=KOISHI_HELPER.check_permission(Permission().update_by_keys(ban_users=True)))


@commands
async def leave_guild(client,message,content):
    guild=message.channel.guild
    if (guild is None):
        return
    user=message.author
    if (guild.owner!=message.author) or (not client.is_owner(user)):
        return
    await client.guild_leave(guild)

async def _help_leave_guild(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('leave_guild',(
        'You really ant me to leave? :c\n'
        f'Usage: `{prefix}leave_guild`'
        ),color=KOISHI_HELP_COLOR).add_footer(
            'Guild only. You must be the owner of the guild to use this command.')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('leave_guild',_help_leave_guild,checker=KOISHI_HELPER.check_is_guild_owner)

@commands
async def change_prefix(client,message,content):
    guild=message.guild
    if (guild is None) or (message.author!=guild.owner) or (not client.is_owner(message.author)) or (not content):
        return
    content=filter_content(content)[0]
    if not (0<len(content)<33):
        text=f'Prefix lenght should be between 1 and 32, got {len(content)}.'
    elif '`' in content:
        text=f'The prefix should not include `\`` in it.'
    elif PREFIXES.add(guild,content):
        text='Prefix modified.'
    else:
        text='Thats the frefix already.'
    await client.message_create(message.channel,text)

async def _help_change_prefix(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('change_prefix',(
        'Do you have any preferred prefix for my commands?\n'
        f'Usage: `{prefix}chnage_prefix *prefix*`'
        ),color=KOISHI_HELP_COLOR).add_footer(
            'Guild only. You must be the owner of the guild to use this command.')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('change_prefix',_help_change_prefix,checker=KOISHI_HELPER.check_is_guild_owner)



@commands
async def yuno(client,message,content):
    await client.message_create(message.channel,embed=Embed('YUKI YUKI YUKI!',
        '░░░░░░░░░░░▄▄▀▀▀▀▀▀▀▀▄▄░░░░░░░░░░░░░\n'
        '░░░░░░░░▄▀▀░░░░░░░░░░░░▀▄▄░░░░░░░░░░\n'
        '░░░░░░▄▀░░░░░░░░░░░░░░░░░░▀▄░░░░░░░░\n'
        '░░░░░▌░░░░░░░░░░░░░▀▄░░░░░░░▀▀▄░░░░░\n'
        '░░░░▌░░░░░░░░░░░░░░░░▀▌░░░░░░░░▌░░░░\n'
        '░░░▐░░░░░░░░░░░░▒░░░░░▌░░░░░░░░▐░░░░\n'
        '░░░▌▐░░░░▐░░░░▐▒▒░░░░░▌░░░░░░░░░▌░░░\n'
        '░░▐░▌░░░░▌░░▐░▌▒▒▒░░░▐░░░░░▒░▌▐░▐░░░\n'
        '░░▐░▌▒░░░▌▄▄▀▀▌▌▒▒░▒░▐▀▌▀▌▄▒░▐▒▌░▌░░\n'
        '░░░▌▌░▒░░▐▀▄▌▌▐▐▒▒▒▒▐▐▐▒▐▒▌▌░▐▒▌▄▐░░\n'
        '░▄▀▄▐▒▒▒░▌▌▄▀▄▐░▌▌▒▐░▌▄▀▄░▐▒░▐▒▌░▀▄░\n'
        '▀▄▀▒▒▌▒▒▄▀░▌█▐░░▐▐▀░░░▌█▐░▀▄▐▒▌▌░░░▀\n'
        '░▀▀▄▄▐▒▀▄▀░▀▄▀░░░░░░░░▀▄▀▄▀▒▌░▐░░░░░\n'
        '░░░░▀▐▀▄▒▀▄░░░░░░░░▐░░░░░░▀▌▐░░░░░░░\n'
        '░░░░░░▌▒▌▐▒▀░░░░░░░░░░░░░░▐▒▐░░░░░░░\n'
        '░░░░░░▐░▐▒▌░░░░▄▄▀▀▀▀▄░░░░▌▒▐░░░░░░░\n'
        '░░░░░░░▌▐▒▐▄░░░▐▒▒▒▒▒▌░░▄▀▒░▐░░░░░░░\n'
        '░░░░░░▐░░▌▐▐▀▄░░▀▄▄▄▀░▄▀▐▒░░▐░░░░░░░\n'
        '░░░░░░▌▌░▌▐░▌▒▀▄▄░░░░▄▌▐░▌▒░▐░░░░░░░\n'
        '░░░░░▐▒▐░▐▐░▌▒▒▒▒▀▀▄▀▌▐░░▌▒░▌░░░░░░░\n'
        '░░░░░▌▒▒▌▐▒▌▒▒▒▒▒▒▒▒▐▀▄▌░▐▒▒▌░░░░░░░\n'
        ,0xffafde,'https://www.youtube.com/watch?v=NI_fgwbmJg0&t=0s'))
    
async def _help_yuno(client,message):
    embed=Embed('yuno',(
        'Your personal yandere.\n'
        'Good luck, I better leave now!'
            ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('yuno',_help_yuno,)


valuable_scopes = [
    'identify',
    'connections',
    'guilds',
    'guilds.join',
    'email',
    'applications.builds.read',
    'applications.builds.upload',
    'applications.entitlements',
    'applications.store.update',
        ]

OA2_accesses={}

@commands
async def oa2_link(client,message,content): #just a test link
    if not client.is_owner(message.author):
        return

    await client.message_create(message.channel,(
        'https://discordapp.com/oauth2/authorize?client_id=486565096164687885'
        '&redirect_uri=https%3A%2F%2Fgithub.com%2FHuyaneMatsu'
        '&response_type=code&scope=identify%20connections%20guilds%20guilds.join'
        '%20email%20applications.builds.read'
        '%20applications.builds.upload%20applications.entitlements'
        '%20applications.store.update'))

async def _help_oa2_link(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('oa2_link',(
        'I ll give you a nice authorization link for some oauth 2 scopes.\n'
        f'Usage: `{prefix}oa2_link`\n'
        'After you authorized yourself, you should call the `oa2_feed` '
        'command, to feed the authorized link to me.\n'
        f'Example: `{prefix}oa2_feed *link*`\n'
        'By doing this you will unlock other oauth 2 commands, like:\n'
        f'- `{prefix}oa2_user <user_id>`\n'
        f'- `{prefix}oa2_connections <user_id>`\n'
        f'- `{prefix}oa2_guilds <user_id>`\n'
        f'- `{prefix}oa2_my_guild <user_id>`\n'
        f'- `{prefix}oa2_renew <user_id>`'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('oa2_link',_help_oa2_link,KOISHI_HELPER.check_is_owner)


@commands
async def oa2_feed(client,message,content):
    if not client.is_owner(message.author):
        return

    Task(client.message_delete(message),client.loop)
    try:
        result=others.parse_oauth2_redirect_url(content)
    except ValueError:
        await client.message_create(message.channel,'Bad link')
        return

    access = await client.activate_authorization_code(*result,valuable_scopes)

    if access is None:
        await client.message_create(message.channel,'Too old link')
        return
    user = await client.user_info(access)
    OA2_accesses[user.id]=user
    await client.message_create(message.channel,'Thanks')

async def _help_oa2_feed(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('oa2_feed',(
        'Feeds your oauth 2 authorized redirect url.\n'
        f'Usage: `{prefix}oa2_feed *link*`\n'
        f'How to get an oauth 2 authorization url?, use: `{prefix}oa2_link`\n'
        'By doing this you will unlock other oauth 2 commands, like:\n'
        f'- `{prefix}oa2_user <user_id>`\n'
        f'- `{prefix}oa2_connections <user_id>`\n'
        f'- `{prefix}oa2_guilds <user_id>`\n'
        f'- `{prefix}oa2_my_guild <user_id>`\n'
        f'- `{prefix}oa2_renew <user_id>`'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('oa2_feed',_help_oa2_feed,KOISHI_HELPER.check_is_owner)


def _oa2_query(message,content):
    author_id=message.author.id
    if not (16<len(content)<33):
        return OA2_accesses.get(author_id,None)
    try:
        user_id=int(content)
    except ValueError:
        return OA2_accesses.get(author_id,None)
    
    user=OA2_accesses.get(user_id,None)
    if user is None:
        user=OA2_accesses.get(author_id,None)
    return user

@commands
async def oa2_user(client,message,content):
    if not client.is_owner(message.author):
        return

    user=_oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(user)])

async def _help_oa2_user(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('oa2_user',(
        'After you authorized yourself, I will know your deepest secrets :3\n'
        'Using this command, I ll show the extra user information , I '
        'received.\n'
        f'Usage: `{prefix}oa2_user <user_id>`\n'
        'Well, every other owner will know it too, by passing your id, '
        'so take care, you can not trust them! *Only me!*\n'
        'If you dont know how to authorize yourself; use : '
        f'`{prefix}help oa2_link`'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('oa2_user',_help_oa2_user,KOISHI_HELPER.check_is_owner)



@commands
async def oa2_connections(client,message,content):
    if not client.is_owner(message.author):
        return

    user=_oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    connections = await client.user_connections(user.access)
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(connections)])

async def _help_oa2_connections(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('oa2_connections',(
        'After you authorized yourself, I will know your deepest secrets :3\n'
        'You might ask what are your connections. '
        'Those are your connected apps and sites.\n'
        f'Usage: `{prefix}oa2_connections <user_id>`\n'
        'Well, every other owner will know it too, by passing your id, '
        'so take care, you can not trust them! *Only me!*\n'
        'If you dont know how to authorize yourself; use : '
        f'`{prefix}help oa2_link`'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)
    
KOISHI_HELPER.add('oa2_connections',_help_oa2_connections,KOISHI_HELPER.check_is_owner)

    
@commands
async def oa2_guilds(client,message,content):
    if not client.is_owner(message.author):
        return

    user=_oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    guilds = await client.user_guilds(user.access)
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(guilds)])

async def _help_oa2_guilds(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('oa2_guilds',(
        'After you authorized yourself, I will know your deepest secrets :3\n'
        'By using this command, I ll show your guilds. '
        '*And everything, what I know about them.*\n'
        f'Usage: `{prefix}oa2_guilds <user_id>`\n'
        'Well, every other owner will know it too, by passing your id, '
        'so take care, you can not trust them! *Only me!*\n'
        'If you dont know how to authorize yourself; use : '
        f'`{prefix}help oa2_link`'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('oa2_guilds',_help_oa2_guilds,KOISHI_HELPER.check_is_owner)


@commands
async def oa2_my_guild(client,message,content):
    if not client.is_owner(message.author):
        return

    user=_oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    try:
        guild = await client.guild_create(name='Luv ya',
            channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=ChannelText),])

        await sleep(1.,client.loop)
        await client.guild_user_add(guild,user)
        await sleep(1.,client.loop)
        await client.guild_edit(guild,owner=user)
    except Exception as err:
        sys.stderr.write(''.join(render_exc_to_list(err,['Exception occured at oa2_my_guild\n'])))
    finally:
        try:
            guild
        except UnboundLocalError:
            return
        await sleep(1.,client.loop)
        if client is guild.owner:
            await client.guild_delete(guild)
        else:
            await client.guild_leave(guild)

async def _help_oa2_my_guild(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('my_guild',(
        'After you authorized yourself, I can create a guild for you, '
        'so just sit back!\n'
        f'Usage: `{prefix}oa2_my_guild <user_id>`\n'
        'Other owners can create a guild for you, after you authorized, '
        'take care!\n'
        'If you dont know how to authorize yourself, use : '
        f'`{prefix}help oa2_link`'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('my_guild',_help_oa2_my_guild,KOISHI_HELPER.check_is_owner)


# Deprecated because it does not works with teams.
#@commands
#async def oa2_owners(client,message,content):
#    if not client.is_owner(message.author):
#        return
#
#    access = await client.owners_access(valuable_scopes)
#    user = await client.user_info(access)
#    OA2_accesses[user.id]=user
#    result=[f'queried {user:f}']
#    for scope in access.scopes:
#        result.append(f'- {scope}')
#
#    text='\n'.join(result)
#
#    await client.message_create(message.channel,text)
    
@commands
async def oa2_renew(client,message,content):
    if not client.is_owner(message.author):
        return

    user=_oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    access=user.access
    last=access.created_at
    await client.renew_access_token(access)
    new=access.created_at
    await client.message_create(message.channel,
        f'{user:f}\' access token got renewed.\n'
        f'From creation time at: {last:%Y.%m.%d-%H:%M:%S}\n'
        f'To creation time at: {new:%Y.%m.%d-%H:%M:%S}'
            )

async def _help_oa2_renew(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('oa2_renew',(
        'Your oauth2 authorization might expire; with this command you can '
        'renew it.\n'
        f'Usage: `{prefix}oa2_renew <user_id>`\n'
        'Other owners can renew it for you as well!\n'
        'If you dont know how to authorize yourself;\n'
        f'Use : `{prefix}help oa2_link`'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('oa2_renew',_help_oa2_renew,KOISHI_HELPER.check_is_owner)



@commands
@ContentParser('emoji')
async def se(client,message,emoji):
    if emoji.is_custom_emoji():
        await client.message_create(message.channel,f'**Name:** {emoji:e} **Link:** {emoji.url}')

async def _help_se(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('se',(
        '`se` stands for `show emoji`.\n'
        f'Usage: `{prefix}se *emoji*`\n'
        'I can show only custom emojis.'
            ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('se',_help_se)


@commands
@ContentParser('condition, flags=r, default="not client.is_owner(message.author)"',
                'int',
                'channel, flags=mnig, default="message.channel"',)
async def resend_webhook(client,message,message_id,channel):
    permissions=message.channel.cached_permissions_for(client)
    can_delete=permissions.can_manage_messages
    
    if not permissions.can_manage_webhooks:
        message = await client.message_create(message.channel,
            'I have no permissions to get webhooks from this channel.')
        if can_delete:
            await sleep(30.0,client.loop)
            await client.message_delete(message)
        return
    
    try:
        target_message = await client.message_get(channel,message_id)
    except DiscordException as err:
        message = await client.message_create(message.channel,err.__repr__())
        if can_delete:
            await sleep(30.0,client.loop)
            await client.message_delete(message)
        return

    webhooks = await client.webhook_get_channel(channel)
    if webhooks:
        webhook=webhooks[0]
    else:
        webhook = await client.webhook_create(channel,'Love You')

    await client.webhook_send(webhook,
        embed=target_message.embeds,
        name=target_message.author.name,
        avatar_url=target_message.author.avatar_url)

async def _help_resend_webhook(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('resend_webhook',(
        'I can resend a webhook, if chu really want.\n'
        f'Usage: `{prefix}resend_webhook *message_id* <channel>`\n'
        'The `message_id` must be the `id` of the message sent by the '
        'webhook.\n'
        'The `channel` by default is zhis channel, but if the message '
        'is at a different channel, you should tell me > <.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Guild only. Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('resend_webhook',_help_resend_webhook,KOISHI_HELPER.check_is_owner)


@commands
@ContentParser('int', 'int, default="0"',)
async def random(client,message,v1,v2):
    result=randint(v2,v1) if v1>v2 else randint(v1,v2)
    await client.message_create(message.channel,str(result))

async def _help_random(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('random',(
        'Do you need some random numbers?\n'
        f'Usage: `{prefix}random *number_1* <number_2>`\n'
        'You should pass at least 1 number. The second is optinal and by '
        'default is `0`.'),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('random',_help_random)


async def _pararell_load(client,channel,future):
    try:
        await client.message_at_index(channel,256256256) #gl
    except (IndexError,PermissionError) as err:
        pass
    except BaseException as err:
        sys.stderr.write(''.join(render_exc_to_list(err,['Exception occured at pararell_load\nTraceback (most recent call last):\n'])))
    finally:
        future.set_result(None)
    
@commands
async def count_messages(client,message,content):
    if not client.is_owner(message.author):
        return
    source_channel=message.channel
    guild=source_channel.guild
    if guild is None:
        return
    
    loop=client.loop
    channels=guild.messageable_channels
    future=FutureWM(loop,len(channels))
    users={}
    
    with client.keep_typing(source_channel):
        for channel in channels:
            Task(_pararell_load(client,channel,future),client.loop)

        await future
        
        for channel in channels:
            for message in channel.messages:
                user=message.author
                if type(user) in (Client,User):
                    users[user]=users.get(user,0)+1
    users=list(users.items())
    users.sort(reverse=True,key=lambda item:item[1])
    text=[f'{index}.: {user:f} : {count}' for index,(user,count) in enumerate(users,1)]
    chunks=[{'content':chunk} for chunk in others.chunkify(text)]
    await Pagination(client,source_channel,chunks)

async def _help_count_messages(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('count_messages',(
        'I mastered math for a long time, I can count who and how much messages '
        'sent at the guild!\n'
        f'Usage: `{prefix}count_messages`\n'
        'This command takes a while and it is not guaranteed, that it '
        'will finish without an error.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Guild only. Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('count_messages',_help_count_messages,KOISHI_HELPER.check_is_owner)


async def _pararell_load_reactions(client,channel,future,reactions):
    try:
        await client.message_at_index(channel,256256256) #gl
    except (IndexError,PermissionError) as err:
        pass
    except BaseException as err:
        sys.stderr.write(''.join(render_exc_to_list(err,['Exception occured at pararell_load_reactions\nTraceback (most recent call last):\n'])))
    finally:
        messages=[message for message in channel.messages if message.reactions]
        for message in messages:
            try:
                await client.reaction_load_all(message)
            except DiscordException:
                continue
            for emoji,reacters in message.reactions.items():
                for user in reacters:
                    try:
                        user_s=reactions[user]
                    except KeyError:
                        user_s=reactions[user]={}
                    user_s[emoji]=user_s.get(emoji,0)+1

        future.set_result(None)
    
@commands
async def count_reactions(client,message,content):
    if not client.is_owner(message.author):
        return
    source_channel=message.channel
    guild=source_channel.guild
    if guild is None:
        return
    
    loop=client.loop
    channels=guild.messageable_channels
    future=FutureWM(loop,len(channels))
    reactions={}
    
    with client.keep_typing(source_channel):
        for channel in channels:
            Task(_pararell_load_reactions(client,channel,future,reactions),client.loop)

        await future

    sorted_reactions=[]
    for user,emojis in reactions.items():
        emoji_count=sum(emojis.values())
        emojis=list(emojis.items())
        emojis.sort(reverse=True,key=lambda item:item[1])
        sorted_reactions.append((user,emojis,emoji_count),)
        
    sorted_reactions.sort(reverse=True,key=lambda item:item[2])

    text=[]
    for index,(user,emojis,amount) in enumerate(sorted_reactions,1):
        text.append(f'{index}.: {user:f} {amount}')
        for index,(emoji,emoji_count) in enumerate(emojis,1):
            text.append(f' - {index} {emoji:e} {emoji_count}')
    
    chunks=[{'content':chunk} for chunk in others.chunkify(text)]
    await Pagination(client,source_channel,chunks)        

async def _help_count_reactions(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('count_reactions',(
        'Do you want me to count every reaction at your guild ever sent?\n'
        f'Usage: `{prefix}count_reactions`\n'
        'This command takes a while and it is not guaranteed, that it '
        'will finish without an error.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Guild only. Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('count_reactions',_help_count_reactions,KOISHI_HELPER.check_is_owner)


@commands
@ContentParser('condition, flags=r, default="not client.is_owner(message.author)"',
                'user, flags=mna, default="client"',)
async def update_application_info(client,message,user):
    if type(user) is Client:
        await user.update_application_info()
        text=f'Application info of `{user:f}` is updated succesfully!'
    else:
        text='I can update application info only of a client'
    await client.message_create(message.channel,text)

HTML_RP=re.compile('#?([0-9a-f]{6})',re.I)
REGULAR_RP=re.compile('([0-9]{1,3})\,? *([0-9]{1,3})\,? *([0-9]{1,3})')

async def _help_update_application_info(client,message):
    prefix=client.events.message_create.prefix(message)
    embed=Embed('update_application_info',(
        'I can update applicaction info of any of the active clients '
        'at my mansion.\n'
        f'Usage: `{prefix}update_application_info <user>`\n'
        '`user` is otional and can be only an another client.'
            ),color=KOISHI_HELP_COLOR).add_footer(
            'Owner only!')
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('update_application_info',_help_update_application_info,KOISHI_HELPER.check_is_owner)


@commands(case='color')
async def command_color(client,message,content):
    while True:
        parsed=HTML_RP.fullmatch(content)
        if parsed is not None:
            full_color=int(parsed.group(1),base=16)
            color_r=(full_color&0xff0000)>>16
            color_g=(full_color&0x00ff00)>>8
            color_b=(full_color&0x00ff)
            break
        
        parsed=REGULAR_RP.fullmatch(content)
        if parsed is not None:
            color_r,color_g,color_b=parsed.groups()
            color_r=int(color_r)
            if color_r>255:
                return
            color_g=int(color_g)
            if color_g>255:
                return
            color_b=int(color_b)
            if color_b>255:
                return
            full_color=(color_r<<16)|(color_g<<8)|color_b
            break
            
        return
    
    color=(color_r,color_g,color_b)
    
    embed=Embed(content,color=full_color)
    embed.add_image('attachment://color.png')
    
    with ReuBytesIO() as buffer:
        image=PIL.new('RGB',(120,30),color)
        image.save(buffer,'png')
        buffer.seek(0)
        
        await client.message_create(message.channel,embed=embed,file=('color.png',buffer))

async def _help_color(client,message):
    prefix=client.events.message_crate.prefix(message)
    embed=Embed('color',(
        'Do you wanna see a color?\n'
        f'Usage: `{prefix}color *color*`\n'
        'I accept regular RGB or HTML color format.'
            ),color=KOISHI_HELP_COLOR)
    await client.message_create(message.channel,embed=embed)

KOISHI_HELPER.add('color',_help_color)

del Cooldown
del CooldownHandler
