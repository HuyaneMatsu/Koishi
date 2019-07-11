# -*- coding: utf-8 -*-
from random import choice
import sys
import json

from hata.dereaddons_local import asyncinit
from hata.futures import Task
from hata.parsers import eventlist
from hata.channel import message_at_index,Channel_text,Channel_category,CHANNELS
from hata.prettyprint import pchunkify
from hata.others import elapsed_time,Status,Audit_log_event,cchunkify
from hata.exceptions import DiscordException
from hata.events import Pagination,waitfor_wrapper
from hata.events_compiler import content_parser
from hata.embed import Embed
from hata.emoji import BUILTIN_EMOJIS
from hata.color import Color
from hata.user import USERS
from hata.guild import GUILDS
from hata.client_core import CLIENTS

from help_handler import HELP

async def no_permission(client,message,*args):
    if args:
        await client.message_create(message.channel,'You do not have permission to use this command!')

class show_help:
    __slots__=['embed']
    __async_call__=True
    def __init__(self,name):
        self.embed=HELP[name]
    def __call__(self,client,message,*args):
        return client.message_create(message.channel,embed=self.embed)

infos=eventlist()

@infos.add('user')
@content_parser('user, flags="mna", default="message.author"')
async def user_info(client,message,user):
    guild=message.guild

    embed=Embed(user.full_name)
    embed.add_field('User Information',
        f'Created: {elapsed_time(user.created_at)} ago\n'
        f'Profile: {user:m}\n'
        f'ID: {user.id}')

    try:
        profile=user.guild_profiles[guild]
    except KeyError:
        if user.avatar:
            embed.color=user.avatar&0xFFFFFF
        else:
            embed.color=user.default_avatar.color
    else:
        embed.color=user.color(guild)
        if profile.roles:
            roles=', '.join(role.mention for role in reversed(profile.roles))
        else:
            roles='none'
        text=[]
        if profile.nick is not None:
            text.append(f'Nick: {profile.nick}')
        text.append(f'Joined: {elapsed_time(profile.joined_at)} ago')
        if user.boosts is guild:
            text.append(f'Booster since: {elapsed_time(user.boosts_since)}')
        text.append(f'Roles: {roles}')
        embed.add_field('In guild profile','\n'.join(text))
    
    embed.add_thumbnail(user.avatar_url_as(size=128))

    await client.message_create(message.channel,embed=embed)

@infos.add('guild')
async def guild_info(client,message,content):
    guild=message.guild
    if guild is None:
        return

    #most usual first
    s_grey  = Status.offline
    s_green = Status.online
    s_yellow= Status.idle
    s_red   = Status.dnd
    
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
        features=', '.join(feature.name for feature in guild.features)
    else:
        features='none'

    embed=Embed(guild.name,color=guild.icon&0xFFFFFF if guild.icon else (guild.id>>22)&0xFFFFFF)
    embed.add_field('Guild information',
        f'Created: {elapsed_time(guild.created_at)} ago\n'
        f'Voice region: {guild.region}\n'
        f'Features: {features}\n')
    embed.add_field('Counts',
        f'Users: {guild.user_count}\n'
        f'Roles: {len(guild.roles)}\n'
        f'Text channels: {channel_text}\n'
        f'Voice channels: {channel_voice}\n'
        f'Category channels: {channel_category}\n')
    embed.add_field('Users',
        f'{BUILTIN_EMOJIS["green_heart"]:e} {v_green}\n'
        f'{BUILTIN_EMOJIS["yellow_heart"]:e} {v_yellow}\n'
        f'{BUILTIN_EMOJIS["heart"]:e} {v_red}\n'
        f'{BUILTIN_EMOJIS["black_heart"]:e} {v_grey}\n')

    boosters=guild.boosters
    if boosters:
        emoji=BUILTIN_EMOJIS['gift_heart']
        count=len(boosters)
        to_render=count if count<21 else 21
        
        embed.add_field('Most awesome people of the guild',
                        f'{to_render} {emoji:e} out of {count} {emoji:e}')

        for user in boosters[:21]:
            embed.add_field(user.full_name,
                f'since: {elapsed_time(user.boosts_since)}',
                inline=True)
    
    embed.add_thumbnail(guild.icon_url_as(size=128))

    await client.message_create(message.channel,embed=embed)

@infos
@content_parser('guild',
                'condition, default="guild.permissions_for(message.author).can_manage_channel"',
                'channel, flags=mni, default=None',
                on_failure=no_permission)
async def invites(client,message,guild,channel):
    try:
        if channel is None:
            invites = await client.invite_get_guild(guild)
        else:
            invites = await client.invite_get_channel(channel)
    except DiscordException:
        return
    
    pages=[{'content':chunk} for chunk in pchunkify(invites,write_parents=False,show_code=False)]
    await Pagination(client,message.channel,pages,120.)

def generate_love_level():
    value = {
        'titles' : (
            f'{BUILTIN_EMOJIS["blue_heart"]:e} There\'s no real connection between you two {BUILTIN_EMOJIS["blue_heart"]:e}',
                ),
        'text' : (
            'The chance of this relationship working out is really low. You '
            'can get it to work, but with high costs and no guarantee of '
            'working out. Do not sit back, spend as much time together as '
            'possible, talk a lot with each other to increase the chances of '
            'this relationship\'s survival.'
                ),
            }

    for x in range(0,2):
        yield value

    value = { 
        'titles' : (
            f'{BUILTIN_EMOJIS["blue_heart"]:e} A small acquaintance {BUILTIN_EMOJIS["blue_heart"]:e}',
                ),
        'text' : (
            'There might be a chance of this relationship working out somewhat '
            'well, but it is not very high. With a lot of time and effort '
            'you\'ll get it to work eventually, however don\'t count on it. It '
            'might fall apart quicker than you\'d expect.'
                ),
            }
    
    for x in range(2,6):
        yield value

    value = { 
        'titles' : (
            f'{BUILTIN_EMOJIS["purple_heart"]:e} You two seem like casual friends {BUILTIN_EMOJIS["purple_heart"]:e}',
                ),
        'text' : (
            'The chance of this relationship working is not very high. You both '
            'need to put time and effort into this relationship, if you want it '
            'to work out well for both of you. Talk with each other about '
            'everything and don\'t lock yourself up. Spend time together. This '
            'will improve the chances of this relationship\'s survival by a lot.'
                ),
            }

    for x in range(6,21):
        yield value

    value = { 
        'titles' : (
            f'{BUILTIN_EMOJIS["heartpulse"]:e} You seem like you are good friends {BUILTIN_EMOJIS["heartpulse"]:e}',
                ),
        'text' : (
            'The chance of this relationship working is not very high, but its '
            'not that low either. If you both want this relationship to work, '
            'and put time and effort into it, meaning spending time together, '
            'talking to each other etc., than nothing shall stand in your way.'
                ),
            }

    for x in range(21,31):
        yield value


    value = { 
        'titles':(
            f'{BUILTIN_EMOJIS["cupid"]:e} You two are really close aren\'t you? {BUILTIN_EMOJIS["cupid"]:e}',
                ),
        'text' : (
            'Your relationship has a reasonable amount of working out. But do '
            'not overestimate yourself there. Your relationship will suffer '
            'good and bad times. Make sure to not let the bad times destroy '
            'your relationship, so do not hesitate to talk to each other, '
            'figure problems out together etc.'
                ),
            }

    for x in range(31,46):
        yield value
    
    value = { 
        'titles' : (
            f'{BUILTIN_EMOJIS["heart"]:e} So when will you two go on a date? {BUILTIN_EMOJIS["heart"]:e}',
                ),
        'text' : (
            'Your relationship will most likely work out. It won\'t be perfect '
            'and you two need to spend a lot of time together, but if you keep '
            'on having contact, the good times in your relationship will '
            'outweigh the bad ones.'
                ),
            }

    for x in range(46,61):
        yield value

    value = { 
        'titles' : (
            f'{BUILTIN_EMOJIS["two_hearts"]:e} Aww look you two fit so well together {BUILTIN_EMOJIS["two_hearts"]:e}',
                ),
        'text' : (
            'Your relationship will most likely work out well. Don\'t hesitate '
            'on making contact with each other though, as your relationship '
            'might suffer from a lack of time spent together. Talking with '
            'each other and spending time together is key.'
                ),
            }

    for x in range(61,86):
        yield value

    value = { 
        'titles' : (
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} Love is in the air {BUILTIN_EMOJIS["sparkling_heart"]:e}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} Planned your future yet? {BUILTIN_EMOJIS["sparkling_heart"]:e}',
                ),
        'text' : (
            'Your relationship will most likely work out perfect. This '
            'doesn\'t mean thought that you don\'t need to put effort into it. '
            'Talk to each other, spend time together, and you two won\'t have '
            'a hard time.'
                ),
            }

    for x in range(86,96):
        yield value

    value = { 
        'titles' : (
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} When will you two marry? {BUILTIN_EMOJIS["sparkling_heart"]:e}',
            f'{BUILTIN_EMOJIS["sparkling_heart"]:e} Now kiss already {BUILTIN_EMOJIS["sparkling_heart"]:e}',
                ),
        'text' : (
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
@content_parser('user, flags="mna"',
                'condition, flags=r, default="message.author is user_0"',
                on_failure=show_help('love'))
async def love(client,message,target):
    source=message.author

    percent=((source.id&0x1111111111111111111111)+(target.id&0x1111111111111111111111))%101
    element=LOVE_VALUES[percent]
    
    embed=Embed(
        choice(element['titles']),
        f'{source:f} {BUILTIN_EMOJIS["heart"]:e} {target:f} scored {percent}%!',
        0xad1457,
            )
    embed.add_field('My advice:',element['text'])

    await client.message_create(message.channel,embed=embed)

class once:
    __slots__=['content','embed','ready']
    def __init__(self,content='',embed=None):
        self.ready=False
        self.content=content
        self.embed=embed
    async def __call__(self,client,message,content):
        if self.ready:
            await client.message_create(message.channel,self.content,self.embed)

ABOUT=once()
infos(ABOUT,'about')
def update_about(client):
    implement=sys.implementation
    text=''.join([ \
        f'Me, {client:f}, I am general purpose/test client.',
        '\n',
        'My code base is',
        ' [open source](https://github.com/HuyaneMatsu/Koishi). ',
        'One of the main goal of my existence is to test the best *cough*',
        ' [discord API wrapper](https://github.com/HuyaneMatsu/hata). ',
        '\n\n',
        f'My Masutaa is {client.owner:f} (send neko pictures pls).\n\n',
        '**Client info**\n',
        f'Python version: {implement.version[0]}.{implement.version[1]}',
        f'{"" if implement.version[3]=="final" else " "+implement.version[3]}\n',
        f'Interpreter: {implement.name}\n',
        f'Clients: {len(CLIENTS)}\n',
        f'Users: {len(USERS)}\n',
        f'Guilds: {len(GUILDS)}\n',
        f'Channels: {len(CHANNELS)}\n',
        'Power level: over 9000!\n',
            ])
    embed=Embed('About',text,0x5dc66f)
    embed.add_thumbnail(client.application.icon_url_as(size=128))
    ABOUT.embed=embed
    ABOUT.ready=True


@infos
@content_parser('guild',
                'condition, default="guild.permissions_for(message.author).can_view_audit_log"',
                'ensure',
                'condition, default="not part"',
                'user, flags=nmi, default=part',
                'ensure',
                'condition, default="not part"',
                'str',
                on_failure=no_permission)
async def logs(client,message,guild,*args):
    user=None
    event=None

    while True:
        if not args:
            break
        if type(args[0]) is str:
            event_iter=(event_as_str,user)
        else:
            user,*args=args
        if not args:
            break
        for event_name in args:
            try:
                event=Audit_log_event.values[int(event_name)]
                break
            except (KeyError,ValueError):
                pass
            try:
                event=getattr(Audit_log_event,event_name.upper())
                break
            except AttributeError:
                continue
            break
        break

    with client.keep_typing(message.channel):
        iterator = client.audit_log_iterator(guild,user,event)
        await iterator.load_all()
        logs = iterator.transform()
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(logs)])


@infos
@content_parser('condition, default="guild.permissions_for(message.author).can_administrator"',
                'int',
                'channel, flags=mnig, default="message.channel"',
                on_failure=no_permission)
async def message(client,message,message_id,channel):
    try:
        target_message = await client.message_get(channel,message_id)
    except DiscordException:
        await client.message_create(message.channel,'Acces denied or not existing message')
        return
    await Pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(target_message)])

@infos
@content_parser('condition, default="guild.permissions_for(message.author).can_administrator"',
                'int',
                'channel, flags=mnig, default="message.channel"',
                on_failure=no_permission)
async def message_pure(client,message,message_id,channel):
    try:
        data = await client.http.message_get(channel.id,message_id)
    except DiscordException:
        await client.message_create(message.channel,'Access denied or not existing message')
        return
    
    await Pagination(client,message.channel,[{'content':chunk} for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())])


class role_details(metaclass=asyncinit):
    __slots__=['cache','guild','roles']
    def __init__(self,client,channel):
        self.roles=list(reversed(channel.guild.roles))
        self.cache=[None for _ in range(self.roles.__len__()+1)]
        self.createpage0(channel.guild)
        #we return awaitable, so it is OK
        return embedination_rr(client,channel,self)
        
    def __len__(self):
        return self.cache.__len__()
    
    def createpage0(self,guild):
        embed=Embed(f'Roles of **{guild.name}**:',
            '\n'.join([role.mention for role in self.roles]),
            color=guild.icon&0xFFFFFF if guild.icon else (guild.id>>22)&0xFFFFFF)
        embed.add_footer(f'Page 1 /  {len(self.cache)}')
        self.cache[0]=embed
    
    def __getitem__(self,index):
        page=self.cache[index]
        if page is None:
            return self.create_page(index)
        return page

    def create_page(self,index):
        role=self.roles[index-1]
        embed=Embed(role.name,
            '\n'.join([
                f'id : {role.id!r}',
                f'color : {role.color.as_html}',
                f'permission number : {role.permissions}',
                f'managed : {role.managed}',
                f'separated : {role.separated}',
                f'mentionable : {role.mentionable}',
                '\nPermissions:\n```diff',
                *(f'{"+" if value else "-"}{key}' for key,value in role.permissions.items()),
                '```',
                    ]),
            color=role.color)
        embed.add_footer(f'Page {index+1} /  {len(self.cache)}')

        self.cache[index]=embed
        return embed

class embedination_rr(metaclass=asyncinit):
    LEFT2   = BUILTIN_EMOJIS['rewind']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['fast_forward']
    RESET   = BUILTIN_EMOJIS['arrows_counterclockwise']
    CROSS   = BUILTIN_EMOJIS['x']
    emojis  = [LEFT2,LEFT,RIGHT,RIGHT2,RESET,CROSS]
    
    __slots__=['cancel', 'channel', 'page', 'pages', 'task_flag']
    async def __init__(self,client,channel,pages):
        self.pages=pages
        self.page=0
        self.channel=channel
        self.cancel=type(self)._cancel
        self.task_flag=0
        
        message = await client.message_create(self.channel,embed=self.pages[0])
        message.weakrefer()
        
        if len(self.pages)>1:
            for emoji in self.emojis:
                await client.reaction_add(message,emoji)
        else:
            await client.reaction_add(message,self.CROSS)

        waitfor_wrapper(client,self,150.,client.events.reaction_add,message)
        
    async def __call__(self,wrapper,emoji,user):
        if user.is_bot:
            return
        
        client=wrapper.client
        message=wrapper.target

        if self.task_flag:
            if self.task_flag==1:
                if emoji is self.CROSS:
                    self.task_flag=2
                elif emoji in self.emojis:
                    Task(self.reaction_remove(client,message,emoji,user),client.loop)
            return
        
        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
            if emoji is self.RIGHT:
                page=self.page+1
                break
            if emoji is self.RESET:
                page=0
                break
            if emoji is self.CROSS:
                self.task_flag=3
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
                return wrapper.cancel()
            if emoji is self.LEFT2:
                page=self.page-10
                break
            if emoji is self.RIGHT2:
                page=self.page+10
                break

            return

        Task(self.reaction_remove(client,message,emoji,user),client.loop)

        if page<0:
            page=0
        elif page>=len(self.pages):
            page=len(self.pages)-1
        
        if self.page==page:
            return

        self.page=page
        self.task_flag=1
        try:
            await client.message_edit(message,embed=self.pages[page])
        except DiscordException:
            self.task_flag=3
            return wrapper.cancel()
        else:
            if self.task_flag==2:
                self.task_flag=3
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
                return wrapper.cancel()
            else:
                self.task_flag=0

        if wrapper.timeout<150.:
            wrapper.timeout+=10.

    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass
        
    async def _cancel(self,wrapper,exception):
        self.task_flag=3
        if exception is None:
            #we delete the message, so no need to remove reactions
            return
        if isinstance(exception,TimeoutError):
            if self.channel.guild is not None:
                try:
                    await wrapper.client.reaction_clear(wrapper.target)
                except DiscordException:
                    pass
            return

@infos
async def roles(client,message,content):
    if message.guild is None:
        return
    await role_details(client,message.channel)
