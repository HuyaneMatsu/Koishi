# -*- coding: utf-8 -*-
from random import choice
import sys
import json

from hata.parsers import eventlist
from hata.channel import message_at_index,Channel_text,Channel_category,CHANNELS
from hata.prettyprint import pchunkify
from hata.others import time_left,statuses,audit_log_events,cchunkify
from hata.exceptions import Forbidden,HTTPException
from hata.events import pagination
from hata.events_compiler import content_parser
from hata.embed import Embed,Embed_thumbnail,Embed_field,rendered_embed
from hata.emoji import BUILTIN_EMOJIS
from hata.color import Color
from hata.user import USERS
from hata.guild import GUILDS
from hata.client_core import CLIENTS

from help_handler import HELP

async def no_permission(client,message,args):
    if args:
        await client.message_create(message.channel,'You do not have permission to use this command!')

class show_help:
    __slots__=['embed']
    __async_call__=True
    def __init__(self,name):
        self.embed=HELP[name]
    def __call__(self,client,message,args):
        return client.message_create(message.channel,embed=self.embed)

infos=eventlist()

@infos.add('user')
@content_parser('user, flags="mna", default="message.author"')
async def user_info(client,message,user):
    guild=message.guild
    
    text=[f'**User Information**\nCreated: {time_left(user)} ago\nProfile: {user:m}\nID: {user.id}']

    try:
        profile=user.guild_profiles[guild]
    except KeyError:
        if user.avatar:
            color=user.avatar&0xFFFFFF
        else:
            color=user.default_avatar.color
    else:
        color=user.color(guild)
        if profile.roles:
            roles=', '.join(role.mention for role in reversed(profile.roles))
        else:
            roles='none'
        text.append('\n**In guild profile**')
        if profile.nick is not None:
            text.append(f'Nick: {profile.nick}')
        text.append(f'Joined: {time_left(profile)} ago\nRoles: {roles}')
        
    embed=Embed(f'{user:f}','\n'.join(text),color)
    embed.thumbnail=Embed_thumbnail(user.avatar_url_as(size=128))

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
@content_parser('guild',
                'condition, default="not guild.permissions_for(message.author).can_administrator"',
                'channel, flags=mni, default=None',
                on_failure=no_permission)
async def invites(client,message,guild,channel):
    try:
        if channel is None:
            invites = await client.invite_get_guild(guild)
        else:
            invites = await client.invite_get_channel(channel)
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
@content_parser('user, flags="mna"',
                on_failure=show_help('love'))
async def love(client,message,target):
    source=message.author

    percent=((source.id&0x1111111111111111111111)+(target.id&0x1111111111111111111111))%101
    element=LOVE_VALUES[percent]
    
    embed=Embed( \
        choice(element['titles']),
        f'{source:f} {BUILTIN_EMOJIS["heart"]} {target:f} scored {percent}%!',
        Color.d_magenta,
            )
    embed.fields.append(Embed_field('My advice:',element['text']))

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
    embed.thumbnail=Embed_thumbnail(client.application.icon_url_as(size=128))
    ABOUT.embed=rendered_embed(embed)
    ABOUT.ready=True


@infos
@content_parser('guild',
                'condition, default="not guild.permissions_for(message.author).can_view_audit_log"',
                'ensure',
                'condition, flags=r, default="not part"',
                'user, flags=nmi, default=part',
                'ensure',
                'condition, flags=r, default="not part"',
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
                event=audit_log_events.values[int(event_name)]
                break
            except (KeyError,ValueError):
                pass
            try:
                event=getattr(audit_log_events,event_name.upper())
                break
            except AttributeError:
                continue
            break
        break

    with client.keep_typing(message.channel):
        iterator = client.audit_log_iterator(guild,user,event)
        await iterator.load_all()
        logs = iterator.transform()
    
    pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(logs)])


@infos
@content_parser('condition, default="not guild.permissions_for(message.author).can_administrator"',
                'int',
                'channel, flags=mnig, default="message.channel"',
                on_failure=no_permission)
async def message(client,message,message_id,channel):
    try:
        target_message = await client.message_get(channel,message_id)
    except (Forbidden,HTTPException):
        await client.message_create(message.channel,'Acces denied or not existing message')
        return
    pagination(client,message.channel,[{'content':chunk} for chunk in pchunkify(target_message)])

@infos
@content_parser('condition, default="not guild.permissions_for(message.author).can_administrator"',
                'int',
                'channel, flags=mnig, default="message.channel"',
                on_failure=no_permission)
async def message_pure(client,message,message_id,channel):
    try:
        data = await client.http.message_get(channel.id,message_id)
    except (Forbidden,HTTPException):
        await client.message_create(message.channel,'Access denied or not existing message')
        return
    
    pagination(client,message.channel,[{'content':chunk} for chunk in cchunkify(json.dumps(data,indent=4,sort_keys=True).splitlines())])
