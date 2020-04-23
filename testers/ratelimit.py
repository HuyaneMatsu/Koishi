# -*- coding: utf-8 -*-
import os, re
join=os.path.join
from threading import current_thread
from time import time as time_now
from email._parseaddr import _parsedate_tz
from datetime import datetime, timedelta, timezone

from hata import Future, sleep, Task, WaitTillAll, AsyncIO, CancelledError, multidict_titled, titledstr, Embed, \
    alchemy_incendiary, Webhook, eventlist, EventThread, DiscordException, BUILTIN_EMOJIS, Message, ChannelText, \
    VoiceRegion, VerificationLevel, MessageNotificationLevel, ContentFilterLevel, DISCORD_EPOCH, User, Client, \
    Achievement, UserOA2, parse_oauth2_redirect_url, cr_pg_channel_object, ChannelCategory, Role, GUILDS

from hata.backend.dereaddons_local import _spaceholder
from hata.backend.futures import _EXCFrameType, render_frames_to_list, render_exc_to_list
from hata.backend.hdrs import DATE, METH_PATCH, METH_GET, METH_DELETE, METH_POST, METH_PUT, AUTHORIZATION, \
    CONTENT_TYPE
from hata.backend.http import Request_CM
from hata.discord.others import to_json, from_json, quote, bytes_to_base64, ext_from_base64, Discord_hdrs
from hata.discord.guild import PartialGuild
from hata.discord.http import VALID_ICON_FORMATS, VALID_ICON_FORMATS_EXTENDED
from hata.ext.commands import wait_for_message, Pagination, wait_for_reaction, Command, checks

RATELIMIT_RESET=Discord_hdrs.RATELIMIT_RESET
RATELIMIT_RESET_AFTER=Discord_hdrs.RATELIMIT_RESET_AFTER

RATELIMIT_COMMANDS=eventlist(type_=Command, category='RATELIMIT TESTS')

def setup(lib):
    Koishi.command_processer.create_category('RATELIMIT TESTS',checks=[checks.owner_only()])
    Koishi.commands.extend(RATELIMIT_COMMANDS)
    
def teardown(lib):
    Koishi.command_processer.delete_category('RATELIMIT TESTS')

def parsedate_to_datetime(data):
    *dtuple, tz = _parsedate_tz(data)
    if tz is None:
        return datetime(*dtuple[:6])
    return datetime(*dtuple[:6],tzinfo=timezone(timedelta(seconds=tz)))

def parse_header_ratelimit(headers):
    delay1=( \
        datetime.fromtimestamp(float(headers[RATELIMIT_RESET]),timezone.utc)
        -parsedate_to_datetime(headers[DATE])
            ).total_seconds()
    delay2=float(headers[RATELIMIT_RESET_AFTER])
    return (delay1 if delay1<delay2 else delay2)

async def bypass_request(client,method,url,data=None,params=None,reason=None,header=None,decode=True,):
    self=client.http
    if header is None:
        header=self.header.copy()
    header[titledstr.bypass_titling('X-RateLimit-Precision')]='millisecond'
    
    if CONTENT_TYPE not in header and data and isinstance(data,(dict,list)):
        header[CONTENT_TYPE]='application/json'
        #converting data to json
        data=to_json(data)

    if reason:
        header['X-Audit-Log-Reason']=quote(reason)
    
    try_again=5
    while try_again:
        try_again-=1
        with RLTPrinterBuffer() as buffer:
            buffer.write(f'Request started : {url} {method}\n')
            
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
        
        with RLTPrinterBuffer() as buffer:
            headers=response.headers
            status=response.status
            if headers['content-type']=='application/json':
                response_data=from_json(response_data)
            
            value=headers.get('X-Ratelimit-Global',None)
            if value is not None:
                buffer.write(f'global : {value}\n')
            value=headers.get('X-Ratelimit-Limit',None)
            if value is not None:
                buffer.write(f'limit : {value}\n')
            value=headers.get('X-Ratelimit-Remaining',None)
            if value is not None:
                buffer.write(f'remaining : {value}\n')
                
            value=headers.get('X-Ratelimit-Reset',None)
            if value is not None:
                delay=parse_header_ratelimit(headers)
                buffer.write(f'reset : {value}, after {delay} seconds\n')
            value=headers.get('X-Ratelimit-Reset-After',None)
            if value is not None:
                buffer.write(f'reset after : {value}\n')
    
            
            if 199<status<305:
                if headers.get('X-Ratelimit-Remaining','1')=='0':
                    buffer.write(f'reached 0\n try again after {delay}\n',)
                return response_data
            
            if status==429:
                retry_after=response_data['retry_after']/1000.
                buffer.write(f'RATE LIMITED\nretry after : {retry_after}\n',)
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

class RLTCTX(object): #rate limit tester context manager
    active_ctx=None
    
    __slots__ = ('task', 'client', 'channel', 'title',)
    
    def __new__(cls,client,channel,title):
        thread=current_thread()
        if type(thread) is not EventThread:
            raise RuntimeError(f'{cls.__name__} can be created only at an {EventThread.__name__}')
        current_task=thread.current_task
        if current_task is None:
            raise RuntimeError(f'{cls.__name__} was created outside of a task')
            
        self=object.__new__(cls)
        self.task=current_task
        self.client=client
        self.channel=channel
        self.title=title
        return self

    def __enter__(self):
        active_ctx=type(self).active_ctx
        if (active_ctx is not None):
            raise RuntimeError(f'There is an already active {self.__class__.__name__} right now.')
        
        type(self).active_ctx=self
        return self
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        type(self).active_ctx=None
        if exc_type is CancelledError:
            return True
        
        if exc_type is None:
            Task(self._render_exit_result(),self.client.loop)
            return True
        
        Task(self._render_exit_exc(exc_val,exc_tb),self.client.loop)
        return True
    
    async def _render_exit_result(self):
        unit_result = []
        
        for unit in RLTPrinterBuffer.buffers:
            if type(unit) is str:
                unit_result.append(unit)
                unit_result.append('\n')
                continue
            
            task=unit.task
            unit_result.append(f'Task `{task.name}`')
            unit_result.append('\n')
            
            for date,buffer in unit.buffer:
                date=date.__format__('%Y.%m.%d-%H:%M:%S-%f')
                unit_result.append(date)
                unit_result.append(':\n')
                
                unit_result.extend(buffer)
                unit_result.append('\n')
                
            exception=task.exception()
            if exception is None:
                continue
            
            if type(exception) is DiscordException:
                unit_result.append(repr(exception))
                unit_result.append('\n')
                continue
            
            unit_result.append('```')
            await self.client.loop.run_in_executor(alchemy_incendiary(render_exc_to_list,(exception,unit_result,),))
            unit_result.append('\n')
            unit_result.append('```')
            unit_result.append('\n')

        RLTPrinterBuffer.buffers.clear()
        
        pages = []
        contents = []
        page_content_length = 0
        in_code_block=0
        
        for str_ in unit_result:
            local_length=len(str_)
            
            page_content_length+=local_length
            if page_content_length<1996:
                if str_=='```':
                    in_code_block^=1
                contents.append(str_)
                continue
            
            if contents[-1]=='\n':
                del contents[-1]
            
            if in_code_block:
                if contents[-1]=='```':
                    del contents[-1]
                else:
                    if str_=='```':
                        in_code_block=0
                    contents.append('\n```')
            else:
                if str_=='```':
                    in_code_block=2
            
            pages.append(Embed(self.title,''.join(contents)))
            contents.clear()
            if in_code_block==1:
                contents.append('```\n')
                local_length+=4
            elif in_code_block==2:
                contents.append('```')
                local_length+=3
                in_code_block=1
            
            if str_=='\n':
                page_content_length=0
                continue
            
            contents.append(str_)
            page_content_length=local_length
            continue

        if page_content_length:
            pages.append(Embed(self.title,''.join(contents)))
            
        del unit_result
        del contents
        
        if pages:
            page_count=len(pages)
            index=0
            for page in pages:
                index=index+1
                page.add_footer(f'Page {index}/{page_count}')
        else:
            pages.append(Embed(self.title,).add_footer('Page 1/1'))
        
        await Pagination(self.client,self.channel,pages)
        
    async def _render_exit_exc(self,exception,tb):
        frames=[]
        while True:
            if tb is None:
                break
            frame=_EXCFrameType(tb)
            frames.append(frame)
            tb=tb.tb_next
        
        extend=[]
        extend.append('```Traceback (most recent call last):\n')
        await self.client.loop.run_in_executor(alchemy_incendiary(render_frames_to_list,(frames,),{'extend':extend}))
        extend.append(repr(exception))
        extend.append('\n```')
        pages = []
        contents = []
        page_content_length = 0
    
        for str_ in extend:
            local_length=len(str_)
            page_content_length+=local_length
            if page_content_length<1996:
                contents.append(str_)
                continue
                
            if contents[-1]=='\n':
                del contents[-1]
            
            contents.append('\n```')
            pages.append(Embed(self.title,''.join(contents)))
            contents.clear()
            contents.append('```\n')
            
            if str_=='\n':
                page_content_length=0
                continue
            
            contents.append(str_)
            page_content_length=local_length
            continue

        if page_content_length:
            pages.append(Embed(self.title,''.join(contents)))
            
        del contents
        
        page_count=len(pages)
        index=0
        for page in pages:
            index=index+1
            page.add_footer(f'Page {index}/{page_count}')
        
        await Pagination(self.client,self.channel,pages)
    
    def write(self,content):
        RLTPrinterBuffer.buffers.append(content)
    
    async def send(self,description):
        await Pagination(self.client,self.channel,[Embed(self.title,description).add_footer('Page 1/1')])
        raise CancelledError()
            
class RLTPrinterUnit(object):
    __slots__=('task','buffer','start_new_block',)
    def __init__(self,task):
        self.task=task
        self.buffer=[]
        self.start_new_block=True
    
    def write(self,content):
        if self.start_new_block:
            buffer=[]
            self.buffer.append((datetime.now(),buffer),)
            self.start_new_block=False
        else:
            buffer=self.buffer[-1][1]
        
        buffer.append(content)
    
class RLTPrinterBuffer(object):
    buffers=[]
    __slots__=('buffer',)
    
    def __init__(self):
        thread=current_thread()
        if type(thread) is not EventThread:
            raise RuntimeError(f'{self.__name__}.__enter__ can be used only at an {EventThread.__name__}')
        current_task=thread.current_task
        if current_task is None:
            raise RuntimeError(f'{self.__name__}.__enter__ was used outside of a task')
        
        for buffer in self.buffers:
            if type(buffer) is str:
                continue
            if buffer.task is current_task:
                buffer.start_new_block=True
                break
        else:
            buffer=RLTPrinterUnit(current_task)
            self.buffers.append(buffer)
        
        self.buffer=buffer
    
    def __enter__(self):
        return self.buffer
    
    def __exit__(self,exc_type,exc_val,exc_tb):
        self.buffer.start_new_block=True
        return False
        
        
async def reaction_add(client,message,emoji,):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return await bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me',
        )
        
async def reaction_delete(client,message,emoji,user,):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    user_id=user.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}',
        )

async def reaction_delete_own(client,message,emoji,):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me',
        )

async def reaction_clear(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions',)

async def reaction_users(client,message,emoji,):
    if message.reactions is None:
        return []
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/reactions/{reaction}',
        params={'limit':100},)

async def message_create(client,channel,content=None,embed=None,):
    data={}
    if content is not None and content:
        data['content']=content
    if embed is not None:
        data['embed']=embed.to_data()
    channel_id=channel.id
    data = await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages',
        data,)
    return Message.new(data,channel)

async def message_delete(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}',)

async def message_delete_multiple(client,messages,):
    if len(messages)==0:
        return
    if len(messages)==1:
        return message_delete(client,messages[0])
    data={'messages':[message.id for message in messages]}
    channel_id=messages[0].channel.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/bulk_delete',
        data,)

async def message_edit(client,message,content=None,embed=None,):
    data={}
    if content is not None:
        data['content']=content
    if embed is not None:
        data['embed']=embed.to_data()
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}',
        data,)

async def message_pin(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/channels/{channel_id}/pins/{message_id}',
        )

async def message_unpin(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}/pins/{message_id}',
        )

async def message_pinneds(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/pins',
        )

async def message_logs(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages',
        params={'limit':1},)

async def message_get(client,channel,message_id,):
    channel_id=channel.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}',
        )

async def download_attachment(client,attachment,):
    if attachment.proxy_url.startswith('https://cdn.discordapp.com/'):
        url=attachment.proxy_url
    else:
        url=attachment.url
    return await bypass_request(client,METH_GET,url,header=multidict_titled(),decode=False,
        )


async def typing(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/typing',
        )

async def client_edit(client,name='',avatar=b'',):
    data={}
    if name:
        if not (1<len(name)<33):
            raise ValueError(f'The length of the name can be between 2-32, got {len(name)}')
        data['username']=name
    
    if avatar is None:
        data['avatar']=None
    elif avatar:
        avatar_data=bytes_to_base64(avatar)
        ext=ext_from_base64(avatar_data)
    return await bypass_request(client,METH_PATCH,
        'https://discordapp.com/api/v7/users/@me',
        data,)

async def client_connections(client,):
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/connections',
        )

async def client_edit_nick(client,guild,nick,):
    guild_id=guild.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/@me/nick',
        {'nick':nick},)

async def client_gateway_bot(client,):
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/gateway/bot',
        )

async def client_application_info(client,):
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/oauth2/applications/@me',
        )

async def client_login_static(client,):
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me',
        )

async def client_logout(client,):
    return await bypass_request(client,METH_POST,
        'https://discordapp.com/api/v7/auth/logout',
        )


async def permission_ow_create(client,channel,target,allow,deny,):
    if type(target) is Role:
        type_='role'
    elif type(target) in (User,Client,UserOA2):
        type_='member'
    else:
        raise TypeError(f'Target expected to be Role or User type, got {type(target)!r}')
    data = {
        'target':target.id,
        'allow':allow,
        'deny':deny,
        'type':type_,
            }
    channel_id=channel.id
    overwrite_id=target.id
    return await bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/channels/{channel_id}/permissions/{overwrite_id}',
        data,)

async def permission_ow_delete(client,channel,overwrite,):
    channel_id=channel.id
    overwrite_id=overwrite.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}/permissions/{overwrite_id}',
        )

async def channel_edit(client,channel,name='',topic='',nsfw=None,slowmode=None,user_limit=None,bitrate=None,type_=128,):
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
        if bitrate<8000 or bitrate>(96000,128000)['VIP' in channel.guild.feautres]:
            raise ValueError(f'Invalid bitrate {bitrate!r}, should be 8000-96000 (128000 for vip)')
        data['bitrate']=bitrate
        
        if user_limit:
            if user_limit<1 or user_limit>99:
                raise ValueError(f'Invalid user_limit {user_limit!r}, should be 0 for unlimited or 1-99')
            data['user_limit']=user_limit

    channel_id=channel.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/channels/{channel_id}',
        data,)

async def channel_delete(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{channel_id}',
        )

async def oauth2_token(client,):
    data = {
        'client_id'     : client.id,
        'client_secret' : client.secret,
        'grant_type'    : 'client_credentials',
        'scope'         : 'connections'
            }
    
    headers=multidict_titled()
    dict.__setitem__(headers,CONTENT_TYPE,['application/x-www-form-urlencoded'])
                
    return await bypass_request(client,METH_POST,
        'https://discordapp.com/api/oauth2/token',
        data,header=headers,)

async def invite_create(client,channel,):
    data = {
        'max_age'   : 60,
        'max_uses'  : 1,
        'temporary' : False,
        'unique'    : True,
            }
    channel_id=channel.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/invites',
        data,)

async def invite_get_channel(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/invites',
        )

async def webhook_create(client,channel,name,avatar=b'',):
    data={'name':name}
    if avatar:            
        data['avatar']=bytes_to_base64(avatar)
            
    channel_id=channel.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/webhooks',
        data,)

async def webhook_get_channel(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/channels/{channel_id}/webhooks',
        )

async def guild_create(client,name,icon=None,avatar=b'',
        region=VoiceRegion.eu_central,
        verification_level=VerificationLevel.medium,
        message_notification_level=MessageNotificationLevel.only_mentions,
        content_filter_level=ContentFilterLevel.disabled,
        roles=[],channels=[],):
        
    if client.is_bot and len(client.guilds)>9:
        raise ValueError('Bots cannot create a new server if they have more than 10.')

    if not (1<len(name)<101):
        raise ValueError(f'Guild\'s name\'s length can be between 2-100, got {len(name)}')
    
    data = {
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
        'https://discordapp.com/api/v7/guilds',
        data,)
    #we can create only partial, because the guild data is not completed usually
    return PartialGuild(data)

async def guild_get(client,guild_id,):
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}',
        )

async def guild_delete(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}',
        )

async def guild_edit(client,guild,name,icon=b'',): #keep it short
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
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}',
        data,)

async def audit_logs(client,guild,):
    data={'limit':100}
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/audit-logs',
        params=data,)

async def guild_bans(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans',
        )

async def guild_ban_add(client,guild,user_id,):
    data={'delete-message-days':0}
    guild_id=guild.id
    return await bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans/{user_id}',
        params=data,)

async def guild_ban_delete(client,guild,user_id,):
    guild_id=guild.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans/{user_id}',
        )

async def guild_ban_get(client,guild,user_id,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/bans/{user_id}',
        )

async def channel_move(client,*args,file=None,**kwargs):
    def http_channel_move_redirect(self,guild_id,data,reason):
        return bypass_request(client,METH_PATCH,
            f'https://discordapp.com/api/v7/guilds/{guild_id}/channels',data,
            )
    original=type(client.http).channel_move
    type(client.http).channel_move=http_channel_move_redirect
    coro=client.channel_move(*args,**kwargs)
    future=Future(client.loop)
    #skip 1 loop
    client.loop.call_at(0.0,future.__class__.set_result_if_pending,future,None)
    await future
    
    type(client.http).channel_move=original
    await coro

async def channel_create(client,guild,category=None,):
    data=cr_pg_channel_object(type_=0,name='tesuto-channel9')
    data['parent_id']=category.id if type(category) is ChannelCategory else None
    guild_id=guild.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/channels',
        data,)

async def guild_embed_get(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/embed',
        )

async def guild_embed_edit(client,guild,value,):
    data={'enabled':value}
    guild_id=guild.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/embed',
        data,)

async def guild_embed_image(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/embed.png',
        params={'style':'shield'},decode=False,header={},)

async def guild_emojis(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis',
        )

async def emoji_create(client,guild,name,image,):
    image=bytes_to_base64(image)
    name=''.join(re.findall('([0-9A-Za-z_]+)',name))
    if not (1<len(name)<33):
        raise ValueError(f'The length of the name can be between 2-32, got {len(name)}')
    
    data = {
        'name'      : name,
        'image'     : image,
        'role_ids'  : []
            }
        
    guild_id=guild.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis',
        data,)

async def emoji_get(client,guild,emoji_id,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis/{emoji_id}',
        )

async def emoji_delete(client,guild,emoji,):
    guild_id=guild.id
    emoji_id=emoji.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis/{emoji_id}',
        )

async def emoji_edit(client,guild,emoji,name,): #keep it short
    data={'name':name}
    guild_id=guild.id
    emoji_id=emoji.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/emojis/{emoji_id}',
        data,)

async def integration_get_all(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/integrations',
        )

async def invite_get_guild(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/invites',
        )

async def guild_user_delete(client,guild,user_id,):
    guild_id=guild.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}',
        )

async def user_edit(client,guild,user,nick,mute=False,):
    guild_id=guild.id
    user_id=user.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}',
        data={'nick':nick,'mute':mute},)

async def guild_user_add(client,guild,user,):
    guild_id=guild.id
    user_id=user.id
    return await bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}',
        data={'access_token':user.access.access_token},)

async def user_role_add(client,user,role,):
    guild_id=role.guild.id
    user_id=user.id
    role_id=role.id
    return await bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
        )

async def user_role_delete(client,user,role,):
    guild_id=role.guild.id
    user_id=user.id
    role_id=role.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
        )

async def guild_prune(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/prune',
        params={'days':30},)

async def guild_prune_estimate(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/prune',
        params={'days':30},)

async def role_create(client,guild,name=None,permissions=None,color=None,
        separated=None,mentionable=None,reason=None,):

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
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles',
        data=data,)

async def role_move(client,role,new_position,):
    data=role.guild.roles.change_on_switch(role,new_position,key=lambda role,pos:{'id':role.id,'position':pos})
    guild_id=role.guild.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles',
        data=data,)

async def role_edit(client,role,color=None,separated=None,mentionable=None,
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
        permissions=role.permissions

    data = {
        'name'        : name,
        'permissions' : permissions,
        'color'       : color,
        'hoist'       : separated,
        'mentionable' : mentionable,
            }
    guild_id=role.guild.id
    role_id=role.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles/{role_id}',
        data=data,)

async def role_delete(client,role,):
    guild_id=role.guild.id
    role_id=role.id
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles/{role_id}',
        )


async def webhook_get_guild(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/webhooks',
        )

async def guild_widget_image(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/widget.png',
        params={'style':'shield'},decode=False,header={},)

async def invite_get(client,invite,):
    invite_code=invite.code
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/invites/{invite_code}',
        )

async def invite_delete(client,invite,):
    invite_code=invite.code
    return await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/invites/{invite_code}',
        )

async def user_info(client,access,):
    header=multidict_titled()
    header[AUTHORIZATION]=f'Bearer {access.access_token}'
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me',
        header=header,)

async def client_user(client,):
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me',
        )

async def channel_private_get_all(client,):
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/channels',
        )

async def channel_private_create(client,user,):
    return await bypass_request(client,METH_POST,
        'https://discordapp.com/api/v7/users/@me/channels',
        data={'recipient_id':user.id},)

async def user_connections(client,access,):
    header=multidict_titled()
    header[AUTHORIZATION]=f'Bearer {access.access_token}'
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/connections',
        header=header,)

async def user_guilds(client,access,):
    header=multidict_titled()
    header[AUTHORIZATION]=f'Bearer {access.access_token}'
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/guilds',
        header=header,)

async def guild_get_all(client,):
    return await bypass_request(client,METH_GET,
        'https://discordapp.com/api/v7/users/@me/guilds',
        params={'after':0},)

async def user_get(client,user,):
    user_id=user.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/users/{user_id}',
        )

async def webhook_get(client,webhook,):
    webhook_id=webhook.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/webhooks/{webhook_id}',
        )

async def webhook_delete(client,webhook,):
    webhook_id=webhook.id
    return  bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/webhooks/{webhook_id}',
        )

async def webhook_edit(client,webhook,name,): #keep it short
    webhook_id=webhook.id
    return await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/webhooks/{webhook_id}',
        data={'name':name},)

async def webhook_get_token(client,webhook,):
    return await bypass_request(client,METH_GET,
        webhook.url,header={},)

async def webhook_delete_token(client,webhook,):
    return await bypass_request(client,METH_DELETE,
        webhook.url,header={},)

async def webhook_edit_token(client,webhook,name,): #keep it short
    return await bypass_request(client,METH_PATCH,
        webhook.url,
        data={'name':name},header={},)

async def webhook_execute(client,webhook,content,wait=False,):
    return await bypass_request(client,METH_POST,
        f'{webhook.url}?wait={wait:d}',
        data={'content':content},header={},)
    
async def guild_users(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members',
        )

async def guild_regions(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/regions',
        )

async def guild_channels(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/channels',
        )

async def guild_roles(client,guild,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/roles',
        )

async def guild_user_get(client,guild,user_id,):
    guild_id=guild.id
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/members/{user_id}',
        )

async def guild_widget_get(client,guild_id,):
    return await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/widget.json',
        header={},)

async def message_suppress_embeds(client,message,suppress=True,):
    message_id=message.id
    channel_id=message.channel.id
    return await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/messages/{message_id}/suppress-embeds',
        data={'suppress':suppress},)

async def channel_follow(client,source_channel,target_channel,):
    if source_channel.type!=5:
        raise ValueError(f'\'source_channel\' must be type 5, so news (announcements) channel, got {source_channel}')
    if target_channel.type not in ChannelText.INTERCHANGE:
        raise ValueError(f'\'target_channel\' must be type 0 or 5, so any guild text channel, got  {target_channel}')

    data = {
        'webhook_channel_id': target_channel.id,
            }

    channel_id=source_channel.id

    data = await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/channels/{channel_id}/followers',
        data,)
    webhook=Webhook._from_follow_data(data,source_channel,target_channel,client)
    return webhook

async def achievement_get(client,achievement_id,):
    application_id=client.application.id
        
    data = await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/applications/{application_id}/achievements/{achievement_id}',
        )
    
    return Achievement(data)
    

async def achievement_create(client,name,description,icon,secret=False,secure=False,):
    icon_data=bytes_to_base64(icon)
    ext=ext_from_base64(icon_data)
    if ext not in VALID_ICON_FORMATS_EXTENDED:
        raise ValueError(f'Invalid icon type: {ext}')

    data = {
        'name'          : {
            'default'   : name,
                },
        'description'   : {
            'default'   : description,
                },
        'secret'        : secret,
        'secure'        : secure,
        'icon'          : icon_data,
            }

    application_id=client.application.id
        
    data =  await bypass_request(client,METH_POST,
        f'https://discordapp.com/api/v7/applications/{application_id}/achievements',
        data=data,)
    
    return Achievement(data)

async def achievement_delete(client,achievement,):
    application_id=client.application.id
    achievement_id=achievement.id
    await bypass_request(client,METH_DELETE,
        f'https://discordapp.com/api/v7/applications/{application_id}/achievements/{achievement_id}',
        )

async def achievement_edit(client,achievement,name=None,description=None,secret=None,secure=None,icon=_spaceholder,):
    data={}
    if (name is not None):
        data['name'] = {
            'default'   : name,
                }
    if (description is not None):
        data['description'] = {
            'default'   : description,
                }
    if (secret is not None):
        data['secret']=secret
        
    if (secure is not None):
        data['secure']=secure
        
    if (icon is not _spaceholder):
        icon_data=bytes_to_base64(icon)
        ext=ext_from_base64(icon_data)
        if ext not in VALID_ICON_FORMATS_EXTENDED:
            raise ValueError(f'Invalid icon type: {ext}')
        data['icon']=icon_data

    application_id=client.application.id
    achievement_id=achievement.id
    
    data = await bypass_request(client,METH_PATCH,
        f'https://discordapp.com/api/v7/applications/{application_id}/achievements/{achievement_id}',
        data=data,)

    achievement._update_no_return(data)
    return achievement

async def achievement_get_all(client,):
    application_id=client.application.id
    
    data = await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/applications/{application_id}/achievements',
        )
    
    return [Achievement(achievement_data) for achievement_data in data]

async def user_achievement_update(client,user,achievement,percent_complete,):
    data={'percent_complete':percent_complete}
    
    user_id=user.id
    application_id=client.application.id
    achievement_id=achievement.id
    
    await bypass_request(client,METH_PUT,
        f'https://discordapp.com/api/v7/users/{user_id}/applications/{application_id}/achievements/{achievement_id}',
        data=data,)

async def user_achievements(client,access,):
    header=multidict_titled()
    header[AUTHORIZATION]=f'Bearer {access.access_token}'
    
    application_id=client.application.id
    
    data = await bypass_request(client,METH_GET,
        f'https://discordapp.com/api/v7/users/@me/applications/{application_id}/achievements',
        header=header,)
    
    return [Achievement(achievement_data) for achievement_data in data]

async def reaction_delete_emoji(client, message, emoji):
    await bypass_request(client, METH_DELETE,
        f'https://discordapp.com/api/v7/channels/{message.channel.id}/messages/{message.id}/reactions/{emoji.as_reaction}')

async def guild_preview(client, guild_id):
    await bypass_request(client, METH_GET,
        f'https://discordapp.com/api/v7/guilds/{guild_id}/preview')

async def message_crosspost(client, message):
    await bypass_request(client, METH_POST,
        f'https://discordapp.com/api/v7//channels/{message.channel.id}/messages/{message.id}/crosspost')

@RATELIMIT_COMMANDS
async def ratelimit_test0000(client,message):
    '''
    Does 6 achievement get request towards 1 achievemt.
    The bot's application must have at least 1 achievement created.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0000') as RLT:
        try:
            achievements = await client.achievement_get_all()
        except BaseException as err:
            await RLT.send(repr(err))
        
        if not achievements:
            await RLT.send(repr('The application has no achievement'))
        
        achievement=achievements[0]
        achievement_id=achievement.id
        
        loop=client.loop
        
        tasks=[]
        for _ in range(6):
            task=Task(achievement_get(client,achievement_id),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
    #achievement_get limited. limit:5, reset:5
    
@RATELIMIT_COMMANDS
async def ratelimit_test0001(client,message):
    '''
    Does 3-3 achievement get request towards 2 achievemts.
    The bot's application must have at least 2 achievement created.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0001') as RLT:
        try:
            achievements = await client.achievement_get_all()
        except BaseException as err:
            await RLT.send(repr(err))
        
        if len(achievements)<3:
            await RLT.send(repr('The application has less than 2 achievements'))
        
        achievement_1=achievements[0]
        achievement_2=achievements[1]
        
        achievement_id_1=achievement_1.id
        achievement_id_2=achievement_2.id
        
        loop=client.loop
        
        tasks=[]
        for _ in range(4):
            task=Task(achievement_get(client,achievement_id_1),loop)
            tasks.append(task)
            
            task=Task(achievement_get(client,achievement_id_2),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
    #achievement_get limited globally
    
@RATELIMIT_COMMANDS
async def ratelimit_test0002(client,message):
    '''
    Creates 6 achievements.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0002') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        loop=client.loop
        
        tasks=[]
        names=('Yura','Hana','Neko','Kaze','Scarlet','Yukari')
        for name in names:
            description=name+'boroshi'
            task=Task(achievement_create(client,name,description,image),loop)
            tasks.append(task)
            
        await WaitTillAll(tasks,loop)
        
        for task in tasks:
            try:
                achievement=task.result()
            except:
                pass
            else:
                await client.achievement_delete(achievement.id)
    #achievement_create limited. limit:5, reset:5, globally
    
@RATELIMIT_COMMANDS
async def ratelimit_test0003(client,message):
    '''
    First creates 2 achievements with the client normally, then deletes them for testing.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0003') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievements=[]
        for name in ('Cake','Neko'):
            description=name+' are love'
            achievement = await client.achievement_create(name,description,image)
            achievements.append(achievement)
        
        loop=client.loop
        
        tasks = []
        for achievement in achievements:
            task = Task(achievement_delete(client,achievement),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
    #achievement_delete limited. limit:5, reset:5, globally

@RATELIMIT_COMMANDS
async def ratelimit_test0004(client,message):
    '''
    Creates an achievent, then edits it twice for testing. When done, deletes it.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0004') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Cake','Nekos are love',image)
        
        loop=client.loop
        tasks = []
        
        task = Task(achievement_edit(client,achievement,name='Hana'),loop)
        tasks.append(task)
        
        task = Task(achievement_edit(client,achievement,name='Phantom'),loop)
        tasks.append(task)
        
        await WaitTillAll(tasks,loop)
        await client.achievement_delete(achievement)
    #achievement_edit limited. limit:5, reset:5
    
@RATELIMIT_COMMANDS
async def ratelimit_test0005(client,message):
    '''
    Creates 2 achievements, then edits them once, once for testing. At the end deletes them.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0005') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievements=[]
        for name in ('Kokoro','Koishi'):
            description='UwUwUwU'
            achievement = await client.achievement_create(name,description,image)
            achievements.append(achievement)
    
        loop=client.loop
        tasks = []
        for achievement in achievements:
            task = Task(achievement_edit(client,achievement,name='Yura'),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
        
        for achievement in achievements:
            await client.achievement_delete(achievement)
    #achievement_edit limited globally

@RATELIMIT_COMMANDS
async def ratelimit_test0006(client,message):
    '''
    Creates, edits and deletes an achievment.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0006') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await achievement_create(client,'Kokoro','is love',image)
        await achievement_get(client,achievement.id)
        await achievement_edit(client,achievement,name='Yurika')
        await achievement_delete(client,achievement)
    
    # achievement_create, achievement_get, achievement_edit, achievement_delete are NOT grouped
    
@RATELIMIT_COMMANDS
async def ratelimit_test0007(client,message):
    '''
    Requests all the achievemenets.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0007') as RLT:
        loop=client.loop
        tasks = []
        for _ in range(2):
            task = Task(achievement_get_all(client),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
    
    #achievement_get_all limited. limit:5, reset:5, globally

@RATELIMIT_COMMANDS
async def ratelimit_test0008(client,message):
    '''
    Updates an achievement of the client's owner.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0008') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi','Kokoro',image,secure=True)
        
        try:
            await user_achievement_update(client,client.owner,achievement,100)
        finally:
            await client.achievement_delete(achievement)
    
    # DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    # user_achievement_update limited. Limit : 5, reset : 5.
    
@RATELIMIT_COMMANDS
async def ratelimit_test0009(client,message):
    '''
    Updates an achievement of the client's owner.
    Waits 2 seconds after the achievement is created, so it might work this time (nope).
    '''
    with RLTCTX(client,message.channel,'ratelimit_test0009') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi','Kokoro',image,secure=True)
        await sleep(2.0,client.loop) # wait some time this time
        
        try:
            await user_achievement_update(client,client.owner,achievement,100)
        finally:
            await client.achievement_delete(achievement)

    # DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    
@RATELIMIT_COMMANDS
async def ratelimit_test0010(client,message):
    '''
    Updates an achievement of the client's owner. But now one, what has `secure=False`
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0010') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi','Kokoro',image) #no just a normal one
        
        try:
            await user_achievement_update(client,client.owner,achievement,100)
        finally:
            await client.achievement_delete(achievement)
    
    # DiscordException FORBIDDEN (403), code=40001: Unauthorized

@RATELIMIT_COMMANDS
async def ratelimit_test0011(client,message):
    '''
    Updates the achievemenets of all the owners of the client.
    '''
    
    with RLTCTX(client,message.channel,'ratelimit_test0011') as RLT:
        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi','Kokoro',image,secure=True)
        
        loop=client.loop
        tasks=[]
        for member in client.application.owner.members:
            user = member.user
            task=Task(user_achievement_update(client,user,achievement,100),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
        await client.achievement_delete(achievement)
    
    # DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    #limited globally

class check_is_owner(object):
    __slots__=('client', )
    def __init__(self,client):
        self.client=client
    
    def __call__(self,message):
        return self.client.is_owner(message.author)
    
@RATELIMIT_COMMANDS
async def ratelimit_test0012(client,message):
    '''
    Tries to get a user's achievemenets after oauth2 authorization.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0012') as RLT:
        await client.message_create(channel, (
            'Please authorize yourself and resend the redirected url after it\n'
            'https://discordapp.com/oauth2/authorize?client_id=486565096164687885'
            '&redirect_uri=https%3A%2F%2Fgithub.com%2FHuyaneMatsu'
            '&response_type=code&scope=identify%20applications.store.update'))
        
        try:
            message = await wait_for_message(client,channel,check_is_owner(client),60.)
        except TimeoutError:
            await RLT.send('Timeout meanwhile waiting for redirect url.')
    
        Task(client.message_delete(message),client.loop)
        try:
            result=parse_oauth2_redirect_url(message.content)
        except ValueError:
            await RLT.send('Bad redirect url.')
        
        access = await client.activate_authorization_code(*result,['identify', 'applications.store.update'])
        
        if access is None:
            await RLT.send('Too old redirect url.')
        
        await user_achievements(client,access)
    #DiscordException UNAUTHORIZED (401): 401: Unauthorized
    # no limit data provided

ratelimit_test0020_OK       = BUILTIN_EMOJIS['ok_hand']
ratelimit_test0020_CANCEL   = BUILTIN_EMOJIS['x']
ratelimit_test0020_EMOJIS   = (ratelimit_test0020_OK, ratelimit_test0020_CANCEL)

class ratelimit_test0020_checker(object):
    __slots__ = ('client',)
    
    def __init__(self, client):
        self.client=client
    
    def __call__(self, emoji, user):
        if not self.client.is_owner(user):
            return False
        
        if emoji not in ratelimit_test0020_EMOJIS:
            return False
        
        return True

@RATELIMIT_COMMANDS
async def ratelimit_test0013(client,message):
    '''
    Requests messages for each day from the channel if can, then deletes them if you agree with it as well.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0013') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        target_time=int((time_now()-40*86400.)*1000.-DISCORD_EPOCH)<<22
        async for message_ in client.message_iterator(channel):
            if message_.id>target_time:
                continue
            break
        
        now=time_now()
        time_bounds=[]
        for day in range(41):
            before= int((now-(day  )*86400.+100.)*1000.-DISCORD_EPOCH)<<22
            after = int((now-(day+1)*86400.-100.)*1000.-DISCORD_EPOCH)<<22
            time_bounds.append((before,after),)
        
        messages=[]
        for day in range(41):
            messages.append((None,None),)
        
        for message_ in channel.messages:
            for day,(before,after) in enumerate(time_bounds):
                if message_.id>before:
                    continue
                
                if message_.id<after:
                    continue
                
                message_own,message_other=messages[day]
                if (message_own is not None) and (message_other is not None):
                    break
                
                if message_.author==client:
                    if message_own is None:
                        messages[day]=(message_,message_other)
                else:
                    if message_other is None:
                        messages[day]=(message_own,message_)
                
                break
        
        result=['```\nday | own | other\n']
        for day,(message_own, message_other) in enumerate(messages):
            result.append(f'{day:>3} | {("YES", " NO")[message_own is None]} | {("YES"," NO")[message_other is None]}\n')
        result.append('```\nShould we start?')
        embed=Embed('Found messages',''.join(result))
        
        message = await client.message_create(channel,embed=embed)
        
        for emoji in ratelimit_test0020_EMOJIS:
            await client.reaction_add(message,emoji)
        
        try:
            _, emoji, _ = await wait_for_reaction(client, message, ratelimit_test0020_checker(client), 40.)
        except TimeoutError:
            emoji = ratelimit_test0020_CANCEL
            
        await client.reaction_clear(message)
        
        if emoji is ratelimit_test0020_CANCEL:
            embed.add_footer('ratelimit_test0020 cancelled')
            await client.message_edit(message,embed=embed)
            raise CancelledError()
        
        if emoji is ratelimit_test0020_OK:
            loop=client.loop
            for day,(message_own, message_other) in enumerate(messages):
                if (message_own is not None):
                    RLT.write(f'day {day}, own:')
                    await Task(message_delete(client,message_own),loop)
                
                if (message_other is not None):
                    RLT.write(f'day {day}, other:')
                    await Task(message_delete(client,message_other),loop)
            
            return
            
        # no more case
        
@RATELIMIT_COMMANDS
async def ratelimit_test0014(client,message):
    '''
    Creates 2 message.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0014') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
            
        messages=[]
        for index in range(2):
            message_ = await client.message_create(channel,f'testing ratelimit: message {index}')
            messages.append(message_)
        
        await Task(message_delete_multiple(client,messages),client.loop)

@RATELIMIT_COMMANDS
async def ratelimit_test0015(client,message):
    '''
    Deletes all the reactions of a single emoji from a message.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0015') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        emoji = BUILTIN_EMOJIS['x']
        await reaction_delete_emoji(client, message, emoji)

@RATELIMIT_COMMANDS
async def ratelimit_test0016(client,message):
    '''
    Adds a reaction and deletes alll the same type from the message.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0016') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        emoji = BUILTIN_EMOJIS['x']
        await reaction_add(client, message, emoji)
        await reaction_delete_emoji(client, message, emoji)

@RATELIMIT_COMMANDS
async def ratelimit_test0017(client,message):
    '''
    Requests 1 guild preview.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0017') as RLT:
        await guild_preview(client, 197038439483310086)

@RATELIMIT_COMMANDS
async def ratelimit_test0018(client,message):
    '''
    Requests 2 guild preview.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0018') as RLT:
        await guild_preview(client, 302094807046684672)
        await guild_preview(client, 197038439483310086)

@RATELIMIT_COMMANDS
async def ratelimit_test0019(client,message):
    '''
    Edits the channel twice.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0019') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        nsfw=channel.nsfw
        
        await channel_edit(client, channel, nsfw = (not nsfw))
        await channel_edit(client, channel, nsfw = nsfw)

@RATELIMIT_COMMANDS
async def ratelimit_test0020(client,message):
    '''
    Creates a channel.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0020') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        data = await channel_create(client, guild)
        channel_id=int(data['id'])
        await client.http.channel_delete(channel_id,None)

@RATELIMIT_COMMANDS
async def ratelimit_test0021(client,message):
    '''
    Deletes a channel.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0021') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        channel = await client.channel_create(guild, name='Kanako', type_=0)
        await channel_delete(client, channel)

@RATELIMIT_COMMANDS
async def ratelimit_test0022(client,message):
    '''
    Edits a role.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0022') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        role = await client.role_create(guild,name='Sanae')
        await role_edit(client, role, name='Chiruno')
        await client.role_delete(role)

@RATELIMIT_COMMANDS
async def ratelimit_test0023(client,message):
    '''
    Creates a role.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0023') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        data = await role_create(client, guild, name='Yukari')
        role_id=int(data['id'])
        await client.http.role_delete(guild.id,role_id,None)

@RATELIMIT_COMMANDS
async def ratelimit_test0024(client,message):
    '''
    Deletes a role.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0024') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        role = await client.role_create(guild,name='Sakuya')
        await role_delete(client, role)

@RATELIMIT_COMMANDS
async def ratelimit_test0025(client,message):
    '''
    Edits 2 channel.
    '''
    channel_1 = message.channel
    with RLTCTX(client,channel_1,'ratelimit_test0025') as RLT:
        if channel_1.guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel_1.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        category = channel_1.category
        if category is None:
            await RLT.send('The channel should be at a category')
        
        channel_2=None
        for channel in category.channels:
            if channel is channel_1:
                continue
            
            if type(channel) is not ChannelText:
                continue
            
            channel_2 = channel
            break
        
        if channel_2 is None:
            await RLT.send('I want 2 text channels at the category of this channel.')
        
        nsfw_1=channel_1.nsfw
        nsfw_2=channel_2.nsfw
        
        await channel_edit(client, channel_1, nsfw = (not nsfw_1))
        await channel_edit(client, channel_2, nsfw = (not nsfw_2))
        
        await client.channel_edit(channel_1, nsfw = nsfw_1)
        await client.channel_edit(channel_2, nsfw = nsfw_2)

@RATELIMIT_COMMANDS
async def ratelimit_test0026(client,message):
    '''
    Edits 2 roles at the same guild.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0026') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not guild.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        role_1 = await client.role_create(guild,name='Sanae')
        role_2 = await client.role_create(guild,name='Reimu')
        await role_edit(client, role_1, name='Chiruno')
        await role_edit(client, role_2, name='Ririi')
        await client.role_delete(role_1)
        await client.role_delete(role_2)

@RATELIMIT_COMMANDS
async def ratelimit_test0027(client, message, guild_id:str=''):
    '''
    Edits 1-1 roles at separate guilds.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0027') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
            
        if not guild_1.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        if not guild_2.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission at the other guild as well')
            
        role_1 = await client.role_create(guild_1,name='Sanae')
        role_2 = await client.role_create(guild_2,name='Reimu')
        await role_edit(client, role_1, name='Chiruno')
        await role_edit(client, role_2, name='Ririi')
        await client.role_delete(role_1)
        await client.role_delete(role_2)

@RATELIMIT_COMMANDS
async def ratelimit_test0028(client, message, guild_id:str=''):
    '''
    Creates 1-1 roles at separate guilds
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0027') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
            
        if not guild_1.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        if not guild_2.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission at the other guild as well')
            
        role_1_data = await role_create(client,guild_1,name='Yuyuko')
        role_2_data = await role_create(client,guild_2,name='Yoshika')
        role_1_id=int(role_1_data['id'])
        role_2_id=int(role_2_data['id'])
        await client.http.role_delete(guild_1.id,role_1_id,None)
        await client.http.role_delete(guild_2.id,role_2_id,None)

@RATELIMIT_COMMANDS
async def ratelimit_test0029(client,message):
    '''
    Moves a role.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0029') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        role = await client.role_create(guild,name='Sakuya')
        await role_move(client,role,2)
        await client.role_delete(role)

@RATELIMIT_COMMANDS
async def ratelimit_test0030(client, message):
    '''
    Crossposts 2 message at the current channel.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0030') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        if channel.type != 5:
            await RLT.send('Pls perform this action at a news channel.')
        
        message_1 = await client.message_create(channel, 'Hatate')
        message_2 = await client.message_create(channel, 'Iku')
        
        await message_crosspost(client, message_1)
        await message_crosspost(client, message_2)
        
        await client.message_delete(message_1)
        await client.message_delete(message_2)

@RATELIMIT_COMMANDS
async def ratelimit_test0031(client, message):
    '''
    Crossposts 1-1 messages at 2 different channels.
    '''
    channel = message.channel
    with RLTCTX(client,channel,'ratelimit_test0031') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_administrator:
            await RLT.send('I need admin permission to complete this command.')
        
        if channel.type != 5:
            await RLT.send('Pls perform this action at a news channel.')
        
        category = channel.category
        if category is None:
            await RLT.send('Pls perform this action at a channel within a category.')
        
        for channel_ in category.channels:
            if channel_ is channel:
                continue
            
            if channel_.type!=5:
                continue
            
            channel_2 = channel_
            break
        else:
            channel_2 = None
        
        if channel_2 is None:
            await RLT.send('The channel\'s category has only 1 news channel.')
        
        message_1 = await client.message_create(channel, 'Aya')
        message_2 = await client.message_create(channel_2, 'Chen')
        
        await message_crosspost(client, message_1)
        await message_crosspost(client, message_2)
        
        await client.message_delete(message_1)
        await client.message_delete(message_2)

