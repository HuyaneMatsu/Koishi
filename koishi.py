import re, traceback
from random import randint

from hata.parsers import eventlist
from hata.client_core import CLIENTS
from hata.oauth2 import SCOPES
from hata.events_compiler import content_parser
from hata.user import User
from hata.client import Client
from hata.prettyprint import pchunkify
from hata.futures import CancelledError,sleep,Future_WM,Task
from hata.events import Pagination,wait_for_message,wait_for_reaction,cooldown,prefix_by_guild
from hata.channel import cr_pg_channel_object,Channel_text
from hata import others
from hata.exceptions import DiscordException
from hata.emoji import BUILTIN_EMOJIS,parse_emoji
from hata.others import filter_content
from hata.guild import Guild,GUILDS
from hata.role import Role
from hata.embed import Embed

import image_handler
from help_handler import on_command_help,HELP,invalid_command
from ratelimit_tests import ratelimit_commands
from kanako import kanako_manager
from dungeon_sweeper import ds_manager,_DS_modify_best
from voice import voice
from dispatch_tests import dispatch_tester
from battleships import battle_manager
from infos import infos,update_about
from tools import cooldown_handler, BeautifulSoup
from gambling import gambling
import channeller
import pers_data
import models

PREFIXES=prefix_by_guild(pers_data.PREFIX,models.DB_ENGINE,models.PREFIX_TABLE,models.pefix_model)

del pers_data
del prefix_by_guild
del models

class once_on_ready:
    __slots__ = ['called',]
    __event_name__='ready'
    def __init__(self):
        self.called=False
    async def __call__(self,client):
        if self.called:
            update_about(client)
            return
        self.called=True

        print(f'{client:f} ({client.id}) logged in')
        await client.update_application_info()
        print(f'owner: {client.owner:f} ({client.owner.id})')
        update_about(client)

commands=eventlist()

commands(image_handler.on_command_upload,'upload')
commands(image_handler.on_command_image,'image')
commands(on_command_help,'help')
commands(invalid_command)
commands.extend(ratelimit_commands)
commands(kanako_manager,'kanako')
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
        if _KOISHI_NOU_RP.match(content) is not None:
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
@content_parser('user, flags=mna, default="message.author"')
async def rate(client,message,target):
    if target in CLIENTS or client.is_owner(target):
        result=10
    else:
        result=target.id%11
    #nickname check
    await client.message_create(message.channel,f'I rate {target.name_at(message.guild)} {result}/10')


@commands
@content_parser('int, default="1"')
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

@commands
@cooldown(30.,'user',handler=cooldown_handler())
async def ping(client,message,content):
    await client.message_create(message.channel,f'{int(client.kokoro.latency*1000.)} ms')


@commands
async def message_me(client,message,content):
    channel = await client.channel_private_create(message.author)
    try:
        await client.message_create(channel,'Love you!')
    except DiscordException:
        await client.message_create(message.channel,'Pls turn on private messages from this server!')

@commands
@content_parser('condition, flags=gr, default="not message.channel.permissions_for(message.author).can_manage_messages"',
                'int, default=1',
                'rest, default="f\'{message.author:f} asked for it\'"')
async def clear(client,message,limit,reason):
    if limit>0:
        await client.message_delete_sequence(channel=message.channel,limit=limit,reason=reason)

@commands
async def waitemoji(client,message,content):
    channel=message.channel
    
    message_to_delete = await client.message_create(channel,'Waiting!')
    
    try:
        _,emoji = await wait_for_message(client,channel,lambda message:parse_emoji(message.content),30.)
    except TimeoutError:
        emoji=None
    except Exception as err:
        return
    
    try:
        await client.message_delete(message_to_delete)
    except DiscordException:
        pass
    
    if emoji is not None:
        await client.message_create(channel,emoji.as_emoji*5)

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

@commands
async def invite(client,message,content):
    guild=message.guild
    if guild is None or not guild.permissions_for(message.author).can_create_instant_invite:
        return

    if message.author is guild.owner and content=='perma':
        max_age=0
        max_use=0
    else:
        max_age=21600
        max_use=1
    
    try:
        invite = await client.invite_create_pref(guild,max_age,max_use)
    except DiscordException:
        return
                                            
    channel = await client.channel_private_create(message.author)
    await client.message_create(channel,f'Here is your invite, dear:\n\n{invite.url}')

mine_mine_clear = (
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

mine_mine=tuple(f'||{e}||' for e in mine_mine_clear)

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
            result_sub.append(mine_mine[data[x+y]])
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
        emoji=BUILTIN_EMOJIS['anger']
        user=message.author
    
    text='\n'.join(result)
    result.clear()
    
    message = await client.message_create(message.channel,text)

    if text_mode:
        return
    
    message.weakrefer()
    await client.reaction_add(message,emoji)
    
    try:
        await wait_for_reaction(client,message,
            lambda emoji,user,v0=emoji,v1=user:emoji is v0 and user is v1,
            1200.)
    except TimeoutError:
        return
    finally:
        try:
            await client.reaction_delete_own(message,emoji)
        except DiscordException:
            pass
    
    y=0
    while True:
        x=0
        while True:
            result_sub.append(mine_mine_clear[data[x+y]])
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

@commands
async def bans(client,message,content):
    guild=message.guild
    if guild is None:
        return
    if not guild.permissions_for(client).can_ban_user:
        return await client.message_create(message.channel,embed=Embed(description='I have no permissions to check it.'))
                                 
    ban_data = await client.guild_bans(guild)

    if not ban_data:
        await client.message_create(message.channel,'None')
        return
        
    ban_index=0
    embeds=[]
    maintext=f'Guild bans for {guild.name} {guild.id}:'
    limit=len(ban_data)
    index=0

    while True:
        field_index=0       
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
            if embed_length>7900:
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

@commands
async def leave_guild(client,message,content):
    guild=message.guild
    if guild is None or guild.owner is not message.author:
        return
    await client.guild_leave(guild)
    
@commands
async def change_prefix(client,message,content):
    guild=message.guild
    if (guild is None) or (message.author is not guild.owner) or (not content):
        return
    content=filter_content(content)[0]
    if not (0<len(content)<33):
        text=f'Prefix lenght should be between 1 and 32, got {len(content)}.'
    elif PREFIXES.add(guild,content):
        text='Prefix modified.'
    else:
        text='Thats the frefix already.'
    await client.message_create(message.channel,text)

@commands
async def _change_prefix(client,message,content):
    if not client.is_owner(message.author):
        return
    content=filter_content(content)
    if len(content)<2:
        return
    if not (0<len(content[1])<33):
        return
    
    try:
        guild=GUILDS[int(content[0])]
    except (ValueError,KeyError):
        guild=client.get_guild(content[0])
        if guild is None:
            return
    if PREFIXES.add(guild,content[1]):
        text='Done.'
    else:
        text='No modifications took place.'

    await client.message_create(message.channel,text)

@commands
async def nikki(client,message,content):
    await client.message_create(message.channel,embed=Embed('YUKI YUKI YUKI!','''
        ░░░░░░░░░░░▄▄▀▀▀▀▀▀▀▀▄▄░░░░░░░░░░░░░
        ░░░░░░░░▄▀▀░░░░░░░░░░░░▀▄▄░░░░░░░░░░
        ░░░░░░▄▀░░░░░░░░░░░░░░░░░░▀▄░░░░░░░░
        ░░░░░▌░░░░░░░░░░░░░▀▄░░░░░░░▀▀▄░░░░░
        ░░░░▌░░░░░░░░░░░░░░░░▀▌░░░░░░░░▌░░░░
        ░░░▐░░░░░░░░░░░░▒░░░░░▌░░░░░░░░▐░░░░
        ░░░▌▐░░░░▐░░░░▐▒▒░░░░░▌░░░░░░░░░▌░░░
        ░░▐░▌░░░░▌░░▐░▌▒▒▒░░░▐░░░░░▒░▌▐░▐░░░
        ░░▐░▌▒░░░▌▄▄▀▀▌▌▒▒░▒░▐▀▌▀▌▄▒░▐▒▌░▌░░
        ░░░▌▌░▒░░▐▀▄▌▌▐▐▒▒▒▒▐▐▐▒▐▒▌▌░▐▒▌▄▐░░
        ░▄▀▄▐▒▒▒░▌▌▄▀▄▐░▌▌▒▐░▌▄▀▄░▐▒░▐▒▌░▀▄░
        ▀▄▀▒▒▌▒▒▄▀░▌█▐░░▐▐▀░░░▌█▐░▀▄▐▒▌▌░░░▀
        ░▀▀▄▄▐▒▀▄▀░▀▄▀░░░░░░░░▀▄▀▄▀▒▌░▐░░░░░
        ░░░░▀▐▀▄▒▀▄░░░░░░░░▐░░░░░░▀▌▐░░░░░░░
        ░░░░░░▌▒▌▐▒▀░░░░░░░░░░░░░░▐▒▐░░░░░░░
        ░░░░░░▐░▐▒▌░░░░▄▄▀▀▀▀▄░░░░▌▒▐░░░░░░░
        ░░░░░░░▌▐▒▐▄░░░▐▒▒▒▒▒▌░░▄▀▒░▐░░░░░░░
        ░░░░░░▐░░▌▐▐▀▄░░▀▄▄▄▀░▄▀▐▒░░▐░░░░░░░
        ░░░░░░▌▌░▌▐░▌▒▀▄▄░░░░▄▌▐░▌▒░▐░░░░░░░
        ░░░░░▐▒▐░▐▐░▌▒▒▒▒▀▀▄▀▌▐░░▌▒░▌░░░░░░░
        ░░░░░▌▒▒▌▐▒▌▒▒▒▒▒▒▒▒▐▀▄▌░▐▒▒▌░░░░░░░
        ''',0xffafde,'https://www.youtube.com/watch?v=NI_fgwbmJg0&t=0s'))
valuable_scopes=[scope for scope in SCOPES if scope[0] not in 'mrw']

OA2_accesses={}

@commands
async def oa2_link(client,message,content): #just a test link
    await client.message_create(message.channel,'https://discordapp.com/oauth2/authorize?client_id=486565096164687885&redirect_uri=https%3A%2F%2Fgithub.com%2FHuyaneMatsu&response_type=code&scope=identify%20connections%20guilds%20guilds.join%20email')

@commands
async def oa2_feed(client,message,content):
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
    
def oa2_query(message,content):
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
    user=oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(user)])


@commands
async def oa2_connections(client,message,content):
    user=oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    connections = await client.user_connections(user.access)
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(connections)])
    
    
@commands
async def oa2_guilds(client,message,content):
    user=oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    guilds = await client.user_guilds(user.access)
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(guilds)])
    
@commands
async def oa2_my_guild(client,message,content):
    user=oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    if (not client.is_owner(message.author)) and user!=message.author:
        await client.message_create(message.channel,'NOPE, do it on yourself!')
        return
    
    try:
        guild = await client.guild_create(name='Luv ya',
            channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=Channel_text),])

        await sleep(1.,client.loop)
        await client.guild_user_add(guild,user)
        await sleep(1.,client.loop)
        await client.guild_edit(guild,owner=user)
    except Exception as err:
        print(err)
        traceback.print_exc()
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
        
@commands
async def oa2_owners(client,message,content):
    if not client.is_owner(message.author):
        return

    access = await client.owners_access(valuable_scopes)
    user = await client.user_info(access)
    OA2_accesses[user.id]=user
    result=[f'queried {user:f}']
    for scope in access.scopes:
        result.append(f'- {scope}')

    text='\n'.join(result)
                 
    await client.message_create(message.channel,text)
    
@commands
async def oa2_renew(client,message,content):
    user=oa2_query(message,content)
    if user is None:
        await client.message_create(message.channel,'Could not find that user')
        return
    
    access=user.access
    last=access.created_at
    await client.renew_access_token(access)
    new=access.created_at
    await client.message_create(message.channel,f'{user:f}\' access token got renewed.\nFrom creation time at: {last:%Y.%m.%d-%H:%M:%S}\nTo creation time at: {new:%Y.%m.%d-%H:%M:%S}')

@commands
async def OG(client,message,content):
    if not client.is_owner(message.author):
        return
    
    access = await client.owners_access(valuable_scopes)
    user = await client.user_info(access)

    guild = await client.guild_create(name=content,
        channels=[cr_pg_channel_object(name='general',type_=Channel_text),])

    await sleep(1.,client.loop)
    role = await client.role_create(guild,'my dear',8)
    await client.guild_user_add(guild,user,roles=[role])
    await sleep(1.,client.loop)
    
@commands
async def download(self,message,content):
    if message.author is not self.owner:
        return
    data = await self.download_url(content)
    soup = BeautifulSoup(data,'html.parser',from_encoding='utf-8')
    text = soup.prettify()
    result = [{'content':element} for element in others.cchunkify(text.splitlines())]
    await Pagination(self,message.channel,result)

@commands
@content_parser('emoji')
async def se(client,message,emoji):
    if emoji.is_custom_emoji:
        await client.message_create(message.channel,f'**Name:** {emoji:e} **Link:** {emoji.url}')


@commands
async def nitro(client,message,content):
    if message.permissions.can_manage_messages:
        Task(client.message_delete(message),client.loop)
    content=filter_content(content)
    
    if not content:
        return
    
    text_form=content[0]
    
    emoji=parse_emoji(text_form)
    
    if emoji is None:
        
        for guild in client.guilds.values():
            emoji=guild.get_emoji(text_form)
            if emoji is not None:
                break
        
        if emoji is None:
            return
        
    else:
        if emoji.is_custom_emoji:
            found=False
            for guild in client.guilds.values():
                if emoji.id in guild.emojis:
                    found=True
                    break
            
            if found==False:
                return
    
    await client.message_create(message.channel,emoji.as_emoji)

@commands
@content_parser('condition, flags=r, default="not client.is_owner(message.author)"',
                'int',
                'channel, flags=mnig, default="message.channel"',)
async def resend_webhook(client,message,message_id,channel):
    try:
        target_message = await client.message_get(channel,message_id)
    except Exception as err:
        await client.message_create(message.channel,err.__class__.__name__)
        return

    webhooks = await client.webhook_get_channel(channel)
    webhook=webhooks[0]

    await client.webhook_send(webhook,
        embed=target_message.embeds,
        name=target_message.author.name,
        avatar_url=target_message.author.avatar_url)

@commands
@content_parser('int', 'int, default="0"',)
async def random(client,message,v1,v2):
    result=randint(v2,v1) if v1>v2 else randint(v1,v2)
    await client.message_create(message.channel,str(result))

async def pararell_load(client,channel,future):
    try:
        await client.message_at_index(channel,256256256) #gl
    except (IndexError,PermissionError) as err:
        pass
    except BaseException as err:
        traceback.print_exc()
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
    future=Future_WM(loop,len(channels))
    users={}
    
    with client.keep_typing(source_channel):
        for channel in channels:
            Task(pararell_load(client,channel,future),client.loop)

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

async def pararell_load_reactions(client,channel,future,reactions):
    try:
        await client.message_at_index(channel,256256256) #gl
    except (IndexError,PermissionError) as err:
        pass
    except BaseException as err:
        traceback.print_exc()
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
    future=Future_WM(loop,len(channels))
    reactions={}
    
    with client.keep_typing(source_channel):
        for channel in channels:
            Task(pararell_load_reactions(client,channel,future,reactions),client.loop)

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

@commands
@content_parser('delta, default="None"')
async def parse_timedelta(client,message,delta):
    await client.message_create(message.channel,(repr(delta)))            
