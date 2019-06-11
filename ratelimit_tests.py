import os, re, time
from collections import deque
from time import time as time_now
from hata.dereaddons_local import multidict_titled
from hata.futures import Future,sleep,elsewhere_await_coro
from hata.parsers import eventlist
from hata.client_core import CLIENTS
from hata import py_hdrs as hdrs
METH_PATCH  = hdrs.METH_PATCH
METH_GET    = hdrs.METH_GET
METH_DELETE = hdrs.METH_DELETE
METH_POST   = hdrs.METH_POST
METH_PUT    = hdrs.METH_PUT
from hata.py_reqrep import Request_CM
from hata.exceptions import DiscordException
from hata.others import to_json,from_json,quote
from hata.emoji import BUILTIN_EMOJIS
from hata.message import Message
from hata.others import (ext_from_base64,bytes_to_base64,Voice_region,
    Verification_level,Message_notification_level,Content_filter_level,
    parse_oauth2_redirect_url)
from hata.user import Partial_user,User
from hata.role import Role
from hata.client import Client
from hata.oauth2 import completed_user
from hata.channel import cr_pg_channel_object,Channel_category,Channel_text
from hata.guild import Partial_guild
from hata.http import VALID_ICON_FORMATS
from hata.integration import Integration
from email._parseaddr import _parsedate_tz
from datetime import datetime,timedelta,timezone

user1_id=189702078958927872
user2_id=184405311681986560
guild1_id=558318432253378560
guild2_id=388267636661682178

'''
UNLIMITED  :
    reaction_users
    message_logs
    message_get
    download_attachment
    invite_get_channel
    permission_ow_create
    permission_ow_delete
    channel_edit
    channel_delete
    oauth2_token
    webhook_create
    webhook_get_channel
    guild_create
    guild_get
    guild_delete
    guild_edit
    audit_logs
    guild_bans
    guild_ban_add
    guild_ban_delete
    guild_ban_get
    channel_move
    channel_create
    guild_embed_get
    guild_embed_edit
    guild_emojis
    emoji_get
    integration_get_all
    invite_get_guild
    guild_prune
    guild_prune_estimate
    role_create
    role_move
    role_edit
    role_delete
    webhook_get_guild
    invite_delete
    client_application_info
    user_info
    client_user
    channel_private_get_all
    channel_private_create
    guild_delete
    webhook_get
    webhook_edit
    webhook_delete
    webhook_get_token
    webhook_edit_token
    webhook_delete_token
    guild_regions
    guild_channels
    guild_roles
    guild_widget_get
    
group       : reaction
limit       : 1
reset       : 0.25s
limited by  : channel
members     :
    reaction_add
    reaction_delete
    reaction_delete_own
    reaction_clear

group       : message_create
limit       : 5
reset       : 4s
limited by  : channel
members     :
    message_create
    
    
group       : message_delete_multiple
limit       : 1
reset       : 3s
limited by  : channel
members     :
    message_delete_multiple

group       : message_edit
limit       : 5
reset       : 4s
limited by  : channel
members     :
    message_edit

group       : pinning
limit       : 5
reset       : 4s
limited by  : channel
members     :
    message_pin
    message_unpin

group       : pinneds
limit       : 1
reset       : 5s
limited by  : global
members     :
    message_pinneds


group       : typing
limit       : 5
reset:      : 5s
limited by  : channel
members     :
    typing

group       : invite_create
limit       : 5
reset       : 15s
limited by  : global
members     :
    invite_create

group       : client_gateway_bot
limit       : 2
reset       : 5s
limited by  : global
members     :
    client_gateway_bot

group       : emoji_create
limit       : 50
reset       : 3600s
limited by  : guild
members     :
    emoji_create

group       : emoji_delete
limit       : 1
reset       : 3s
limited by  : global
members     :
    emoji_delete

group       : emoji_edit
limit       : 1
reset       : 3s
limited by  : global
members     :
    emoji_edit

group       : client_edit_nick
limit       : 1
reset       : 2s
limited by  : global
members     :
    client_edit_nick

group       : guild_user_delete
limit       : 5
reset       : 2s
limited by  : guild
members     :
    guild_user_delete

group       : user_edit
limit       : 10
reset       : 10s
limited by  : guild
members     :
    user_edit

group       : guild_user_add
limit       : 10
reset       : 10s
limited by  : guild
members     :
    guild_user_add

group       : user_role
limit       : 10
reset       : 10s
limited by  : guild
members     :
    user_role_add
    user_role_delete

group       : invite_get
limit       : 250
reset       : 6s
limited by  : global
members     :
    invite_get

group       : client_edit
limit       : 2
reset       : 3600s
limited by  : global
members     :
    client_edit

group       : user_guilds
limit       : 1
reset       : 1s
limited by  : global
members     :
    user_guilds

group       : guild_get_all
limit       : 1
reset       : 1s
limited by  : global
members     :
    guild_get_all
    
group       : user_get
limit       : 30
reset       : 30s
limited by  : global
members     :
    user_get

group       : webhook_execute
limit       : 5
reset       : 2s
limited by  : webhook
members     :
    webhook_execute

group       : guild_users
limit       : 10
reset       : 10s
limited by  : webhook
members     :
    guild_users
    
group       : guild_user_get
limit       : 5
reset       : 2s
limited by  : global
members:
    guild_user_get

group       : message_delete 
case 1      : newer than 2 week or own
    limit   : 3
    reset   : 2s
case 2      : older than 2 week and not own
    limit   : 30
    reset   : 120s
members     :
    message_delete
'''

def parsedate_to_datetime(data):
    *dtuple, tz = _parsedate_tz(data)
    if tz is None:
        return datetime(*dtuple[:6])
    return datetime(*dtuple[:6],tzinfo=timezone(timedelta(seconds=tz)))

def parse_header_ratelimit(headers):
    return ( \
        datetime.fromtimestamp(int(headers['X-Ratelimit-Reset']),timezone.utc)
        -parsedate_to_datetime(headers['Date']) 
            ).total_seconds()

def other_client(client):
    for client2 in CLIENTS:
        if client2 is client:
            continue
        return client2

async def notsocoro():
    pass

ratelimit_commands=eventlist()

async def bypass_request(client,method,url,data=None,params=None,reason=None,header=None,decode=True):
    self=client.http
    if header is None:
        header=self.header.copy()

    
    if hdrs.CONTENT_TYPE not in header and data and isinstance(data,(dict,list)):
        header[hdrs.CONTENT_TYPE]='application/json'
        #converting data to json
        data=to_json(data)

    if reason:
        header['X-Audit-Log-Reason']=quote(reason)

    try_again=5
    while try_again:
        try_again-=1
        try:
            async with Request_CM(self._request(method,url,header,data,params)) as response:
                if decode:
                    response_data = await response.text(encoding='utf-8')
                else:
                    response_data=''
        except OSError as err:
            #os cant handle more, need to wait for the blocking job to be done
            await sleep(0.1,self.loop)
            #invalid adress causes OSError too, but we will let it run 5 times, then raise a ConnectionError
            continue
        
        headers=response.headers
        status=response.status
        
        if headers['content-type']=='application/json':
            response_data=from_json(response_data)
        
        result=['\nrate limits:',f'{url} {method}']
        value=headers.get('X-RateLimit-Global',None)
        if value is not None:
            result.append(f'global : {value}')
        value=headers.get('X-RateLimit-Limit',None)
        if value is not None:
            result.append(f'limit : {value}')
        value=headers.get('X-RateLimit-Remaining',None)
        if value is not None:
            result.append(f'remaining : {value}')
        value=headers.get('X-RateLimit-Reset',None)
        if value is not None:
            delay=parse_header_ratelimit(headers)
            result.append(f'reset : {value}, after {delay} seconds')
        print('\n'.join(result))

        
        if 199<status<305:
            if headers.get('X-Ratelimit-Remaining','1')=='0':
                print(f'reached 0\n try again after {delay}')
            return response_data
        
        if status==429:
            retry_after=response_data['retry_after']/1000.
            print(f'RATE LIMITED\nretry after : {retry_after}')
            await sleep(retry_after,self.loop)
            continue
        
        elif status==500 or status==502:
            await sleep(10./try_again+1.,self.loop)
            continue
        
        raise DiscordException(response,response_data)

    try:
        raise DiscordException(response,response_data)
    except UnboundLocalError:
        raise ConnectionError('Invalid adress')

def reaction_add(client,message,emoji):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return bypass_request(client,METH_PUT, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')
        
def reaction_delete(client,message,emoji,user):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    user_id=user.id
    return bypass_request(client,METH_DELETE, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}')

def reaction_delete_own(client,message,emoji):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return bypass_request(client,METH_DELETE, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me')

def reaction_clear(client,message):
    channel_id=message.channel.id
    message_id=message.id
    return bypass_request(client,METH_DELETE, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions')

def reaction_users(client,message,emoji):
    if message.reactions is None:
        return []
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return bypass_request(client,METH_GET, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}',
        params={'limit':100})

async def message_create(client,channel,content=None,embed=None,tts=False,nonce=0):
    if not (content or embed):
        return #saved 1 request, is this really necesarry?
    data={}
    if content is not None:
        data['content']=content
    if embed is not None:
        data['embed']=embed.to_data()
    if tts:
        data['tts']=True
    if nonce:
        data['nonce']=nonce
    channel_id=channel.id
    data = await bypass_request(client,METH_POST, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages',
        data)
    return Message.new(data,channel)

def message_delete(client,message):
    channel_id=message.channel.id
    message_id=message.id
    return bypass_request(client,METH_DELETE, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}')

def message_delete_multiple(client,messages):
    if len(messages)==0:
        return notsocoro()
    if len(messages)==1:
        return message_delete(client,messages[0])
    data={'messages':[message.id for message in messages]}
    channel_id=messages[0].channel.id
    return bypass_request(client,METH_POST, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/bulk_delete',
        data)

def message_edit(client,message,content=None,embed=None):
    data={}
    if content is not None:
        data['content']=content
    if embed is not None:
        data['embed']=embed.to_data()
    channel_id=message.channel.id
    message_id=message.id
    return bypass_request(client,METH_PATCH, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}',
        data)

def message_pin(client,message):
    channel_id=message.channel.id
    message_id=message.id
    return bypass_request(client,METH_PUT, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/pins/{message_id}')

def message_unpin(client,message):
    channel_id=message.channel.id
    message_id=message.id
    return bypass_request(client,METH_DELETE, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/pins/{message_id}')

def message_pinneds(client,channel):
    channel_id=channel.id
    return bypass_request(client,METH_GET, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/pins')

def message_logs(client,channel):
    channel_id=channel.id
    return bypass_request(client,METH_GET, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages',
        params={'limit':1})

def message_get(client,channel,message_id):
    channel_id=channel.id
    return bypass_request(client,METH_GET, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}')

def download_attachment(client,attachment):
    if attachment.proxy_url.startswith('https://cdn.discordapp.com/'):
        url=attachment.proxy_url
    else:
        url=attachment.url
    return bypass_request(client,hdrs.METH_GET,url,header=multidict_titled(),decode=False)


def typing(client,channel):
    channel_id=channel.id
    return bypass_request(client,METH_POST, \
        f'https://discordapp.com/api/v7/channels/{channel_id}/typing')

def client_edit(client,name='',avatar=b''):
    data={}
    if name:
        if not (1<len(name)<33):
            raise ValueError(f'The lenght of the name can be between 2-32, got {len(name)}')
        data['username']=name
    
    if avatar is None:
        data['avatar']=None
    elif avatar:
        avatar_data=bytes_to_base64(avatar)
        ext=ext_from_base64(avatar_data)
    return bypass_request(client,METH_PATCH, \
        'https://discordapp.com/api/v7/users/@me',
        data)

def client_connections(client):
    return bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/connections')

def client_edit_nick(client,guild,nick):
    guild_id=guild.id
    return bypass_request(client,METH_PATCH, \
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/@me/nick',
        {'nick':nick})

def client_gateway_bot(client):
    return bypass_request(client,METH_GET, \
        'https://discordapp.com/api/v7/gateway/bot')

def client_application_info(client):
    return bypass_request(client,METH_GET, \
        'https://discordapp.com/api/v7/oauth2/applications/@me')

def client_login_static(client):
    return bypass_request(client,METH_GET, \
        'https://discordapp.com/api/v7/users/@me')

def client_logout(client):
    return bypass_request(client,METH_POST, \
        'https://discordapp.com/api/v7/auth/logout')


def permission_ow_create(client,channel,target,allow,deny):
    if type(target) is Role:
        type_='role'
    elif type(target) in (User,Client,completed_user):
        type_='member'
    else:
        raise TypeError(f'Target expected to be Role or User type, got {type(target)!r}')
    data={ \
        'target':target.id,
        'allow':allow,
        'deny':deny,
        'type':type_,
            }
    channel_id=channel.id
    overwrite_id=target.id
    return bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/channels/{channel_id}/permissions/{overwrite_id}',data)

def permission_ow_delete(client,channel,overwrite):
    channel_id=channel.id
    overwrite_id=overwrite.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}/permissions/{overwrite_id}')

def channel_edit(client,channel,name='',topic='',nsfw=None,slowmode=None,user_limit=None,bitrate=None,type_=128):
    data={}
    value=channel.type
    if name:
        if not 1<len(name)<101:
            raise ValueError(f'Invalid nam length {len(name)}, should be 2-100')
        data['name']=name
    
    if value in (0,5):
        if topic:
            if len(topic)>1024:
                raise ValueError(f'Invalid topic length {len(topic)}, should be 0-1024')
            data['topic']=topic
        
        if type_<128:
            if type_ not in (0,5):
                raise ValueError('You can switch chanel type only between only Text channel (0) and Guild news channel (5)')
            if type_!=value:
                data['type']=type_
        
    if value==0:
        if nsfw is not None:
            data['nsfw']=nsfw
            
        if slowmode is not None:
            if slowmode<0 or slowmode>120:
                raise ValueError(f'Invalid slowmode {slowmode}, should be 0-120')
            data['rate_limit_per_user']=slowmode

    elif value==2:
        if bitrate<8000 or bitrate>(96000,128000)['VIP' in chanel.guild.feautres]:
            raise ValueError(f'Invalid bitrate {bitrate!r}, should be 8000-96000 (128000 for vip)')
        data['bitrate']=bitrate
        
        if user_limit:
            if user_limit<1 or user_limit>99:
                raise ValueError(f'Invalid user_limit {user_limit!r}, should be 0 for unlimited or 1-99')
            data['user_limit']=user_limit

    channel_id=channel.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/channels/{channel_id}',data)

def channel_delete(client,channel):
    channel_id=channel.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}')

def oauth2_token(client):
    data={ \
        'client_id'     : client.id,
        'client_secret' : client.secret,
        'grant_type'    : 'client_credentials',
        'scope'         : 'connections'
            }
    
    headers=multidict_titled()
    dict.__setitem__(headers,hdrs.CONTENT_TYPE,['application/x-www-form-urlencoded'])
                
    return bypass_request(client,METH_POST,
        'https://discordapp.com/api/oauth2/token',data,header=headers)

def invite_create(client,channel):
    data={ \
        'max_age'   : 60,
        'max_uses'  : 1,
        'temporary' : False,
        'unique'    : True,
            }
    channel_id=channel.id
    return bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/invites',data)

def invite_get_channel(client,channel):
    channel_id=channel.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/invites')

def webhook_create(client,channel,name,avatar=b''):
    data={'name':name}
    if avatar:            
        data['avatar']=bytes_to_base64(avatar)
            
    channel_id=channel.id
    return bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/webhooks',data)

def webhook_get_channel(client,channel):
    channel_id=channel.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/webhooks')

async def guild_create(client,name,icon=None,
        region=Voice_region.eu_central,
        verification_level=Verification_level.medium,
        message_notification_level=Message_notification_level.only_mentions,
        content_filter_level=Content_filter_level.disabled,
        roles=[],channels=[]):
        
    if client.is_bot and len(client.guilds)>9:
        raise ValueError('Bots cannot create a new server if they have more than 10.')

    if not (1<len(name)<101):
        raise ValueError(f'Guild\'s name\'s lenght can be between 2-100, got {len(name)}')
    
    data = { \
        'name'                          : name,
        'icon'                          : None if icon is None else bytes_to_base64(avatar),
        'region'                        : region.id,
        'verification_level'            : verification_level.value,
        'default_message_notifications' : message_notification_level.value,
        'explicit_content_filter'       : content_filter_level.value,
        'roles'                         : roles,
        'channels'                      : channels,
            }

    data = await bypass_request(client,METH_POST,
        'https://discordapp.com/api/v7/guilds',data)
    #we can create only partial, because the guild data is not completed usually
    return Partial_guild(data)

def guild_get(client,guild_id):
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}')

def guild_delete(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}')

def guild_edit(client,guild,name,icon=b''): #keep it short
    data={'name':name}
    if icon is None:
        data['icon']=None
    elif icon:
        icon_data=bytes_to_base64(icon)
        ext=ext_from_base64(icon_data)
        if ext not in VALID_ICON_FORMATS:
            raise ValueError(f'Invalid icon type: {ext}')
        data['icon']=icon_data
    guild_id=guild.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}',data)

def audit_logs(client,guild,):
    data={'limit':100}
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/audit-logs',params=data)

def guild_bans(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans')

def guild_ban_add(client,guild,user_id):
    data={'delete-message-days':0}
    guild_id=guild.id
    return bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans/{user_id}',params=data)

def guild_ban_delete(client,guild,user_id):
    guild_id=guild.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans/{user_id}')

def guild_ban_get(client,guild,user_id):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans/{user_id}')

async def channel_move(client,*args,**kwargs):
    def http_channel_move_redirect(self,guild_id,data,reason):
        return bypass_request(client,METH_PATCH,
            f'https://discordapp.com/api/v7/guilds/{guild_id}/channels',data)
    original=type(client.http).channel_move
    type(client.http).channel_move=http_channel_move_redirect
    await client.channel_move(*args,**kwargs)
    type(client.http).channel_move=original

def channel_create(client,guild,category=None):
    data=cr_pg_channel_object(type_=0,name='tesuto-channel9')
    data['parent_id']=category.id if type(category) is Channel_category else None
    guild_id=guild.id
    return bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/channels',data)

def guild_embed_get(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/embed')

def guild_embed_edit(client,guild,value):
    data={'enabled':value}
    guild_id=guild.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/embed',data)

def guild_embed_image(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/embed.png',
        params={'style':'shield'},decode=False,header={})

def guild_emojis(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis')

def emoji_create(client,guild,name,image):
    image=bytes_to_base64(image)
    name=''.join(re.findall('([0-9A-Za-z_]+)',name))
    if not (1<len(name)<33):
        raise ValueError(f'The lenght of the name can be between 2-32, got {len(name)}')
    
    data={ \
        'name'      : name,
        'image'     : image,
        'role_ids'  : []
            }
        
    guild_id=guild.id
    return bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis',data)

def emoji_get(client,guild,emoji_id):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis/{emoji_id}')

def emoji_delete(client,guild,emoji):
    guild_id=guild.id
    emoji_id=emoji.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis/{emoji_id}')

def emoji_edit(client,guild,emoji,name): #keep it short
    data={'name':name}
    guild_id=guild.id
    emoji_id=emoji.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis/{emoji_id}',data)

def integration_get_all(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/integrations')

def invite_get_guild(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/invites')

def guild_user_delete(client,guild,user_id):
    guild_id=guild.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}')

def user_edit(client,guild,user,nick,mute=False):
    guild_id=guild.id
    user_id=user.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}',
        data={'nick':nick,'mute':mute})

def guild_user_add(client,guild,user):
    guild_id=guild.id
    user_id=user.id
    return bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}',
        data={'access_token':user.access.access_token})

def user_role_add(client,user,role):
    guild_id=role.guild.id
    user_id=user.id
    role_id=role.id
    return bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}/roles/{role_id}')

def user_role_delete(client,user,role):
    guild_id=role.guild.id
    user_id=user.id
    role_id=role.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}/roles/{role_id}')

def guild_prune(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/prune',
        params={'days':30})

def guild_prune_estimate(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/prune',
        params={'days':30})

def role_create(client,guild,name=None,permissions=None,color=None,
        separated=None,mentionable=None,reason=None):

    data={}
    if name is not None:
        data['name']=name
    if permissions is not None:
        data['permissions']=permissions
    if color is not None:
        data['color']=color
    if separated is not None:
        data['hoist']=separated
    if mentionable is not None:
        data['mentionable']=mentionable

    guild_id=guild.id
    return bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles',
        data=data)

def role_move(client,role,new_position):
    data=role.guild.roles.change_on_swich(role,new_position,key=lambda role,pos:{'id':role.id,'position':pos})
    guild_id=role.guild.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles',
        data=data)

def role_edit(client,role,color=None,separated=None,mentionable=None,
        name=None,permissions=None,):
    
    if color is None:
        color=role.color
    if separated is None:
        separated=role.separated
    if mentionable is None:
        mentionable=role.mentionable
    if name is None:
        name=role.name
    if permissions is None:
        permission=role.permissions

    data={ \
        'name'        : name,
        'permissions' : permissions,
        'color'       : color,
        'hoist'       : separated,
        'mentionable' : mentionable,
            }
    guild_id=role.guild.id
    role_id=role.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles/{role_id}',
        data=data)

def role_delete(client,role):
    guild_id=role.guild.id
    role_id=role.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles/{role_id}')


def webhook_get_guild(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/webhooks')

def guild_widget_image(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/widget.png',
        params={'style':'shield'},decode=False,header={})

def invite_get(client,invite):
    invite_code=invite.code
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/invites/{invite_code}')

def invite_delete(client,invite):
    invite_code=invite.code
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/invites/{invite_code}')

def user_info(client,access):
    header=multidict_titled()
    header[hdrs.AUTHORIZATION]=f'Bearer {access.access_token}'
    return bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me',
        header=header)

def client_user(client):
    return bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me')

def channel_private_get_all(client):
    return bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/channels')

def channel_private_create(client,user):
    return bypass_request(client,METH_POST,
        'https://discordapp.com/api/v7/users/@me/channels',
        data={'recipient_id':user.id},)

def user_connections(client,access):
    header=multidict_titled()
    header[hdrs.AUTHORIZATION]=f'Bearer {access.access_token}'
    return bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/connections',
        header=header)

def user_guilds(client,access):
    header=multidict_titled()
    header[hdrs.AUTHORIZATION]=f'Bearer {access.access_token}'
    return bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/guilds',
        header=header)

def guild_get_all(client):
    return bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/guilds',
        params={'after':0})

def guild_delete(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}')

def user_get(client,user):
    user_id=user.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/users/{user_id}')

def webhook_get(client,webhook):
    webhook_id=webhook.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/webhooks/{webhook_id}')

def webhook_delete(client,webhook):
    webhook_id=webhook.id
    return  bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/webhooks/{webhook_id}')

def webhook_edit(client,webhook,name): #keep it short
    webhook_id=webhook.id
    return bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/webhooks/{webhook_id}',
        data={'name':name})

def webhook_get_token(client,webhook):
    return bypass_request(client,METH_GET,
        webhook.url,header={})

def webhook_delete_token(client,webhook):
    return bypass_request(client,METH_DELETE,
        webhook.url,header={})

def webhook_edit_token(client,webhook,name): #keep it short
    return bypass_request(client,METH_PATCH,
        webhook.url,
        data={'name':name},header={})

def webhook_execute(client,webhook,content,wait=False):
    return bypass_request(client,METH_POST,
        f'{webhook.url}?wait={wait:d}',
        data={'content':content},header={})
    
def guild_users(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members')

def guild_regions(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/regions')

def guild_channels(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/channels')

def guild_roles(client,guild):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles')

def guild_user_get(client,guild,user_id):
    guild_id=guild.id
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}')

def guild_widget_get(client,guild_id):
    return bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/widget.json',
        header={})

@ratelimit_commands
async def ratelimit_test0000(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1,channel2,channel3=message.channel.category.channels[0:3]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    message3 = await client.message_create(channel3,'test')
    loop.create_task(reaction_add(client,message1,emoji1))
    loop.create_task(reaction_add(client,message2,emoji1))
    loop.create_task(reaction_add(client,message3,emoji1))
    #reaction_add is not per guild

@ratelimit_commands
async def ratelimit_test0001(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel1,'test')
    loop=client.loop
    loop.create_task(reaction_add(client,message1,emoji1))
    loop.create_task(reaction_add(client,message2,emoji1))
    loop.create_task(reaction_add(client,message3,emoji1))
    #reaction_add is per channel -> no pm tests needed

@ratelimit_commands
async def ratelimit_test0002(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1,channel2,channel3=message.channel.category.channels[0:3]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    message3 = await client.message_create(channel3,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    await client.reaction_add(message3,emoji1)
    loop.create_task(reaction_delete_own(client,message1,emoji1))
    loop.create_task(reaction_delete_own(client,message2,emoji1))
    loop.create_task(reaction_delete_own(client,message3,emoji1))
    #reaction_delete_own not limited per guild
    
@ratelimit_commands
async def ratelimit_test0003(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel1,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    await client.reaction_add(message3,emoji1)
    loop.create_task(reaction_delete_own(client,message1,emoji1))
    loop.create_task(reaction_delete_own(client,message2,emoji1))
    loop.create_task(reaction_delete_own(client,message3,emoji1))
    #reaction_delete_own limited per chanel

@ratelimit_commands
async def ratelimit_test0004(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    emoji2=BUILTIN_EMOJIS['o']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    loop.create_task(reaction_delete_own(client,message1,emoji1))
    loop.create_task(reaction_delete_own(client,message2,emoji1))
    loop.create_task(reaction_add(client,message1,emoji2))
    loop.create_task(reaction_add(client,message2,emoji2))
    #reaction_delete_own and reaction_add share the same category

@ratelimit_commands
async def ratelimit_test0005(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    client2=other_client(client)
    emoji1=BUILTIN_EMOJIS['x']
    channel1,channel2,channel3=message.channel.category.channels[0:3]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    message3 = await client.message_create(channel3,'test')
    await elsewhere_await_coro(client2.reaction_add(message1,emoji1),loop,client2.loop)
    await elsewhere_await_coro(client2.reaction_add(message2,emoji1),loop,client2.loop)
    await elsewhere_await_coro(client2.reaction_add(message3,emoji1),loop,client2.loop)
    loop.create_task(reaction_delete(client,message1,emoji1,client2))
    loop.create_task(reaction_delete(client,message2,emoji1,client2))
    loop.create_task(reaction_delete(client,message3,emoji1,client2))
    #reaction_delete is not guild limited

@ratelimit_commands
async def ratelimit_test0006(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    client2=other_client(client)
    emoji1=BUILTIN_EMOJIS['x']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel1,'test')
    await elsewhere_await_future(client2.reaction_add(message1,emoji1),loop,client2.loop)
    await elsewhere_await_future(client2.reaction_add(message2,emoji1),loop,client2.loop)
    await elsewhere_await_future(client2.reaction_add(message3,emoji1),loop,client2.loop)
    loop.create_task(reaction_delete(client,message1,emoji1,client2))
    loop.create_task(reaction_delete(client,message2,emoji1,client2))
    loop.create_task(reaction_delete(client,message3,emoji1,client2))
    #reaction_delete is channel limited

@ratelimit_commands
async def ratelimit_test0007(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    client2=other_client(client)
    emoji1=BUILTIN_EMOJIS['x']
    emoji2=BUILTIN_EMOJIS['o']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await elsewhere_await_future(client2.reaction_add(message1,emoji1),loop,client2.loop)
    await elsewhere_await_future(client2.reaction_add(message2,emoji1),loop,client2.loop)
    loop.create_task(reaction_delete(client,message1,emoji1,client2))
    loop.create_task(reaction_delete(client,message2,emoji1,client2))
    loop.create_task(reaction_add(client,message1,emoji2))
    loop.create_task(reaction_add(client,message2,emoji2))
    #reaction_delete is limited with reaction_add

@ratelimit_commands
async def ratelimit_test0008(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1,channel2,channel3=message.channel.category.channels[0:3]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    message3 = await client.message_create(channel3,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    await client.reaction_add(message3,emoji1)
    loop.create_task(reaction_clear(client,message1))
    loop.create_task(reaction_clear(client,message2))
    loop.create_task(reaction_clear(client,message3))
    #reaction_clear is not guild limited
    
@ratelimit_commands
async def ratelimit_test0009(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel1,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    await client.reaction_add(message3,emoji1)
    loop.create_task(reaction_clear(client,message1))
    loop.create_task(reaction_clear(client,message2))
    loop.create_task(reaction_clear(client,message3))
    #reaction_clear is channel limited

@ratelimit_commands
async def ratelimit_test0010(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    emoji2=BUILTIN_EMOJIS['o']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    loop.create_task(reaction_clear(client,message1))
    loop.create_task(reaction_clear(client,message2))
    loop.create_task(reaction_add(client,message1,emoji2))
    loop.create_task(reaction_add(client,message2,emoji2))
    #reaction_clear is limited with reaction_add
    
@ratelimit_commands
async def ratelimit_test0011(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1,channel2,channel3=message.channel.category.channels[0:3]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    message3 = await client.message_create(channel3,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    await client.reaction_add(message3,emoji1)
    loop.create_task(reaction_users(client,message1,emoji1))
    loop.create_task(reaction_users(client,message2,emoji1))
    loop.create_task(reaction_users(client,message3,emoji1))
    #reaction_users is not guild limited
    
    
@ratelimit_commands
async def ratelimit_test0012(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel1,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    await client.reaction_add(message3,emoji1)
    loop.create_task(reaction_users(client,message1,emoji1))
    loop.create_task(reaction_users(client,message2,emoji1))
    loop.create_task(reaction_users(client,message3,emoji1))
    #reaction_users is not channel limited
    #REACTION_USERS is NOT limited at all!
    
@ratelimit_commands
async def ratelimit_test0013(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    emoji1=BUILTIN_EMOJIS['x']
    emoji2=BUILTIN_EMOJIS['o']
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await client.reaction_add(message1,emoji1)
    await client.reaction_add(message2,emoji1)
    loop.create_task(reaction_users(client,message1,emoji1))
    loop.create_task(reaction_users(client,message2,emoji1))
    loop.create_task(reaction_add(client,message1,emoji2))
    loop.create_task(reaction_add(client,message2,emoji2))
    # - is reaction_users limited with reaction_add

@ratelimit_commands
async def ratelimit_test0014(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_create(client,channel2,'test'))
    #message_create is not guild limited

@ratelimit_commands
async def ratelimit_test0015(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_create(client,channel1,'test'))
    # - message_create is channel limited

@ratelimit_commands
async def ratelimit_test0016(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    channel2 = await client.channel_private_create(message.author)
    await sleep(5.,loop)
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_create(client,channel2,'test'))
    #message_create is not global limited

@ratelimit_commands
async def ratelimit_test0017(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1 = await client.channel_private_create(message.author)
    channel2 = await client.channel_private_create(Partial_user(user1_id))
    await sleep(5.,loop)
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_create(client,channel2,'test'))
    #message_create is not global PM limited
                     
@ratelimit_commands
async def ratelimit_test0018(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_delete(client,message1))
    loop.create_task(message_delete(client,message2))
    #message_delete is not guild limited
    #MESSAGE_DELETE is NOT limited

@ratelimit_commands
async def ratelimit_test0019(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_delete(client,message1))
    loop.create_task(message_delete(client,message2))
    # - is message_delete channel limited

@ratelimit_commands
async def ratelimit_test0020(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    channel2 = await client.channel_private_create(message.author)
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_delete(client,message1))
    loop.create_task(message_delete(client,message2))
    # - is message_delete global limited

@ratelimit_commands
async def ratelimit_test0021(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1 = await client.channel_private_create(message.author)
    channel2 = await client.channel_private_create(Partial_user(user1_id))
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_delete(client,message1))
    loop.create_task(message_delete(client,message2))
    # - is message_delete global PM limited

@ratelimit_commands
async def ratelimit_test0022(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1=await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_delete(client,message1))
    #message_create limited is not limited with message_delete

@ratelimit_commands
async def ratelimit_test0023(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel2,'test')
    message4 = await client.message_create(channel2,'test')
    await sleep(5.,loop) #wait for potential ratelimits
    loop.create_task(message_delete_multiple(client,[message1,message2]))
    loop.create_task(message_delete_multiple(client,[message3,message4]))
    #message_delete_multiple is not guild limited

    
@ratelimit_commands
async def ratelimit_test0024(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel           
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel1,'test')
    message4 = await client.message_create(channel1,'test')
    await sleep(5.,loop) #wait for potential ratelimits
    loop.create_task(message_delete_multiple(client,[message1,message2]))
    loop.create_task(message_delete_multiple(client,[message3,message4]))
    #message_delete_multiple is channel limited
                     
@ratelimit_commands
async def ratelimit_test0025(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel           
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    message3 = await client.message_create(channel1,'test')
    message4 = await client.message_create(channel1,'test')
    await sleep(5.,loop) #wait for potential ratelimits
    loop.create_task(message_delete(client,message1))
    loop.create_task(message_delete_multiple(client,[message2,message3]))
    loop.create_task(message_delete(client,message4))
    # - is message_delete_multiple limited with message_delete
    
@ratelimit_commands
async def ratelimit_test0026(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(message_edit(client,message2,'notsotest'))
    #message_edit is not guild limited

@ratelimit_commands
async def ratelimit_test0027(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(message_edit(client,message2,'notsotest'))
    #is message_edit channel limited

@ratelimit_commands
async def ratelimit_test0028(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    channel2 = await client.channel_private_create(message.author)
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(message_edit(client,message2,'notsotest'))
    #message_edit is not global limited

@ratelimit_commands
async def ratelimit_test0029(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1 = await client.channel_private_create(message.author)
    channel2 = await client.channel_private_create(Partial_user(user1_id))
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(message_edit(client,message2,'notsotest'))
    #message_edit is not global PM limited

@ratelimit_commands
async def ratelimit_test0030(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1=await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_edit(client,message1,'yessotest'))
    #message_create is not limited with message_edit

@ratelimit_commands
async def ratelimit_test0031(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(message_edit(client,message1,'yessotest'))
    #message_edit is message limited (channel too, so this is ignored)
    
@ratelimit_commands
async def ratelimit_test0032(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_pin(client,message1,))
    loop.create_task(message_pin(client,message2,))
    #message_pin is not guild limited

@ratelimit_commands
async def ratelimit_test0033(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_pin(client,message1))
    loop.create_task(message_pin(client,message2))
    #message_pin is channel limited

@ratelimit_commands
async def ratelimit_test0034(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    channel2 = await client.channel_private_create(message.author)
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_pin(client,message1))
    loop.create_task(message_pin(client,message2))
    # - is message_pin global limited

@ratelimit_commands
async def ratelimit_test0035(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1 = await client.channel_private_create(message.author)
    channel2 = await client.channel_private_create(Partial_user(user1_id))
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_pin(client,message1))
    loop.create_task(message_pin(client,message2))
    # - is message_pin global PM limited

@ratelimit_commands
async def ratelimit_test0036(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1=await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(message_pin(client,message1))
    #message_create is not limited with message_pin
    
@ratelimit_commands
async def ratelimit_test0037(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    await sleep(5.,loop)
    await message_pin(client,message1)
    await client.message_unpin(message1)
    await message_pin(client,message1)
    #message_pin message limited with message_unpin

@ratelimit_commands
async def ratelimit_test0038(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await client.message_pin(message1)
    await client.message_pin(message2)
    await sleep(5.,loop)
    loop.create_task(message_unpin(client,message1,))
    loop.create_task(message_unpin(client,message2,))
    # - is message_unpin guild limited

@ratelimit_commands
async def ratelimit_test0039(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel1,'test')
    await client.message_pin(message1)
    await client.message_pin(message2)
    await sleep(5.,loop)
    loop.create_task(message_pin(client,message1))
    loop.create_task(message_pin(client,message2))
    # - is message_unpin channel limited

@ratelimit_commands
async def ratelimit_test0040(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    channel2 = await client.channel_private_create(message.author)
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await client.message_pin(message1)
    await client.message_pin(message2)
    await sleep(5.,loop)
    loop.create_task(message_unpin(client,message1))
    loop.create_task(message_unpin(client,message2))
    # - is message_unpin global limited

@ratelimit_commands
async def ratelimit_test0041(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1 = await client.channel_private_create(message.author)
    channel2 = await client.channel_private_create(Partial_user(user1_id))
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await client.message_pin(message1)
    await client.message_pin(message2)
    await sleep(5.,loop)
    loop.create_task(message_unpin(client,message1))
    loop.create_task(message_unpin(client,message2))
    # - is message_unpin global PM limited

@ratelimit_commands
async def ratelimit_test0042(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1=await client.message_create(channel1,'test')
    message1=await client.message_create(channel2,'test')
    await client.message_pin(message2)
    await sleep(5.,loop)
    loop.create_task(message_pin(client,message1))
    loop.create_task(message_unpin(client,message2))
    # - is message_unpin limited with message_unpin
    
@ratelimit_commands
async def ratelimit_test0043(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    await client.message_pin(message1)
    await sleep(5.,loop)
    await message_unpin(client,message1)
    await client.message_pin(message1)
    await message_unpin(client,message1)
    # - is message_unpin message limited

@ratelimit_commands
async def ratelimit_test0044(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    loop.create_task(message_pinneds(client,channel1))
    loop.create_task(message_pinneds(client,channel2))
    #message_pinneds is guild limited

@ratelimit_commands
async def ratelimit_test0045(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(message_pinneds(client,channel1))
    loop.create_task(message_pinneds(client,channel1))
    # - is message_pinneds channel limited
    
@ratelimit_commands
async def ratelimit_test0046(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    channel2 = await client.channel_private_create(message.author)
    loop.create_task(message_pinneds(client,channel1))
    loop.create_task(message_pinneds(client,channel2))
    #message_pinneds is global limited

@ratelimit_commands
async def ratelimit_test0047(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1 = await client.channel_private_create(message.author)
    channel2 = await client.channel_private_create(Partial_user(user1_id))
    loop.create_task(message_pinneds(client,channel1))
    loop.create_task(message_pinneds(client,channel2))
    # - is message_pinneds global PM limited
    
@ratelimit_commands
async def ratelimit_test0048(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(message_pinneds(client,channel1))
    loop.create_task(message_create(client,channel1,'test'))
    # - is message_pinneds limited with message_create

@ratelimit_commands
async def ratelimit_test0049(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    loop.create_task(message_logs(client,channel1))
    loop.create_task(message_logs(client,channel2))
    #message_logs is not guild limited
    #MESSAGE_LOGS is NOT limited

@ratelimit_commands
async def ratelimit_test0050(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(message_logs(client,channel1))
    loop.create_task(message_logs(client,channel1))
    # - is message_logs channel limited
    
@ratelimit_commands
async def ratelimit_test0051(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(message_pinneds(client,channel1))
    loop.create_task(message_logs(client,channel1))
    # - is message_logs limited with message_pinneds


@ratelimit_commands
async def ratelimit_test0052(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    message1 = await client.message_create(channel1,'test')
    message2 = await client.message_create(channel2,'test')
    await sleep(5.,loop)
    loop.create_task(message_get(client,channel1,message1.id))
    loop.create_task(message_get(client,channel2,message2.id))
    #message_get is not guild limited
    #MESSAGE_GET is NOT limited
    
@ratelimit_commands
async def ratelimit_test0053(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_get(client,channel1,message1.id))
    loop.create_task(message_get(client,channel1,message.id))
    # - is message_get channel limited

@ratelimit_commands
async def ratelimit_test0054(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(message_get(client,channel1,message.id))
    loop.create_task(message_create(client,channel1,'test'))
    # - is message_get limited with message_create

@ratelimit_commands
async def ratelimit_test0055(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create_file(channel1, \
        open(os.path.join(os.path.abspath('.'),'images',
            '0000000A_touhou_koishi_kokoro_reversed.png'),'rb'))
    loop.create_task(download_attachment(client,message1.attachments[0]))
    #download_attachment is not limited

@ratelimit_commands
async def ratelimit_test0056(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await message.message_create_file(channel1, \
        open(os.path.join(os.path.abspath('.'),'images',
            '0000000A_touhou_koishi_kokoro_reversed.png'),'rb'))
    await sleep(5.,loop)
    loop.create_task(download_attachment(client,message1))
    loop.create_task(message_get(client,message1))
    # - is download_attachment limited with message_get

@ratelimit_commands
async def ratelimit_test0057(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    loop.create_task(typing(client,channel1))
    loop.create_task(typing(client,channel2))
    #typing is not guild limited

@ratelimit_commands
async def ratelimit_test0058(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(typing(client,channel1))
    loop.create_task(typing(client,channel1))
    #typing is channel limited

@ratelimit_commands
async def ratelimit_test0059(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    channel2 = await client.channel_private_create(message.author)
    await sleep(5.,loop)
    loop.create_task(typing(client,channel1))
    loop.create_task(typing(client,channel2))
    #typing is not global limited

@ratelimit_commands
async def ratelimit_test0060(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1 = await client.channel_private_create(message.author)
    channel2 = await client.channel_private_create(Partial_user(user1_id))
    await sleep(5.,loop)
    loop.create_task(typing(client,channel1))
    loop.create_task(typing(client,channel2))
    #typing is not global PM limited
    
@ratelimit_commands
async def ratelimit_test0061(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(message_create(client,channel1,'test'))
    loop.create_task(typing(client,channel1))
    # - is typing limited with message_create

@ratelimit_commands
async def ratelimit_test0062(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1 = await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(typing(client,channel1))
    # - is typing limited with message_edit
                     
@ratelimit_commands
async def ratelimit_test0063(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await client_edit(client,name='Kemoji Koishi')
    await client_edit(client,name='Koishi')
    # - is client_edit - name limited

@ratelimit_commands
async def ratelimit_test0064(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    with open(os.path.join(os.path.abspath('.'),'images',
            '0000000A_touhou_koishi_kokoro_reversed.png'),'rb') as file:
        avatar=file.read()
    await client_edit(client,avatar=avatar)
    # - is client_edit - avatar limited

@ratelimit_commands
async def ratelimit_test0065(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    with open(os.path.join(os.path.abspath('.'),'avatar.png'),'rb') as file:
        avatar=file.read()
    await client_edit(client,name='Koishi',avatar=avatar)
    # - is client_edit - double limited

@ratelimit_commands
async def ratelimit_test0066(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await client_connections(client)
    # - is client_connections limited

@ratelimit_commands
async def ratelimit_test0067(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    profile1=client.guild_profiles[guild1]
    nick1='Nyaishi'
    nick2=None
    await client_edit_nick(client,guild1,nick1)
    await client_edit_nick(client,guild1,nick2)
    #client_edit_nick is guild limited

@ratelimit_commands
async def ratelimit_test0068(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    guild2=guild_iterator.__next__()
    profile1=client.guild_profiles[guild1]
    profile2=client.guild_profiles[guild2]
    nick1='Nyaishi'
    nick2=None
    await client_edit_nick(client,guild1,nick1)
    await client_edit_nick(client,guild2,nick1)
    await client_edit_nick(client,guild1,nick2)
    await client_edit_nick(client,guild2,nick2)
    # - is client_edit_nick global limited
    
@ratelimit_commands
async def ratelimit_test0069(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    guild2=guild_iterator.__next__()
    nick1='Nyaishi'
    nick2=None
    print('turn1')
    await client_edit_nick(client,guild1,nick1)
    await client_edit_nick(client,guild2,nick1)

    await sleep(10.,loop)
    print('turn2')
    
    await client_edit_nick(client,guild1,nick2)
    await client_edit_nick(client,guild2,nick2)
    #client_edit_nick is GLOBALLY limited

@ratelimit_commands
async def ratelimit_test0070(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await client_application_info(client)
    # - is client_application_info limited

@ratelimit_commands
async def ratelimit_test0071(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    loop.create_task(client_connections(client))
    loop.create_task(client_application_info(client))
    # - is client_connections limited with client_application_info

@ratelimit_commands
async def ratelimit_test0072(client,message,cotent):
    if message.author is not client.owner:
        return
    loop=client.loop
    await client_login_static(client)
    # - is client_login_static limited

@ratelimit_commands
async def ratelimit_test0073(client,message,cotent):
    if message.author is not client.owner:
        return
    loop=client.loop
    await client_logout(client)
    # - is client_logout limited

@ratelimit_commands
async def ratelimit_test0074(client,message,cotent):
    if message.author is not client.owner:
        return
    loop=client.loop
    loop.create_task(client_login_static(client))
    loop.create_task(client_logout(client))
    # - is client_logout limited with client_login_static
    
@ratelimit_commands
async def ratelimit_test0075(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    message1=await client.message_create(channel1,'test')
    await sleep(5.,loop)
    loop.create_task(message_edit(client,message1,'notsotest'))
    loop.create_task(message_pin(client,message1))
    #message_edit is not limited with message_pin

@ratelimit_commands
async def ratelimit_test0076(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    loop.create_task(typing(client,channel1))
    await sleep(3.,loop)
    loop.create_task(typing(client,channel1))
    await sleep(2.,loop)
    loop.create_task(typing(client,channel1))
    await sleep(1.,loop)
    loop.create_task(typing(client,channel1))
    #await crashed for me, did every await 3 times, till pc restart.
    
@ratelimit_commands
async def ratelimit_test0077(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1,channel2=message.channel.category.channels[0:2]
    await permission_ow_create(client,channel1,Partial_user(user2_id),156,148)
    await permission_ow_create(client,channel2,Partial_user(user2_id),156,148)
    #permission_ow_create is not guild limited
    #permission_ow_create is UNLIMITED

@ratelimit_commands
async def ratelimit_test0078(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    await permission_ow_create(client,channel1,Partial_user(user2_id),256,149)
    await permission_ow_create(client,channel1,Partial_user(user2_id),356,138)
    #permission_ow_create is not channel limited

@ratelimit_commands
async def ratelimit_test0079(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    await permission_ow_create(client,channel1,Partial_user(user2_id),256,149)
    await permission_ow_delete(client,channel1,Partial_user(user2_id))
    #permission_ow_create is not limited with permission_ow_delete
    #permission_ow_delete is UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0080(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel.category.channels[-1]
    channel2=message.channel.category.channels[-2]
    await channel_edit(client,channel1,name='tesuto-channel4')
    await channel_edit(client,channel2,name='tesuto-channel5')
    #channel_edit is not limited by guild
    #channel_edit is UNLIMITED

@ratelimit_commands
async def ratelimit_test0081(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel.category.channels[-2]
    await channel_edit(client,channel1,name='tesuto-channel6')
    await channel_edit(client,channel1,name='tesuto-channel8')
    #channel_edit is not limited by channel

@ratelimit_commands
async def ratelimit_test0082(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    channel1 = await client.channel_create(guild1,category=None,type_=0,name='tesuto_channel12')
    channel2 = await client.channel_create(guild1,category=None,type_=0,name='tesuto_channel13')
    await channel_delete(client,channel1)
    await channel_delete(client,channel2)
    #channel_delete is not limited by guild
    #channel_delete is UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0083(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    channel1 = await client.channel_create(guild1,category=None,type_=0,name='tesuto_channel15')
    await channel_edit(client,channe2,name='tesuto-channel9')
    await channel_delete(client,channel1)
    # - is channel_delete limited with channel_edit

@ratelimit_commands
async def ratelimit_test0084(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await oauth2_token(client)
    #oauth2_token is UNLIMITED

@ratelimit_commands
async def ratelimit_test0085(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    await invite_create(client,channel1)
    await invite_get_channel(client,channel1)
    #invite_create is not limited with invite_get_channel
    #invite_get_channel is UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0086(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    guild2=guild_iterator.__next__()
    channel1=message.channel
    channel2=guild2.channels[0]
    await invite_create(client,channel1)
    await invite_create(client,channel2)
    #invite_create is limited GLOBALLY

@ratelimit_commands
async def ratelimit_test0087(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    await webhook_create(client,channel1,'testnya')
    await webhook_get_channel(client,channel1)
    #webhook create and webhook_get_channel are UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0088(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    
    guild = await guild_create(client,name='nomnom',
        channels=[cr_pg_channel_object(name=f'awoooo',type_=0),])

    await sleep(1.,loop)
    await client.guild_delete(guild)
    #guild create is UNLIMITED

@ratelimit_commands
async def ratelimit_test0089(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    guild2=guild_iterator.__next__()
    await guild_get(client,guild1.id)
    await guild_get(client,guild2.id)
    #guild_get is UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0090(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild = await client.guild_create(name='Luv ya')
    await sleep(1.,loop)
    await guild_delete(client,guild)
    #guild_delete is UNLIMITED

@ratelimit_commands
async def ratelimit_test0091(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1 = await client.guild_create(name='Luv ya1')
    guild2 = await client.guild_create(name='Luv ya2')
    await sleep(1.,loop)
    await guild_edit(client,guild1,'test1')
    await guild_edit(client,guild2,'test2')
    await sleep(1.,loop)
    await client.guild_delete(guild1)
    await client.guild_delete(guild2)
    #guild_edit UNLIMITED

@ratelimit_commands
async def ratelimit_test0092(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    with open(os.path.join(os.path.abspath('.'),'images',
        '0000000A_touhou_koishi_kokoro_reversed.png'),'rb') as file:
        icon=file.read()
        
    guild1 = await client.guild_create(name='Luv ya1')
    await sleep(1.,loop)
    await guild_edit(client,guild1,'test1',icon=icon)
    await guild_edit(client,guild1,'test1',icon=None)
    await sleep(1.,loop)
    await client.guild_delete(guild1)
    #guild_edit UNLIMITED

@ratelimit_commands
async def ratelimit_test0093(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    with open(os.path.join(os.path.abspath('.'),'images',
        '0000000A_touhou_koishi_kokoro_reversed.png'),'rb') as file:
        icon=file.read()
        
    guild1 = message.guild
    await guild_edit(client,guild1,'test1',icon=icon)
    #guild_edit UNLIMITED (just wont responde propably if limited)

@ratelimit_commands
async def ratelimit_test0094(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    guild2=guild_iterator.__next__()
    await audit_logs(client,guild1)
    await audit_logs(client,guild2)
    await audit_logs(client,guild1)
    await audit_logs(client,guild2)
    #audit_logs UNLIMITED

@ratelimit_commands
async def ratelimit_test0095(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    guild2=guild_iterator.__next__()
    await guild_bans(client,guild1)
    await guild_bans(client,guild2)
    await guild_bans(client,guild1)
    await guild_bans(client,guild2)
    #guild_bans UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0096(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild2_id]
    guild2=client.guilds[guild1_id]
    print('adding')
    await guild_ban_add(client,guild1,user1_id)
    await guild_ban_add(client,guild1,user2_id)
    await guild_ban_add(client,guild2,user1_id)
    await guild_ban_add(client,guild2,user2_id)
    print('getting')
    await guild_ban_get(client,guild1,user1_id)
    await guild_ban_get(client,guild1,user2_id)
    await guild_ban_get(client,guild2,user1_id)
    await guild_ban_get(client,guild2,user2_id)
    print('deleting')
    await guild_ban_delete(client,guild1,user1_id)
    await guild_ban_delete(client,guild1,user2_id)
    await guild_ban_delete(client,guild2,user1_id)
    await guild_ban_delete(client,guild2,user2_id)
    #guild_ban_add is UNLIMITED
    #guild_ban_get is UNLIMITED
    #guild_ban_delete is UNLIMITED

@ratelimit_commands
async def ratelimit_test0097(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    await channel_move(client,channel=channel1,visual_position=3)
    #channel_move UNLIMITED

@ratelimit_commands
async def ratelimit_test0098(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await channel_create(client,guild1)
    #channel_create UNLIMITED

@ratelimit_commands
async def ratelimit_test0099(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await guild_embed_get(client,guild1)
    await guild_embed_edit(client,guild1,True)
    await guild_embed_edit(client,guild1,False)
    #guild_embed_get is UNLIMITED
    #guild_embed_edit is UNLIMITED

@ratelimit_commands
async def ratelimit_test0100(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await guild_embed_image(client,guild1)
    #guild_embed_image is UNLIMITED

@ratelimit_commands
async def ratelimit_test0101(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await guild_emojis(client,guild1)
    #guild_emojis is UNLIMITED

@ratelimit_commands
async def ratelimit_test0102(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    with open(os.path.join(os.path.abspath('.'),'satania-waa.png'),'rb') as file:
        image=file.read()
    await emoji_create(client,guild1,'sataniawaa',image)
    #emoji_create limited by guild
    
@ratelimit_commands
async def ratelimit_test0103(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await emoji_get(client,guild1,guild1.emojis.__iter__().__next__())
    #emoji_get is UNLIMITED

@ratelimit_commands
async def ratelimit_test0104(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    emoji=max(guild1.emojis.values(),key=lambda x:x.created_at)
    await emoji_delete(client,guild1,emoji)
    #emoji_delete limited by guild

@ratelimit_commands
async def ratelimit_test0105(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    emoji=max(guild1.emojis.values(),key=lambda x:x.created_at)
    await emoji_edit(client,guild1,emoji,'test')
    await emoji_edit(client,guild1,emoji,'sataniawaa')
    #limited by guild
    
@ratelimit_commands
async def ratelimit_test0106(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild2_id]
    guild2=client.guilds[guild1_id]
    emoji1=max(guild1.emojis.values(),key=lambda x:x.created_at)
    emoji2=max(guild2.emojis.values(),key=lambda x:x.created_at)
    await emoji_delete(client,guild1,emoji1)
    await emoji_delete(client,guild2,emoji2)
    #emoji_delete limited GLOBALLY

@ratelimit_commands
async def ratelimit_test0107(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild2_id]
    guild2=client.guilds[guild1_id]
    emoji1=max(guild1.emojis.values(),key=lambda x:x.created_at)
    emoji2=max(guild2.emojis.values(),key=lambda x:x.created_at)
    await emoji_edit(client,guild1,emoji1,'test')
    await emoji_edit(client,guild2,emoji2,'test')
    #emoji_edit limited GLOBALLY

@ratelimit_commands
async def ratelimit_test0108(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    emoji1=max(guild1.emojis.values(),key=lambda x:x.created_at)
    await emoji_edit(client,guild1,emoji1,'kyaaaoy')
    await emoji_delete(client,guild1,emoji1)
    #emoji_edit not limited with emoji_delete

@ratelimit_commands
async def ratelimit_test0109(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await integration_get_all(client,guild1)
    #integration_get_all is UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0110(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await invite_get_guild(client,guild1)
    #invite_get_guild is UNLIMITED

@ratelimit_commands
async def ratelimit_test0111(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]

    await guild_user_delete(client,guild1,user1_id)
    await guild_user_delete(client,guild1,user2_id)
    #guild_user_delete is guild limited

@ratelimit_commands
async def ratelimit_test0112(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    guild2=client.guilds[guild2_id]
    await guild_user_delete(client,guild1,user1_id)
    await guild_user_delete(client,guild1,user2_id)
    await guild_user_delete(client,guild2,user1_id)
    await guild_user_delete(client,guild2,user2_id)
    #guild_user_delete is not global limited

@ratelimit_commands
async def ratelimit_test0113(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    user1=guild1.users[user1_id]

    await user_edit(client,guild1,user1,'owo')
    #user_edit is limited

@ratelimit_commands
async def ratelimit_test0114(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    guild2=client.guilds[guild2_id]
    user1=guild1.users[user1_id]
    user2=guild2.users[user2_id]
    await user_edit(client,guild1,user1,'owo')
    await user_edit(client,guild2,user2,'owo')
    #user_edit is not globally limited
    #user_edit is limited by guild

@ratelimit_commands
async def ratelimit_test0115(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds.join'])
    user = await client.user_info(access)
    guild = await client.guild_create(name='Luv ya',
                channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=Channel_text),])
    await sleep(.5,loop)
    await guild_user_add(client,guild,user)
    await sleep(.5,loop)
    await client.guild_delete(guild)
    #guild_user_add is limited

@ratelimit_commands
async def ratelimit_test0116(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds.join'])
    user = await client.user_info(access)
    guild = await client.guild_create(name='Luv ya',
                channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=Channel_text),])
    await sleep(.5,loop)
    await guild_user_add(client,guild,user)
    await sleep(.5,loop)
    await user_edit(client,guild,user,'owo')
    await client.guild_delete(guild)
    #guild_user_add is not limited with user_edit
    
@ratelimit_commands
async def ratelimit_test0117(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds.join'])
    user = await client.user_info(access)
    guild = await client.guild_create(name='Luv ya',
                channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=Channel_text),])
    await sleep(.5,loop)
    await guild_user_add(client,guild,user)

    result=parse_oauth2_redirect_url(content)
    access = await client.activate_authorization_code(*result,['guilds.join'])
    user = await client.user_info(access)
    await guild_user_add(client,guild,user)
    await sleep(.5,loop)
    await client.guild_delete(guild)
    #guild_user_add is limited by guild

@ratelimit_commands
async def ratelimit_test0117(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds.join'])
    user = await client.user_info(access)
    guild = await client.guild_create(name='Luv ya',
                channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=Channel_text),])
    await sleep(.5,loop)
    await guild_user_add(client,guild,user)

    result=parse_oauth2_redirect_url(content)
    access = await client.activate_authorization_code(*result,['guilds.join'])
    user = await client.user_info(access)
    await guild_user_add(client,guild,user)
    await sleep(.5,loop)
    await client.guild_delete(guild)
    #guild_user_add is limited by guild
    
@ratelimit_commands
async def ratelimit_test0118(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    role1=guild1.roles[1] #lul
    user1=guild1.users[user2_id]
    await user_role_add(client,user1,role1)
    await user_role_delete(client,user1,role1)
    await user_role_add(client,user1,role1)
    await user_role_delete(client,user1,role1)
    #user_role_add is limited with user_role_delete

@ratelimit_commands
async def ratelimit_test0119(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    role1=guild1.roles[1] #lul
    user1=guild1.users[user1_id]
    user2=guild1.users[user2_id]
    
    await user_role_add(client,user1,role1)
    await user_role_delete(client,user1,role1)
    
    await user_role_add(client,user2,role1)
    await user_role_delete(client,user2,role1)
    #user_role_add is guild limited


@ratelimit_commands
async def ratelimit_test0120(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    guild2=client.guilds[guild2_id]
    role1=guild1.roles[1] #lul
    role2=guild2.roles[1] #oof
    user1=guild1.users[user2_id]
    
    await user_role_add(client,user1,role1)
    await user_role_delete(client,user1,role1)
    
    await user_role_add(client,user1,role2)
    await user_role_delete(client,user1,role2)
    #user_role_add is not global limited

@ratelimit_commands
async def ratelimit_test0121(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    role1=guild1.roles[1] #lul
    user1=guild1.users[user1_id]
    await user_edit(client,guild1,user1,'owo')
    await user_role_add(client,user1,role1)
    await user_role_delete(client,user1,role1)
    #user_edit is not limited with user_role_add
    
@ratelimit_commands
async def ratelimit_test0122(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    await guild_prune_estimate(client,guild1)
    await guild_prune(client,guild1)
    #guild_prune and guild_prune_estimate are UNLIMITED

@ratelimit_commands
async def ratelimit_test0123(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    await role_create(client,guild1,name='test')
    role1=guild1.roles[2]
    await role_move(client,role1,4)
    #role_create and role_move are UNLIMITED

@ratelimit_commands
async def ratelimit_test0124(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    role1=guild1.roles[2]
    await role_edit(client,role1,name='uwu')
    await role_delete(client,role1)
    #role_edit and role_delete are unlimited

@ratelimit_commands
async def ratelimit_test0125(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    await webhook_get_guild(client,guild1)
    #webhook_get_guild is UNLIMITED
    
@ratelimit_commands
async def ratelimit_test0126(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await guild_widget_image(client,guild1)
    #guild_embed_image is UNLIMITED

@ratelimit_commands
async def ratelimit_test0127(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    invite = await client.invite_create_pref(guild1)
    await invite_get(client,invite)
    await invite_delete(client,invite)
    #invite_delete is UNLIMITED

@ratelimit_commands
async def ratelimit_test0128(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=client.guilds[guild1_id]
    guild2=client.guilds[guild2_id]
    invite1 = await client.invite_create_pref(guild1)
    invite2 = await client.invite_create_pref(guild2)
    await invite_get(client,invite1)
    await invite_get(client,invite2)
    await invite_get(client,invite1)
    await invite_get(client,invite2)
    await client.invite_delete(invite1)
    await client.invite_delete(invite2)
    #invite_get limited GLOBALLY
    
@ratelimit_commands
async def ratelimit_test0129(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['email','identify'])
    await user_info(client,access)
    #user_info is UNLIMITED

@ratelimit_commands
async def ratelimit_test0130(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await client_user(client)
    #client_user is UNLIMITED

@ratelimit_commands
async def ratelimit_test0131(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await channel_private_get_all(client)
    #channel_private_get_all is UNLIMITED

@ratelimit_commands
async def ratelimit_test0132(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await channel_private_create(client,client.owner)
    #channel_private_create is UNLIMITED

@ratelimit_commands
async def ratelimit_test0133(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['connections'])
    await user_connections(client,access)
    #user_connections is UNLIMITED

@ratelimit_commands
async def ratelimit_test0134(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds'])
    await user_guilds(client,access)
    #user_guilds is limited

@ratelimit_commands
async def ratelimit_test0135(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds'])
    loop.create_task(user_guilds(client,access))
    loop.create_task(user_guilds(client,access))
    loop.create_task(user_guilds(client,access))
    #user_guilds is limited GLOBALLY (cant be other)

@ratelimit_commands
async def ratelimit_test0136(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    await guild_get_all(client)
    #guild_get_all is limited
    
@ratelimit_commands
async def ratelimit_test0137(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    loop.create_task(guild_get_all(client))
    loop.create_task(guild_get_all(client))
    loop.create_task(guild_get_all(client))
    #guild_get_all is limited globally

@ratelimit_commands
async def ratelimit_test0138(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds'])
    loop.create_task(user_guilds(client,access))
    loop.create_task(user_guilds(client,access))
    loop.create_task(guild_get_all(client))
    loop.create_task(guild_get_all(client))
    #guild_get_all is not limited with user_guilds

@ratelimit_commands
async def ratelimit_test0139(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1 = await client.guild_create(name='pls kill me')
    sleep(.5,loop)
    await guild_delete(client,guild1)
    #guild_delete is UNLIMITED

@ratelimit_commands
async def ratelimit_test0140(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    user1=message.author
    await user_get(client,user1)
    #user_get is limited

@ratelimit_commands
async def ratelimit_test0141(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    user1=message.author
    loop.create_task(user_get(client,user1))
    loop.create_task(user_get(client,user1))
    loop.create_task(user_get(client,user1))
    loop.create_task(user_get(client,user1))
    #user_get is limited globally probs

@ratelimit_commands
async def ratelimit_test0142(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    
    guild1=message.guild
    webhooks = await client.webhook_get_guild(guild1)
    webhook1=webhooks[0]
    await webhook_get(client,webhook1)
    #webhook_get is UNLIMITED

@ratelimit_commands
async def ratelimit_test0143(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    webhook1 = await client.webhook_create(channel1,'test')
    await webhook_edit(client,webhook1,'notsotest')
    await webhook_delete(client,webhook1)
    #webhook_edit and webhook_delete are UNLIMITED

@ratelimit_commands
async def ratelimit_test0144(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    
    guild1=message.guild
    webhooks = await client.webhook_get_guild(guild1)
    webhook1=webhooks[0]
    await webhook_get_token(client,webhook1)
    #webhook_get_token is UNLIMITED

@ratelimit_commands
async def ratelimit_test0145(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    channel1=message.channel
    webhook1 = await client.webhook_create(channel1,'test')
    await webhook_edit_token(client,webhook1,'notsotest')
    await webhook_execute(client,webhook1,'works?')
    await webhook_execute(client,webhook1,'works?')
    await webhook_delete_token(client,webhook1)
    #webhook_edit_token and webhook_delete_token are UNLIMITED
    #webhook_execute is limited by webhook_id

@ratelimit_commands
async def ratelimit_test0146(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    await guild_users(client,guild1)
    #guild_users is limited by guild

@ratelimit_commands
async def ratelimit_test0147(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild_iterator=client.guilds.values().__iter__()
    guild1=guild_iterator.__next__()
    guild2=guild_iterator.__next__()
    await guild_users(client,guild1)
    await guild_users(client,guild2)
    #guild_users is not limited by global

@ratelimit_commands
async def ratelimit_test0148(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    access = await client.owners_access(['guilds.join'])
    user = await client.user_info(access)
    guild = await client.guild_create(name='Luv ya',
                channels=[cr_pg_channel_object(name=f'Love u {message.author.name}',type_=Channel_text),])
    await sleep(.5,loop)
    await guild_user_add(client,guild,user)
    await guild_users(client,guild)
    await sleep(.5,loop)
    await client.guild_delete(guild)
    #guild_users is not limited with guild_user_add

@ratelimit_commands
async def ratelimit_test0149(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    data = await guild_regions(client,guild1)
    #guild_regions is unlimited

@ratelimit_commands
async def ratelimit_test0150(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    data = await guild_channels(client,guild1)
    #guild_channels is unlimited

@ratelimit_commands
async def ratelimit_test0151(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    data = await guild_roles(client,guild1)
    #guild_roles is unlimited
    
@ratelimit_commands
async def ratelimit_test0152(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    user1_id=message.author.id
    await user_get_profile(client,guild1,user1_id)
    #user_get_profile is limited

@ratelimit_commands
async def ratelimit_test0153(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    guild2=client.guilds[guild2_id]
    user1_id=message.author.id
    for x in range(6):
        loop.create_task(guild_user_get(client,guild1,user1_id))
    #2s ratelimit

@ratelimit_commands
async def ratelimit_test0154(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    guild2=client.guilds[guild2_id]
    user1_id=message.author.id
    loop.create_task(guild_user_get(client,guild1,user1_id))
    loop.create_task(guild_user_get(client,guild2,user1_id))
    #limited globally

@ratelimit_commands
async def ratelimit_test155(client,message,content):
    if message.author is not client.owner:
        return
    messages = await client.messages_till_index(message.channel)
    for message in messages:
        await message_delete(client,message)

    #message_delete ratelimit is known only after the first request

@ratelimit_commands
async def ratelimit_test0156(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    for _ in range(10):
        data = await guild_roles(client,guild1)
    #guild_roles is UNLIMITED #just a check for making sure about the others

@ratelimit_commands
async def ratelimit_test0157(client,message,content):
    if message.author is not client.owner:
        return
    loop=client.loop
    guild1=message.guild
    for _ in range(2):
        await guild_widget_get(client,guild1.id)
