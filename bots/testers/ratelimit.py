import os, re
join = os.path.join
from threading import current_thread
from time import time as time_now
from email._parseaddr import _parsedate_tz
from datetime import datetime, timedelta, timezone

from hata import Embed, PrivacyLevel, ScheduledEventEntityType, datetime_to_timestamp,\
    DiscoveryCategory, Emoji, KOKORO, Webhook, eventlist, DiscordException, BUILTIN_EMOJIS, ChannelText,\
    ApplicationCommand, INTERACTION_RESPONSE_TYPES, VerificationScreen, WelcomeScreen, ChannelGuildUndefined, \
    ApplicationCommandPermission, ApplicationCommandPermissionOverwrite, PrivacyLevel, ChannelStage, \
    ERROR_CODES, ComponentType, Sticker, StickerPack, ChannelDirectory, Permission, \
    VoiceRegion, VerificationLevel, MessageNotificationLevel, ContentFilterLevel, DISCORD_EPOCH, User, Client, \
    Achievement, UserOA2, parse_oauth2_redirect_url, cr_pg_channel_object, ChannelCategory, Role, GUILDS, CLIENTS, \
    Team, WebhookType, PermissionOverwrite, ChannelVoice, Guild
from scarletio import sleep, Task, WaitTillAll, AsyncIO, CancelledError, IgnoreCaseMultiValueDictionary, \
    alchemy_incendiary,  EventThread, WaitTillExc, change_on_switch, to_json, from_json

from scarletio.utils.trace import ExceptionFrameProxy, render_frames_into, render_exception_into
from scarletio.web_common.headers import DATE, METHOD_PATCH, METHOD_GET, METHOD_DELETE, METHOD_POST, METHOD_PUT, \
    AUTHORIZATION, CONTENT_TYPE
from scarletio.http_client import RequestContextManager
from scarletio.web_common import quote, BasicAuth, Formdata
from hata.discord.utils import image_to_base64
from hata.discord.guild import create_partial_guild_from_data, GuildDiscovery
from hata.discord.channel import CHANNEL_TYPE_MAP
from hata.discord.http import API_ENDPOINT, STATUS_ENDPOINT
from hata.discord.http.headers import RATE_LIMIT_RESET, RATE_LIMIT_RESET_AFTER, RATE_LIMIT_PRECISION
from hata.discord.client.functionality_helpers import role_move_key

from hata.ext.command_utils import wait_for_message, wait_for_reaction
from hata.ext.commands_v2 import Command, checks, configure_converter
from hata.ext.slash.menus import Pagination

MAIN_CLIENT: Client
RATE_LIMIT_COMMANDS = eventlist(type_=Command, category='RATE_LIMIT TESTS')

def setup(lib):
    MAIN_CLIENT.command_processor.create_category('RATE_LIMIT TESTS', checks=[checks.owner_only()])
    MAIN_CLIENT.commands.extend(RATE_LIMIT_COMMANDS)
    
def teardown(lib):
    MAIN_CLIENT.command_processor.delete_category('RATE_LIMIT TESTS')

def parse_date_to_datetime(data):
    *date_tuple, tz = _parsedate_tz(data)
    if tz is None:
        return datetime( * date_tuple[:6])
    return datetime( * date_tuple[:6], tzinfo=timezone(timedelta(seconds=tz)))

def parse_header_rate_limit(headers):
    delay1 = ( \
        datetime.fromtimestamp(float(headers[RATE_LIMIT_RESET]), timezone.utc)
        -parse_date_to_datetime(headers[DATE])
            ).total_seconds()
    delay2=float(headers[RATE_LIMIT_RESET_AFTER])
    return (delay1 if delay1 < delay2 else delay2)

async def bypass_request(client,method,url,data=None,params=None,reason=None,headers=None,decode=True,):
    self=client.http
    if headers is None:
        headers=self.headers.copy()
    
    if CONTENT_TYPE not in headers and data and isinstance(data,(dict,list)):
        headers[CONTENT_TYPE] = 'application/json'
        #converting data to json
        data = to_json(data)

    if reason:
        headers['X-Audit-Log-Reason'] = quote(reason)
    
    try_again = 5
    while try_again:
        try_again -= 1
        with RLTPrinterBuffer() as buffer:
            buffer.write(f'Request started : {url} {method}\n')
            
        try:
            async with RequestContextManager(self._request(method, url, headers, data, params)) as response:
                if decode:
                    response_data = await response.text(encoding='utf-8')
                else:
                    response_data = ''
        except OSError as err:
            #os cant handle more, need to wait for the blocking job to be done
            await sleep(0.1, self.loop)
            #invalid address causes OSError too, but we will let it run 5 times, then raise a ConnectionError
            continue
        
        with RLTPrinterBuffer() as buffer:
            response_headers = response.headers
            status = response.status
            if response_headers['content-type'].startswith('application/json'):
                response_data = from_json(response_data)
            
            value = response_headers.get('X-Ratelimit-Global', None)
            if value is not None:
                buffer.write(f'global : {value}\n')
            value = response_headers.get('X-Ratelimit-Limit', None)
            if value is not None:
                buffer.write(f'limit : {value}\n')
            value = response_headers.get('X-Ratelimit-Remaining', None)
            if value is not None:
                buffer.write(f'remaining : {value}\n')
                
            value = response_headers.get('X-Ratelimit-Reset', None)
            if value is not None:
                delay = parse_header_rate_limit(response_headers)
                buffer.write(f'reset : {value}, after {delay} seconds\n')
            value = response_headers.get('X-Ratelimit-Reset-After', None)
            if value is not None:
                buffer.write(f'reset after : {value}\n')
    
            
            if 199<status<305:
                if response_headers.get('X-Ratelimit-Remaining', '1') == '0':
                    buffer.write(f'reached 0\n try again after {delay}\n',)
                return response_data
            
            if status==429:
                retry_after=response_data['retry_after']
                buffer.write(f'RATE LIMITED\nretry after : {retry_after}\n',)
                await sleep(retry_after,self.loop)
                continue
            
            elif status==500 or status==502:
                await sleep(10./try_again + 1.,self.loop)
                continue
            
            raise DiscordException(response, response_data, data)
    
    return None

class RLTCTX: #rate limit tester context manager
    active_ctx = None
    
    __slots__ = ('task', 'client', 'channel', 'title',)
    
    def __new__(cls,client,channel,title):
        thread = current_thread()
        if type(thread) is not EventThread:
            raise RuntimeError(f'{cls.__name__} can be created only at an {EventThread.__name__}')
        current_task = thread.current_task
        if current_task is None:
            raise RuntimeError(f'{cls.__name__} was created outside of a task')
            
        self = object.__new__(cls)
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
        type(self).active_ctx = None
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
            await self.client.loop.run_in_executor(alchemy_incendiary(render_exception_into,(exception,unit_result,),))
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
                index=index + 1
                page.add_footer(f'Page {index}/{page_count}')
        else:
            pages.append(Embed(self.title,).add_footer('Page 1/1'))
        
        await Pagination(self.client, self.channel, pages)
        
    async def _render_exit_exc(self,exception,tb):
        frames=[]
        while True:
            if tb is None:
                break
            frame=ExceptionFrameProxy(tb)
            frames.append(frame)
            tb=tb.tb_next
        
        extend=[]
        extend.append('```Traceback (most recent call last):\n')
        await self.client.loop.run_in_executor(alchemy_incendiary(render_frames_into,(frames,),{'extend':extend}))
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
            index=index + 1
            page.add_footer(f'Page {index}/{page_count}')
        
        await Pagination(self.client,self.channel,pages)
    
    def write(self,content):
        RLTPrinterBuffer.buffers.append(content)
    
    async def send(self,description):
        await Pagination(self.client,self.channel,[Embed(self.title,description).add_footer('Page 1/1')])
        raise CancelledError()
            
class RLTPrinterUnit:
    __slots__=('task','buffer','start_new_block',)
    def __init__(self,task):
        self.task=task
        self.buffer=[]
        self.start_new_block=True
    
    def write(self,content):
        if self.start_new_block:
            buffer=[]
            self.buffer.append((datetime.utcnow(),buffer),)
            self.start_new_block=False
        else:
            buffer=self.buffer[-1][1]
        
        buffer.append(content)
    
class RLTPrinterBuffer:
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
        self.buffer.start_new_block = True
        return False
        
        
async def reaction_add(client,message,emoji,):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return await bypass_request(client,METHOD_PUT,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me',
        )
        
async def reaction_delete(client,message,emoji,user,):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    user_id=user.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/{user_id}',
        )

async def reaction_delete_own(client,message,emoji,):
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}/@me',
        )

async def reaction_clear(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions',)

async def reaction_user_get_chunk(client,message,emoji,):
    if message.reactions is None:
        return []
    channel_id=message.channel.id
    message_id=message.id
    reaction=emoji.as_reaction
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/reactions/{reaction}',
        params={'limit':100},)

async def message_create(client, channel, content=None, embed=None,):
    data = {}
    if content is not None and content:
        data['content'] = content
    if embed is not None:
        data['embed'] = embed.to_data()
    channel_id = channel.id
    
    data = await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/messages',
        data,)
    
    return channel._create_new_message(data)

async def message_delete(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',)

async def message_delete_multiple(client,messages,):
    if len(messages)==0:
        return
    if len(messages)==1:
        return message_delete(client,messages[0])
    data={'messages':[message.id for message in messages]}
    channel_id=messages[0].channel.id
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/bulk-delete',
        data,)

async def message_edit(client,message,content=None,embed=None,):
    data={}
    if content is not None:
        data['content']=content
    if embed is not None:
        data['embed']=embed.to_data()
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',
        data,)

async def message_pin(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METHOD_PUT,
        f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}',
        )

async def message_unpin(client,message,):
    channel_id=message.channel.id
    message_id=message.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/pins/{message_id}',
        )

async def message_pinneds(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/pins',
        )

async def message_get_chunk(client,channel,):
    channel_id = channel.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/messages',
        params = {'limit': 1},)

async def message_get(client, channel, message_id,):
    channel_id = channel.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}',
        )

async def download_attachment(client,attachment,):
    if attachment.proxy_url.startswith('https://cdn.discordapp.com/'):
        url=attachment.proxy_url
    else:
        url=attachment.url
    return await bypass_request(client,METHOD_GET,url,headers=IgnoreCaseMultiValueDictionary(),decode=False,
        )


async def typing(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/typing',
        )

async def client_edit(client, name='', avatar=...,):
    data={}
    if name:
        if not (1<len(name)<33):
            raise ValueError(f'The length of the name can be between 2-32, got {len(name)}')
        data['username']=name
    
    if (avatar is not ...):
        if avatar is None:
            avatar_data = None
        else:
            avatar_data = image_to_base64(avatar)
    
        data['avatar'] = avatar_data
    
    return await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/users/@me',
        data,)

async def client_connection_get_all(client,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me/connections',
        )

async def client_guild_profile_nick_edit(client, guild, nick,):
    guild_id=guild.id
    return await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/@me/nick',
        {'nick':nick},)

async def client_guild_profile_edit(client, guild, nick,):
    guild_id=guild.id
    return await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/@me',
        {'nick':nick},)

async def client_gateway_bot(client,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/gateway/bot',
        )

async def client_application_get(client,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/oauth2/applications/@me',
        )

async def client_login_static(client,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me',
        )

async def client_logout(client,):
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/auth/logout',
        )


async def permission_overwrite_create(client,channel,target,allow,deny,):
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
    await bypass_request(client,METHOD_PUT,
        f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',
        data,)
    
    return PermissionOverwrite.custom(target,allow,deny)

async def permission_overwrite_delete(client,channel,overwrite,):
    channel_id=channel.id
    overwrite_id=overwrite.target.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/permissions/{overwrite_id}',
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
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/channels/{channel_id}',
        data,)

async def channel_delete(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}',
        )

async def oauth2_token(client,):
    data = {
        'grant_type'    : 'client_credentials',
        'scope'         : ' connections',
            }
    
    headers = IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION] = BasicAuth(str(client.id), client.secret).encode()
    headers[CONTENT_TYPE]='application/x-www-form-urlencoded'
                
    return await bypass_request(client,METHOD_POST,
        'https://discordapp.com/api/oauth2/token',
        data,headers=headers,)

async def invite_create(client,channel,):
    data = {
        'max_age'   : 60,
        'max_uses'  : 1,
        'temporary' : False,
        'unique'    : True,
            }
    channel_id=channel.id
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/invites',
        data,)

async def invite_get_channel(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/invites',
        )

async def webhook_create(client,channel,name,avatar=b'',):
    data={'name':name}
    if avatar:            
        data['avatar']=image_to_base64(avatar)
            
    channel_id=channel.id
    data = await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/webhooks',
        data,)
    return Webhook(data)

async def webhook_get_all_channel(client,channel,):
    channel_id=channel.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/webhooks',
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
        'icon'                          : None if icon is None else image_to_base64(avatar),
        'region'                        : region.value,
        'verification_level'            : verification_level.value,
        'default_message_notifications' : message_notification_level.value,
        'explicit_content_filter'       : content_filter_level.value,
        'roles'                         : roles,
        'channels'                      : channels,
            }

    data = await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/guilds',
        data,)
    #we can create only partial, because the guild data is not completed usually
    return create_partial_guild_from_data(data)

async def guild_get(client, guild_id,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}',
        )

async def guild_delete(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}',
        )

async def guild_edit(client, guild, afk_channel=...): #keep it short
    data = {}
    
    if (afk_channel is not ...):
        data['afk_channel'] = None if afk_channel is None else afk_channel.id
    
    guild_id=guild.id
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}',
        data,)

async def audit_log_get_chunk(client, guild,):
    data={'limit':100}
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/audit-logs',
        params=data,)

async def guild_ban_get_all(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/bans',
        )

async def guild_ban_add(client, guild,user_id,):
    data={'delete_message_days':0}
    guild_id=guild.id
    return await bypass_request(client,METHOD_PUT,
        f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',
        params=data,)

async def guild_ban_delete(client, guild,user_id,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',
        )

async def guild_ban_get(client, guild,user_id,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/bans/{user_id}',
        )

async def channel_move(client, channel, visual_position, category=..., parent= ..., lock_permissions=False,
        reason=None):
    
    if parent is not ...:
        category = parent
    
    guild = channel.guild
    if guild is None:
        return
    
    if category is ...:
        category = channel.category
    elif category is None:
        category = guild
    elif type(category) is Guild:
        if guild is not category:
            raise ValueError('Can not move channel between guilds!')
    elif type(category) is ChannelCategory:
        if category.guild is not guild:
            raise ValueError('Can not move channel between guilds!')
    else:
        raise TypeError(f'Invalid type {channel.__class__.__name__}')
    
    if type(channel) is type(category):
        raise ValueError('Cant move category under category!')
    
    if channel.parent is category and category.channels.index(channel)==visual_position:
        return #saved 1 request
    
    #making sure
    visual_position=int(visual_position)
    
    #quality python code incoming :ok_hand:
    ordered=[]
    indexes=[0,0,0,0,0,0,0] #for the 7 channel type (type 1 and 3 wont be used)

    #loop preparations
    outer_channels=guild.channels
    index_0=0
    limit_0=len(outer_channels)
    #inner loop preparations
    index_1=0
    #loop start
    while True:
        if index_0==limit_0:
            break
        channel_=outer_channels[index_0]
        #loop block start
        
        type_=channel_.type
        type_index=indexes[type_]
        indexes[type_]=type_index + 1
        
        ordered.append((index_0,index_1,type_index,channel_),)
        
        if type_==4:
            #reset type_indexes
            indexes[0]=indexes[2]=indexes[5]=indexes[6]=0
            #loop preparations
            inner_channels=channel_.channels
            limit_1=len(inner_channels)
            #loop start
            while True:
                if index_1==limit_1:
                    break
                channel_=inner_channels[index_1]
                #loop block start
                
                type_=channel_.type
                type_index=indexes[type_]
                indexes[type_]=type_index + 1
                
                ordered.append((index_0,index_1,type_index,channel_),)
                
                #loop block end
                index_1=index_1 + 1
            #reseting inner
            index_1=0
            #loop ended
        
        #loop block end
        index_0=index_0 + 1
    #loop ended
    
    #prepare loop
    index_0=0
    limit_0=len(ordered)
    #loop start
    while True:
        if index_0==limit_0:
            break
        info_line=ordered[index_0]
        #loop block start
        
        if info_line[3] is channel:
            original_position=index_0
            break

        #loop block end
        index_0=index_0 + 1
    #loop ended

    restricted_positions=[]
    
    index_0=0
    limit_0=len(ordered)
    last_index=-1
    if type(category) is Guild:
        #loop start
        while True:
            if index_0==limit_0:
                break
            info_line=ordered[index_0]
            #loop block start
            
            if info_line[0]>last_index:
                last_index+=1
                restricted_positions.append(index_0)
            
            #loop block end
            index_0=index_0 + 1
        #loop ended
    else:
        #loop start
        while True:
            if index_0==limit_0:
                break
            info_line=ordered[index_0]
            category_index=index_0 #we might need it
            #loop block start
            if info_line[3] is category:
                index_0=index_0 + 1
                #loop preapre
                #loop start
                while True:
                    if index_0==limit_0:
                        break
                    info_line=ordered[index_0]
                    #loop block start

                    if info_line[3].type==4:
                        break
                    restricted_positions.append(index_0)
                    
                    #loop block end
                    index_0=index_0 + 1
                #loop ended
                break
            
            #loop block end
            index_0=index_0 + 1
        #loop ended
        
    index_0=(4,2,0).index(channel.ORDER_GROUP)
    before=(4,2,0)[index_0:]
    after =(4,2,0)[:index_0 + 1]

    possible_indexes=[]
    if restricted_positions:
        #loop prepare
        index_0=0
        limit_0=len(restricted_positions) - 1
        info_line=ordered[restricted_positions[index_0]]
        #loop at 0 block start
        
        if info_line[3].ORDER_GROUP in after:
            possible_indexes.append((0,restricted_positions[index_0],),)
            
        #loop at 0 block ended
        while True:
            if index_0==limit_0:
                break
            info_line=ordered[restricted_positions[index_0]]
            #next step mixin
            index_0=index_0 + 1
            info_line_2=ordered[restricted_positions[index_0]]
            #loop block start

            if info_line[3].ORDER_GROUP in before and info_line_2[3].ORDER_GROUP in after:
                possible_indexes.append((index_0,restricted_positions[index_0],),)

            #loop block end
        if limit_0:
            info_line=info_line_2
        #loop at -1 block start
        
        if info_line[3].ORDER_GROUP in before:
            possible_indexes.append((index_0 + 1,restricted_positions[index_0]+1,),)

        #loop at -1 block ended
        #loop ended
    else:
        #empty category
        possible_indexes.append((0,category_index + 1,),)
        
    #GOTO start
    while True:
        #GOTO block start
        
        #loop prepare
        index_0=0
        limit_0=len(possible_indexes)
        info_line=possible_indexes[index_0]
        
        #loop at 0 block start
        if info_line[0]>visual_position:
            result_position=info_line[1]
            
            #GOTO end
            break
            #GOTO ended
        
        #loop at 0 block ended
        
        #setup GOTO from loop start
        end_goto=False
        #setup GOTO from loop ended
        
        index_0=index_0 + 1
        while True:
            if index_0==limit_0:
                break
            info_line=possible_indexes[index_0]
            #loop block start

            if info_line[0]==visual_position:
                result_position=info_line[1]
                
                #GOTO end inner 1
                end_goto=True
                break
                #GOTO ended inner 1

            #loop block end
            index_0=index_0 + 1
        #loop ended

        #GOTO end
        if end_goto:
            break
        #GOTO ended

        result_position=info_line[1]

        #GOTO block ended
        break
    #GOTO ended
    
    ordered.insert(result_position,ordered[original_position])
    higher_flag=(result_position<original_position)
    if higher_flag:
        original_position=original_position + 1
    else:
        result_position=result_position - 1
    del ordered[original_position]
    
    if channel.type==4:
        channels_to_move=[]

        #loop prepare
        index_0=original_position
        limit_0=len(ordered)
        #loop start
        while True:
            if index_0==limit_0:
                break
            info_line=ordered[index_0]
            #loop block start

            if info_line[3].type==4:
                break
            channels_to_move.append(info_line)
            
            #loop block end
            index_0=index_0 + 1
        #loop ended

        insert_to=result_position + 1
        
        #loop prepare
        index_0=len(channels_to_move)
        limit_0=0
        #loop start
        while True:
            index_0=index_0 - 1
            info_line=channels_to_move[index_0]
            #loop block start
            
            ordered.insert(insert_to,info_line)
            
            #loop block end
            if index_0==limit_0:
                break
        #loop ended

        delete_from=original_position
        if higher_flag:
            delete_from=delete_from + len(channels_to_move) #len(channels_to_move)

        #loop prepare
        index_0=0
        limit_0=len(channels_to_move)
        #loop start
        while True:
            if index_0==limit_0:
                break
            info_line=ordered[index_0]
            #loop block start

            del ordered[delete_from]
            
            #loop block end
            index_0=index_0 + 1
        #loop ended
        
    indexes[0]=indexes[2]=indexes[4]=indexes[5]=indexes[6]=0 #reset

    #loop preparations
    index_0=0
    limit_0=len(ordered)
    #loop start
    while True:
        if index_0==limit_0:
            break
        channel_=ordered[index_0][3]
        #loop block start
        
        type_=channel_.type
        type_index=indexes[type_]
        indexes[type_]=type_index + 1
        
        ordered[index_0]=(type_index,channel_)

        #loop block step
        index_0=index_0 + 1
        #loop block continue
        
        if type_==4:
            #reset type_indexes
            indexes[0]=indexes[2]=indexes[5]=indexes[6]=0
            #loop preparations
            #loop start
            while True:
                if index_0==limit_0:
                    break
                channel_=ordered[index_0][3]
                #loop block start
                
                type_=channel_.type
                if type_ == 4:
                    break
                type_index = indexes[type_]
                indexes[type_] = type_index + 1

                ordered[index_0] = (type_index, channel_)
                
                #loop block end
                index_0 = index_0 + 1
            
        #loop block end
    #loop ended

    bonus_data = {'lock_permissions':lock_permissions}
    if category is guild:
        bonus_data['parent_id'] = None
    else:
        bonus_data['parent_id'] = category.id
    
    data=[]
    for position,channel_ in ordered:
        if channel is channel_:
            data.append({'id': channel_.id, 'position':position, **bonus_data})
            continue
        if channel_.position != position:
            data.append({'id': channel_.id,'position': position})
    
    guild_id = guild.id
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/channels',data,
        )

async def channel_create(client, guild, name, category=None, type_=0):
    data=cr_pg_channel_object(type_=type_,name=name)
    data['parent_id']=category.id if type(category) is ChannelCategory else None
    guild_id=guild.id
    data = await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/guilds/{guild_id}/channels',
        data,)
    return CHANNEL_TYPE_MAP.get(data['type'], ChannelGuildUndefined)(data, client, guild_id)

async def emoji_guild_get_all(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/emojis',
        )

async def emoji_create(client, guild, name, image,):
    image=image_to_base64(image)
    name=''.join(re.findall('([0-9A-Za-z_]+)',name))
    if not (1<len(name)<33):
        raise ValueError(f'The length of the name can be between 2-32, got {len(name)}')
    
    data = {
        'name'      : name,
        'image'     : image,
        'role_ids'  : []
            }
        
    guild_id=guild.id
    data = await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/guilds/{guild_id}/emojis',
        data,)
    
    return Emoji(data, guild)

async def emoji_get(client, emoji):
    guild = emoji.guild
    if guild is None:
        return
    guild_id=guild.id
    emoji_id = emoji.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',
        )

async def emoji_delete(client, emoji,):
    guild_id = emoji.guild.id
    emoji_id = emoji.id
    return await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',
        )

async def emoji_edit(client,emoji,name,): #keep it short
    data = {'name':name}
    guild_id = emoji.guild.id
    emoji_id = emoji.id
    return await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/emojis/{emoji_id}',
        data,)

async def integration_get_all(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/integrations',
        )

async def invite_get_all_guild(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/invites',
        )

async def guild_user_delete(client, guild, user,):
    guild_id = guild.id
    user_id = user.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
        )

async def user_edit(client, guild,user,nick,mute=False,):
    guild_id=guild.id
    user_id=user.id
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
        data={'nick':nick,'mute':mute},)

async def guild_user_add(client, guild,user,):
    guild_id=guild.id
    user_id=user.id
    return await bypass_request(client,METHOD_PUT,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
        data={'access_token':user.access.access_token},)

async def user_role_add(client,user,role,):
    guild_id=role.guild.id
    user_id=user.id
    role_id=role.id
    return await bypass_request(client,METHOD_PUT,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
        )

async def user_role_delete(client,user,role,):
    guild_id=role.guild.id
    user_id=user.id
    role_id=role.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}/roles/{role_id}',
        )

async def guild_prune(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/guilds/{guild_id}/prune',
        params={'days':30},)

async def guild_prune_estimate(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/prune',
        params={'days':30},)

async def role_create(client, guild,name=None,permissions=None,color=None,
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
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/guilds/{guild_id}/roles',
        data=data,)

async def role_move(client,role,new_position,):
    guild = role.guild
    data= change_on_switch(guild.role_list, role, new_position, key=role_move_key)
    guild_id=role.guild.id
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/roles',
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
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',
        data=data,)

async def role_delete(client,role,):
    guild_id=role.guild.id
    role_id=role.id
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/roles/{role_id}',
        )


async def webhook_get_all_guild(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/webhooks',
        )

async def guild_widget_image(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.png',
        params={'style':'shield'},decode=False,headers={},)

async def invite_get(client,invite,):
    invite_code=invite.code
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/invites/{invite_code}',
        )

async def invite_delete(client,invite,):
    invite_code=invite.code
    return await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/invites/{invite_code}',
        )

async def user_info_get(client,access,):
    headers=IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION]=f'Bearer {access.access_token}'
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me',
        headers=headers,)

async def client_user_get(client,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me',
        )

async def channel_private_get_all(client,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me/channels',
        )

async def channel_private_create(client,user,):
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/users/@me/channels',
        data={'recipient_id':user.id},)

async def user_connection_get_all(client,access,):
    headers=IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION]=f'Bearer {access.access_token}'
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me/connections',
        headers=headers,)

async def user_guild_get_all(client,access,):
    headers=IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION]=f'Bearer {access.access_token}'
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me/guilds',
        headers=headers,)

async def guild_get_all(client,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me/guilds',
        params={'after':0},)

async def user_get(client,user,):
    user_id=user.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/{user_id}',
        )

async def webhook_get(client,webhook,):
    webhook_id=webhook.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/webhooks/{webhook_id}',
        )

async def webhook_delete(client,webhook,):
    webhook_id=webhook.id
    return  bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/webhooks/{webhook_id}',
        )

async def webhook_edit(client,webhook,name,): #keep it short
    webhook_id=webhook.id
    return await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/webhooks/{webhook_id}',
        data={'name':name},)

async def webhook_get_token(client,webhook,):
    return await bypass_request(client,METHOD_GET,
        webhook.url,headers={},)

async def webhook_delete_token(client,webhook,):
    return await bypass_request(client,METHOD_DELETE,
        webhook.url,headers={},)

async def webhook_edit_token(client,webhook,name,): #keep it short
    return await bypass_request(client,METHOD_PATCH,
        webhook.url,
        data={'name':name},headers={},)

async def webhook_execute(client, webhook, content,):
    data = await bypass_request(client,METHOD_POST,
        f'{webhook.url}?wait=1',
        data={'content':content}, headers={},)
    
    channel = webhook.channel
    if channel is None:
        channel = ChannelText.precreate(int(data['channel_id']))
    
    return channel._create_new_message(data)

async def webhook_message_edit(client, webhook, message, content):
    return await bypass_request(client, METHOD_PATCH,
        f'{webhook.url}/messages/{message.id}',
        data={'content':content}, headers={},)

async def webhook_message_delete(client, webhook, message):
    return await bypass_request(client, METHOD_DELETE,
        f'{webhook.url}/messages/{message.id}',
        headers={},)

async def webhook_message_get(client, webhook, message_id):
    return await bypass_request(client, METHOD_GET,
        f'{webhook.url}/messages/{message_id}',
        headers={},)

async def guild_user_get_chunk(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/members',
        )

async def guild_voice_region_get_all(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/regions',
        )

async def guild_channels(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/channels',
        )

async def guild_role_get_all(client, guild,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/roles',
        )

async def guild_user_get(client, guild,user_id,):
    guild_id=guild.id
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/{user_id}',
        )

async def guild_user_search(client, guild, query, limit=1):
    data = {'query': query}
    
    if limit == 1:
        # default limit is `1`, so not needed to send it.
        pass
    elif limit < 1000 and limit > 0:
        data['limit'] = limit
    else:
        raise ValueError('`limit` can be between 1 and 1000, got `{limit}`')
    
    guild_id=guild.id
    return await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/members/search', params = data,
            )

async def guild_widget_get(client, guild_id,):
    return await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/widget.json',
        headers={},)

async def message_suppress_embeds(client,message,suppress=True,):
    message_id=message.id
    channel_id=message.channel.id
    return await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/suppress-embeds',
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
    
    data = await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/followers',
        data,)
    webhook = await Webhook._from_follow_data(data, source_channel, target_channel, client)
    return webhook

async def achievement_get(client,achievement_id,):
    application_id=client.application.id
        
    data = await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',
        )
    
    return Achievement(data)
    

async def achievement_create(client,name,description,icon,secret=False,secure=False,):
    icon_data=image_to_base64(icon)
    
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
        
    data =  await bypass_request(client,METHOD_POST,
        f'{API_ENDPOINT}/applications/{application_id}/achievements',
        data=data,)
    
    return Achievement(data)

async def achievement_delete(client,achievement,):
    application_id=client.application.id
    achievement_id=achievement.id
    await bypass_request(client,METHOD_DELETE,
        f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',
        )

async def achievement_edit(client,achievement,name=None,description=None,secret=None,secure=None,icon=...,):
    data={}
    if (name is not None):
        data['name'] = {
            'default': name,
        }
    if (description is not None):
        data['description'] = {
            'default': description,
        }
    if (secret is not None):
        data['secret'] = secret
        
    if (secure is not None):
        data['secure'] = secure
        
    if (icon is not ...):
        data['icon'] = image_to_base64(icon)
    
    application_id=client.application.id
    achievement_id=achievement.id
    
    data = await bypass_request(client,METHOD_PATCH,
        f'{API_ENDPOINT}/applications/{application_id}/achievements/{achievement_id}',
        data=data,)

    achievement._update_attributes(data)
    return achievement

async def achievement_get_all(client,):
    application_id=client.application.id
    
    data = await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/achievements',
    )
    
    return [Achievement(achievement_data) for achievement_data in data]

async def user_achievement_update(client,user,achievement,percent_complete,):
    data={'percent_complete':percent_complete}
    
    user_id=user.id
    application_id=client.application.id
    achievement_id=achievement.id
    
    await bypass_request(client,METHOD_PUT,
        f'{API_ENDPOINT}/users/{user_id}/applications/{application_id}/achievements/{achievement_id}',
        data=data,)

async def user_achievements(client,access,):
    headers=IgnoreCaseMultiValueDictionary()
    headers[AUTHORIZATION]=f'Bearer {access.access_token}'
    
    application_id=client.application.id
    
    data = await bypass_request(client,METHOD_GET,
        f'{API_ENDPOINT}/users/@me/applications/{application_id}/achievements',
        headers=headers,)
    
    return [Achievement(achievement_data) for achievement_data in data]

async def reaction_delete_emoji(client, message, emoji):
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{message.channel.id}/messages/{message.id}/reactions/{emoji.as_reaction}')

async def guild_preview_get(client, guild_id):
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/preview')

async def message_crosspost(client, message):
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/channels/{message.channel.id}/messages/{message.id}/crosspost')

async def vanity_invite_get(client, guild):
    guild_id = guild.id
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url')

async def guild_discovery_get(client, guild):
    guild_id = guild.id
    guild_discovery_data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata')
    return GuildDiscovery(guild_discovery_data, guild)

async def guild_discovery_edit(client, guild, primary_category_id=..., keywords=...,
            emoji_discovery=...):
    
    guild_id = guild.id
    data = {}
    if (primary_category_id is not ...):
        data['primary_category_id'] = primary_category_id
    
    if (keywords is not ...):
        data['keywords'] = keywords
    
    if (emoji_discovery is not ...):
        data['emoji_discoverability_enabled'] = emoji_discovery
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/discovery-metadata',
        data=data)

async def guild_discovery_add_subcategory(client, guild, category_id):
    guild_id = guild.id
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}')

async def guild_discovery_delete_subcategory(client, guild, category_id):
    guild_id = guild.id
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/discovery-categories/{category_id}')

async def discovery_category_get_all(client):
    discovery_category_datas = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/discovery/categories')
    return [DiscoveryCategory(discovery_category_data) for discovery_category_data in discovery_category_datas]

async def discovery_validate_term(client, term):
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/discovery/valid-term',
        params={'term': term})
    
    return data['valid']

async def applications_detectable(client):
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/applications/detectable',
    )

async def welcome_screen_get(client, guild_id):
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/welcome-screen',
    )

async def eula_get(client):
    eula_id = 542074049984200704
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/store/eulas/{eula_id}',
    )

async def voice_regions(client):
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/voice/regions',
    )
    return data


async def application_command_global_get_all(client):
    application_id = client.application.id
    
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/commands',
            )
    
    return [ApplicationCommand.from_data(application_command_data) for application_command_data in data]

async def application_command_global_create(client, application_command):
    application_id = client.application.id
    data = application_command.to_data()
    
    data = await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/applications/{application_id}/commands',
        data)
    
    return ApplicationCommand.from_data(data)

async def application_command_global_edit(client, old_application_command, new_application_command):
    application_command_id = old_application_command.id
    application_id = client.application.id
    data = new_application_command.to_data()
    
    data = await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}',
        data)
    
    return ApplicationCommand.from_data(data)

async def application_command_global_delete(client, application_command):
    application_command_id = application_command.id
    application_id = client.application.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}',
            )

async def application_command_guild_get_all(client, guild):
    application_id = client.application.id
    guild_id = guild.id
    
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands',
            )
    
    return [ApplicationCommand.from_data(application_command_data) for application_command_data in data]

async def application_command_guild_create(client, guild, application_command):
    application_id = client.application.id
    guild_id = guild.id
    data = application_command.to_data()
    
    data = await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands',
        data)
    
    return ApplicationCommand.from_data(data)

async def application_command_guild_edit(client, guild, old_application_command, new_application_command):
    application_command_id = old_application_command.id
    application_id = client.application.id
    guild_id = guild.id
    data = new_application_command.to_data()
    
    data = await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}',
        data)
    
    return ApplicationCommand.from_data(data)

async def application_command_guild_delete(client, guild, application_command):
    application_command_id = application_command.id
    application_id = client.application.id
    guild_id = guild.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}',
    )

async def interaction_response_message_create(client, interaction, content=None, embed=None):
    message_data = {}
    contains_content = False
    
    if (content is not None):
        message_data['content'] = content
        contains_content = True
    
    if (embed is not None):
        message_data['embeds'] = [embed.to_data()]
        contains_content = True
    
    data = {}
    if contains_content:
        data['data'] = message_data
        
        response_type = INTERACTION_RESPONSE_TYPES.message_and_source
    else:
        response_type = INTERACTION_RESPONSE_TYPES.source
    
    data['type'] = response_type
    
    interaction_id = interaction.id
    interaction_token = interaction.token
    
    data = await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/interactions/{interaction_id}/{interaction_token}/callback',
        data)
    
    return None

async def interaction_response_message_edit(client, interaction, content=None, embed=None):
    message_data = {}
    
    if (content is not None):
        message_data['content'] = content
    
    if (embed is not None):
        message_data['embeds'] = embed.to_data()
    
    application_id = client.application.id
    interaction_token = interaction.token
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original',
        message_data)

async def interaction_response_message_delete(client, interaction):
    application_id = client.application.id
    interaction_token = interaction.token
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original',
    )

    
async def interaction_response_message_get(client, interaction):
    application_id = client.application.id
    interaction_token = interaction.token
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/@original',
    )

async def interaction_followup_message_create(client, interaction, content=None, embed=None):
    message_data = {}
    
    if (content is not None):
        message_data['content'] = content
    
    if (embed is not None):
        message_data['embeds'] = [embed.to_data()]
    
    application_id = client.application.id
    interaction_token = interaction.token
    
    data = await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}',
        message_data, headers={})
    
    return interaction.channel._create_new_message(data)

async def interaction_followup_message_edit(client, interaction, message, content=None, embed=None):
    message_data = {}
    
    if (content is not None):
        message_data['content'] = content
    
    if (embed is not None):
        message_data['embeds'] = embed.to_data()
    
    application_id = client.application.id
    interaction_token = interaction.token
    message_id = message.id
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}',
        message_data)
    
async def interaction_followup_message_delete(client, interaction, message):
    application_id = client.application.id
    interaction_token = interaction.token
    message_id = message.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}',
    )


async def interaction_followup_message_get(client, interaction, message):
    application_id = client.application.id
    interaction_token = interaction.token
    message_id = message.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/webhooks/{application_id}/{interaction_token}/messages/{message_id}',
    )


async def verification_screen_get(client, guild):
    guild_id = guild.id
    
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/member-verification',
    )
    
    return VerificationScreen.from_data(data)

async def verification_screen_edit(client, guild):
    guild_id = guild.id
    data = {'enabled': True}

    data = await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/member-verification',
        data)
    
    return VerificationScreen.from_data(data)

async def welcome_screen_edit(client, guild):
    guild_id = guild.id
    data = {'enabled': True}
    
    data = await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/welcome-screen',
        data)
    
    return WelcomeScreen.from_data(data)

async def application_command_global_get(client, application_command_id):
    application_id = client.application.id
    
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/commands/{application_command_id}',
    )
    
    return ApplicationCommand.from_data(data)

async def application_command_guild_get(client, guild, application_command_id):
    application_id = client.application.id
    guild_id = guild.id
    
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}',
    )
    
    return ApplicationCommand.from_data(data)

async def application_command_global_update_multiple(client, application_commands):
    application_id = client.application.id
    application_command_datas = [application_command.to_data() for application_command in application_commands]
    
    application_command_datas = await bypass_request(client, METHOD_PUT,
        f'{API_ENDPOINT}/applications/{application_id}/commands',
        application_command_datas,
    )
    
    return [ApplicationCommand.from_data(application_command_data) \
        for application_command_data in application_command_datas]

async def application_command_guild_update_multiple(client, guild, application_commands):
    application_id = client.application.id
    guild_id = guild.id
    application_command_datas = [application_command.to_data() for application_command in application_commands]
    
    application_command_datas = await bypass_request(client, METHOD_PUT,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands',
        application_command_datas,
    )
    
    return [ApplicationCommand.from_data(application_command_data) \
        for application_command_data in application_command_datas]


async def application_command_permission_get_all_guild(client, guild):
    application_id = client.application.id
    guild_id = guild.id
    permission_datas = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/permissions',
    )
    
    return [ApplicationCommandPermission.from_data(permission_data) for permission_data in permission_datas]

async def application_command_permission_get(client, guild, application_command):
    application_id = client.application.id
    guild_id = guild.id
    application_command_id = application_command.id
    permission_data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}/permissions',
    )
    
    return ApplicationCommandPermission.from_data(permission_data)

async def application_command_permission_edit(client, guild, application_command, overwrites):
    application_id = client.application.id
    guild_id = guild.id
    application_command_id = application_command.id
    
    data = {'permissions': [overwrite.to_data() for overwrite in overwrites]}
    
    await bypass_request(client, METHOD_PUT,
        f'{API_ENDPOINT}/applications/{application_id}/guilds/{guild_id}/commands/{application_command_id}/permissions',
        data)

async def voice_state_client_edit(client, channel, suppress=False, request_to_speak=False):
    channel_id = channel.id
    guild_id = channel.guild.id
    
    if request_to_speak:
        request_to_speak_timestamp = datetime.utcnow().isoformat()
    else:
        request_to_speak_timestamp = None
    
    data = {
        'suppress': suppress,
        'request_to_speak_timestamp': request_to_speak_timestamp,
        'channel_id': channel_id,
    }
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/voice-states/@me',
        data)

async def voice_state_user_edit(client, channel, user, suppress=False):
    channel_id = channel.id
    guild_id = channel.guild.id
    user_id = user.id
    
    data = {
        'suppress': suppress,
        'channel_id': channel_id,
    }
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/voice-states/{user_id}',
        data)


async def stage_discovery_get(client):
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/discovery',
    )

async def guild_discovery_get_all(client):
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guild-discovery',
    )

async def stage_get_all(client):
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/stage-instances',
    )

async def stage_create(client, channel, topic):
    data = {
        'channel_id': channel.id,
        'topic': topic,
        'privacy_level': PrivacyLevel.guild_only.value
    }
    
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/stage-instances',
        data)

async def stage_edit(client, channel, topic):
    channel_id = channel.id
    
    data = {
        'topic': topic,
    }
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/stage-instances/{channel_id}',
        data)


async def stage_get(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/stage-instances/{channel_id}',
    )


async def stage_delete(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/stage-instances/{channel_id}',
        )

async def thread_create(client, channel, type_, name):
    channel_id = channel.id
    data = {
        'name': name,
        'type': type_,
    }
    
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/threads',
        data,
    )

async def thread_create_from_message(client, message, type_, name):
    channel_id = message.channel.id
    message_id = message.id
    data = {
        'name': name,
        'type': type_,
    }
    
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/messages/{message_id}/threads',
        data,
    )

async def thread_join(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members/@me',
    )

async def application_button_create(client, data):
    application_id = client.application.id

    return await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/applications/{application_id}/message-components',
        data,
    )

async def thread_leave(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members/@me',
    )


async def thread_get_self(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members/@me',
    )


async def thread_user_get(client, channel, user):
    channel_id = channel.id
    user_id = user.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members/{user_id}',
    )


async def thread_user_add(client, channel, user):
    channel_id = channel.id
    user_id = user.id
    
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members/{user_id}',
    )


async def thread_user_delete(client, channel, user):
    channel_id = channel.id
    user_id = user.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members/{user_id}',
    )


async def thread_self_settings_edit(client, channel, data):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members/@me/settings',
        data,
    )


async def channel_thread_get_chunk_archived_public(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/threads/archived/public'
    )


async def channel_thread_get_chunk_archived_private(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/threads/archived/private'
    )


async def channel_thread_get_chunk_self_archived(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/users/@me/threads/archived/private'
    )


async def channel_thread_get_chunk_active(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/threads/active'
    )


async def thread_user_get_all(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/thread-members'
    )


async def servers_get(client):
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/servers'
    )


async def sticker_guild_get_all(client, guild):
    guild_id = guild.id
    sticker_datas = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/stickers'
    )
    
    return [Sticker(sticker_data) for sticker_data in sticker_datas]


async def sticker_pack_get_all(client):
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/sticker-packs'
    )
    
    sticker_pack_datas = data['sticker_packs']
    
    return [StickerPack(sticker_pack_data) for sticker_pack_data in sticker_pack_datas]


async def sticker_pack_get(client, sticker_pack_id):
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/sticker-packs/{sticker_pack_id}'
    )
    
    return StickerPack(data)


async def sticker_guild_get(client, guild, sticker_id):
    guild_id = guild.id
    
    sticker_data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/stickers/{sticker_id}'
    )
    
    return Sticker(sticker_data)

async def sticker_guild_create(client, guild, name, description, file, tags):
    form = Formdata()
    form.add_field('name', name)
    form.add_field('description', description)
    form.add_field('tags', ', '.join(tags))
    form.add_field('file', file, filename='file.png', content_type='image/png')
    
    guild_id = guild.id
    
    sticker_data = await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/guilds/{guild_id}/stickers',
        form,
    )
    
    return Sticker(sticker_data)


async def sticker_guild_delete(client, guild, sticker_id):
    guild_id = guild.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/stickers/{sticker_id}'
    )


async def sticker_get(client, sticker_id):
    sticker_data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/stickers/{sticker_id}'
    )
    
    return Sticker(sticker_data)


async def sticker_guild_edit(client, guild, sticker, name=None, description=None, tags=None):
    if tags is None:
        tags = ', '.join(sticker.tags)
    else:
        tags = ', '.join(tags)
    
    if name is None:
        name = sticker.name
    
    if description is None:
        description = sticker.description
    
    
    data = {
        'name': name,
        'description': description,
        'tags': tags,
    }
    
    guild_id = guild.id
    sticker_id = sticker.id
    
    sticker_data = await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/stickers/{sticker_id}',
        data
    )


async def vanity_invite_edit(client, guild, vanity_code=None):
    guild_id = guild.id
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/vanity-url',
        {'code': vanity_code}
    )

async def status_incident_unresolved(client):
    await bypass_request(client, METHOD_GET,
        f'{STATUS_ENDPOINT}/incidents/unresolved.json',
        headers = IgnoreCaseMultiValueDictionary(),
    )

async def status_maintenance_active(client):
    await bypass_request(client, METHOD_GET,
        f'{STATUS_ENDPOINT}/scheduled-maintenances/active.json',
        headers = IgnoreCaseMultiValueDictionary(),
    )

async def status_maintenance_upcoming(client):
    await bypass_request(client, METHOD_GET,
        f'{STATUS_ENDPOINT}/scheduled-maintenances/upcoming.json',
        headers = IgnoreCaseMultiValueDictionary(),
    )


async def greet(client, channel):
    channel_id = channel.id
    sticker_id = 749054660769218631
    
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/channels/{channel_id}/greet',
        {'sticker_ids': [sticker_id]}
    )
    

async def channel_directory_search(client, channel, query):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/directory-entries/search',
        {'query': query}
    )

async def channel_directory_counts(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/directory-entries/counts',
    )

async def channel_directory_get_all(client, channel):
    channel_id = channel.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/channels/{channel_id}/directory-entries/list',
    )


async def guild_thread_get_all_active(client, guild):
    guild_id = guild.id
    
    await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/threads/active',
    )


async def scheduled_event_get_all_guild(client, guild):
    guild_id = guild.id
    
    return await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events',
    )


async def scheduled_event_create(client, guild, voice, name):
    guild_id = guild.id
    
    data = {
        'name' : name,
        'privacy_level': PrivacyLevel.guild_only.value,
        'channel_id': voice.id,
        'entity_metadata': None,
        'entity_type': ScheduledEventEntityType.voice.value,
        'scheduled_start_time': datetime_to_timestamp(datetime.utcnow() + timedelta(hours=1)),
    }
    
    await bypass_request(client, METHOD_POST,
        f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events',
        data,
    )


async def scheduled_event_get(client, guild, scheduled_event_id):
    guild_id = guild.id
    
    return await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}',
    )


async def scheduled_event_edit(client, scheduled_event, name):
    guild_id = scheduled_event.guild_id
    scheduled_event_id = scheduled_event.id
    
    data = {
        'name' : name,
    }
    
    await bypass_request(client, METHOD_PATCH,
        f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}',
        data,
    )


async def scheduled_event_delete(client, scheduled_event):
    guild_id = scheduled_event.guild_id
    scheduled_event_id = scheduled_event.id
    
    await bypass_request(client, METHOD_DELETE,
        f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}',
    )


async def scheduled_event_user_get_chunk(client, scheduled_event):
    guild_id = scheduled_event.guild_id
    scheduled_event_id = scheduled_event.id
    
    data = await bypass_request(client, METHOD_GET,
        f'{API_ENDPOINT}/guilds/{guild_id}/scheduled-events/{scheduled_event_id}/users',
    )


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0000(client, message):
    """
    Does 6 achievement get request towards 1 achievement.
    The bot's application must have at least 1 achievement created.
    """
    with RLTCTX(client, message.channel, 'rate_limit_test_0000') as RLT:
        try:
            achievements = await client.achievement_get_all()
        except BaseException as err:
            await RLT.send(repr(err))
        
        if not achievements:
            await RLT.send(repr('The application has no achievement'))
        
        achievement = achievements[0]
        achievement_id = achievement.id
        
        tasks = []
        for _ in range(6):
            task = Task(achievement_get(client, achievement_id), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
    #achievement_get limited. limit:5, reset:5
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0001(client,message):
    """
    Does 3-3 achievement get request towards 2 achievement.
    The bot's application must have at least 2 achievement created.
    """
    with RLTCTX(client,message.channel, 'rate_limit_test_0001') as RLT:
        try:
            achievements = await client.achievement_get_all()
        except BaseException as err:
            await RLT.send(repr(err))
        
        if len(achievements)<3:
            await RLT.send(repr('The application has less than 2 achievements'))
        
        achievement_1 = achievements[0]
        achievement_2 = achievements[1]
        
        achievement_id_1 = achievement_1.id
        achievement_id_2 = achievement_2.id
        
        tasks = []
        for _ in range(4):
            task = Task(achievement_get(client,achievement_id_1), KOKORO)
            tasks.append(task)
            
            task = Task(achievement_get(client,achievement_id_2), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
    #achievement_get limited globally
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0002(client,message):
    """
    Creates 6 achievements.
    """
    with RLTCTX(client, message.channel, 'rate_limit_test_0002') as RLT:
        image_path = join(os.path.abspath(''), 'images', '0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        tasks = []
        names = ('Yura','Hana','Neko','Kaze','Scarlet','Yukari')
        for name in names:
            description = name+'boroshi'
            task = Task(achievement_create(client,name,description,image), KOKORO)
            tasks.append(task)
            
        await WaitTillAll(tasks, KOKORO)
        
        for task in tasks:
            try:
                achievement = task.result()
            except:
                pass
            else:
                await client.achievement_delete(achievement.id)
    #achievement_create limited. limit:5, reset:5, globally
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0003(client,message):
    """
    First creates 2 achievements with the client normally, then deletes them for testing.
    """
    with RLTCTX(client,message.channel, 'rate_limit_test_0003') as RLT:
        image_path = join(os.path.abspath(''), 'images', '0000000C_touhou_komeiji_koishi.png')
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

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0004(client,message):
    """
    Creates an achievement, then edits it twice for testing. When done, deletes it.
    """
    
    with RLTCTX(client,message.channel,'rate_limit_test_0004') as RLT:
        image_path = join(os.path.abspath(''), 'images', '0000000C_touhou_komeiji_koishi.png')
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
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0005(client,message):
    """
    Creates 2 achievements, then edits them once, once for testing. At the end deletes them.
    """
    with RLTCTX(client,message.channel,'rate_limit_test_0005') as RLT:
        image_path=join(os.path.abspath(''),'images','0000000C_touhou_komeiji_koishi.png')
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

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0006(client,message):
    """
    Creates, edits and deletes an achievement.
    """
    
    with RLTCTX(client,message.channel,'rate_limit_test_0006') as RLT:
        image_path=join(os.path.abspath(''),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await achievement_create(client,'Kokoro','is love',image)
        await achievement_get(client,achievement.id)
        await achievement_edit(client,achievement,name='Yurika')
        await achievement_delete(client,achievement)
    
    # achievement_create, achievement_get, achievement_edit, achievement_delete are NOT grouped
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0007(client,message):
    """
    Requests all the achievements.
    """
    
    with RLTCTX(client,message.channel,'rate_limit_test_0007') as RLT:
        loop=client.loop
        tasks = []
        for _ in range(2):
            task = Task(achievement_get_all(client),loop)
            tasks.append(task)
        
        await WaitTillAll(tasks,loop)
    
    #achievement_get_all limited. limit:5, reset:5, globally

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0008(client,message):
    """
    Updates an achievement of the client's owner.
    """
    
    with RLTCTX(client,message.channel,'rate_limit_test_0008') as RLT:
        image_path=join(os.path.abspath(''),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi','Kokoro',image,secure=True)
        
        try:
            await user_achievement_update(client,client.owner,achievement,100)
        finally:
            await client.achievement_delete(achievement)
    
    # DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    # user_achievement_update limited. Limit : 5, reset : 5.
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0009(client,message):
    """
    Updates an achievement of the client's owner.
    Waits 2 seconds after the achievement is created, so it might work this time (nope).
    """
    with RLTCTX(client,message.channel,'rate_limit_test_0009') as RLT:
        image_path=join(os.path.abspath(''),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi','Kokoro',image,secure=True)
        await sleep(2.0,client.loop) # wait some time this time
        
        try:
            await user_achievement_update(client,client.owner,achievement,100)
        finally:
            await client.achievement_delete(achievement)

    # DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0010(client, message):
    """
    Updates an achievement of the client's owner. But now one, what has `secure=False`
    """
    with RLTCTX(client,message.channel,'rate_limit_test_0010') as RLT:
        image_path=join(os.path.abspath(''),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi', 'Kokoro', image) #no just a normal one
        
        try:
            await user_achievement_update(client,client.owner,achievement,100)
        finally:
            await client.achievement_delete(achievement)
    
    # DiscordException FORBIDDEN (403), code=40001: Unauthorized

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0011(client,message):
    """
    Updates the achievements of all the owners of the client.
    """
    
    with RLTCTX(client,message.channel,'rate_limit_test_0011') as RLT:
        image_path=join(os.path.abspath(''),'images','0000000C_touhou_komeiji_koishi.png')
        with (await AsyncIO(image_path)) as file:
            image = await file.read()
        
        achievement = await client.achievement_create('Koishi','Kokoro',image,secure=True)
        
        tasks = []
        for member in client.application.owner.members:
            user = member.user
            task = Task(user_achievement_update(client,user,achievement,100), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)
        await client.achievement_delete(achievement)
    
    # DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
    #limited globally

class check_is_owner:
    __slots__ = ('client', )
    def __init__(self, client):
        self.client = client
    
    def __call__(self,message):
        return self.client.is_owner(message.author)
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0012(client,message):
    """
    Tries to get a user's achievements after oauth2 authorization.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0012') as RLT:
        await client.message_create(channel, (
            'Please authorize yourself and resend the redirected url after it\n'
            'https://discordapp.com/oauth2/authorize?client_id=486565096164687885'
            '&redirect_uri=https%3A%2F%2Fgithub.com%2FHuyaneMatsu'
            '&response_type=code & scope=identify%20applications.store.update'))
        
        try:
            message = await wait_for_message(client,channel,check_is_owner(client),60.)
        except TimeoutError:
            await RLT.send('Timeout meanwhile waiting for redirect url.')
    
        Task(client.message_delete(message), KOKORO)
        try:
            result = parse_oauth2_redirect_url(message.content)
        except ValueError:
            await RLT.send('Bad redirect url.')
        
        access = await client.activate_authorization_code( * result,['identify', 'applications.store.update'])
        
        if access is None:
            await RLT.send('Too old redirect url.')
        
        await user_achievements(client,access)
    #DiscordException UNAUTHORIZED (401): 401: Unauthorized
    # no limit data provided

rate_limit_test_0013_OK       = BUILTIN_EMOJIS['ok_hand']
rate_limit_test_0013_CANCEL   = BUILTIN_EMOJIS['x']
rate_limit_test_0013_EMOJIS   = (rate_limit_test_0013_OK, rate_limit_test_0013_CANCEL)

class rate_limit_test_0013_checker:
    __slots__ = ('client',)
    
    def __init__(self, client):
        self.client = client
    
    def __call__(self, event):
        if not self.client.is_owner(event.user):
            return False
        
        if event.emoji not in rate_limit_test_0013_EMOJIS:
            return False
        
        return True

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0013(client,message):
    """
    Requests messages for each day from the channel if can, then deletes them if you agree with it as well.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0013') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        target_time = int((time_now() - 40 * 86400.) * 1000.-DISCORD_EPOCH) << 22
        async for message_ in await client.message_iterator(channel):
            if message_.id > target_time:
                continue
            break
        
        now = time_now()
        time_bounds = []
        for day in range(41):
            before= int((now - (day    ) * 86400.0 + 100.0) * 1000.0 - DISCORD_EPOCH) << 22
            after = int((now - (day + 1) * 86400.0 - 100.0) * 1000.0 - DISCORD_EPOCH) << 22
            time_bounds.append((before,after),)
        
        messages = []
        for day in range(41):
            messages.append((None, None),)
        
        for message_ in channel.messages:
            for day,(before,after) in enumerate(time_bounds):
                if message_.id>before:
                    continue
                
                if message_.id<after:
                    continue
                
                message_own, message_other=messages[day]
                if (message_own is not None) and (message_other is not None):
                    break
                
                if message_.author == client:
                    if message_own is None:
                        messages[day] = (message_, message_other)
                else:
                    if message_other is None:
                        messages[day] = (message_own, message_)
                
                break
        
        result=['```\nday | own | other\n']
        for day,(message_own, message_other) in enumerate(messages):
            result.append(f'{day:>3} | {("YES", "NO")[message_own is None]} | {("YES", "NO")[message_other is None]}\n')
        result.append('```\nShould we start?')
        embed=Embed('Found messages',''.join(result))
        
        message = await client.message_create(channel,embed=embed)
        
        for emoji in rate_limit_test_0013_EMOJIS:
            await client.reaction_add(message,emoji)
        
        try:
            event = await wait_for_reaction(client, message, rate_limit_test_0013_checker(client), 40.)
        except TimeoutError:
            emoji = rate_limit_test_0013_CANCEL
        else:
            emoji = event.emoji
        
        await client.reaction_clear(message)
        
        if emoji is rate_limit_test_0013_CANCEL:
            embed.add_footer('rate_limit_test_0020 cancelled')
            await client.message_edit(message,embed=embed)
            raise CancelledError()
        
        if emoji is rate_limit_test_0013_OK:
            for day,(message_own, message_other) in enumerate(messages):
                if (message_own is not None):
                    RLT.write(f'day {day}, own:')
                    await Task(message_delete(client, message_own), KOKORO)
                
                if (message_other is not None):
                    RLT.write(f'day {day}, other:')
                    await Task(message_delete(client, message_other), KOKORO)
            
            return
            
        # no more case
        
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0014(client,message):
    """
    Creates 2 message.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0014') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
            
        messages=[]
        for index in range(2):
            message_ = await client.message_create(channel,f'testing rate_limit: message {index}')
            messages.append(message_)
        
        await Task(message_delete_multiple(client,messages),client.loop)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0015(client,message):
    """
    Deletes all the reactions of a single emoji from a message.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0015') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        emoji = BUILTIN_EMOJIS['x']
        await reaction_delete_emoji(client, message, emoji)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0016(client, message):
    """
    Adds a reaction and deletes all the same type from the message.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0016') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        emoji = BUILTIN_EMOJIS['x']
        await reaction_add(client, message, emoji)
        await reaction_delete_emoji(client, message, emoji)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0017(client,message):
    """
    Requests 1 guild preview.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0017') as RLT:
        await guild_preview_get(client, 197038439483310086)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0018(client,message):
    """
    Requests 2 guild preview.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0018') as RLT:
        await guild_preview_get(client, 302094807046684672)
        await guild_preview_get(client, 197038439483310086)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0019(client,message):
    """
    Edits the channel twice.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0019') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        nsfw=channel.nsfw
        
        await channel_edit(client, channel, nsfw = (not nsfw))
        await channel_edit(client, channel, nsfw = nsfw)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0020(client,message):
    """
    Creates a channel.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0020') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        data = await channel_create(client, guild)
        channel_id=int(data['id'])
        await client.http.channel_delete(channel_id,None)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0021(client,message):
    """
    Deletes a channel.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0021') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        channel = await client.channel_create(guild, name='Kanako', type_=0)
        await channel_delete(client, channel)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0022(client,message):
    """
    Edits a role.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0022') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        role = await client.role_create(guild,name='Sanae')
        await role_edit(client, role, name='Chiruno')
        await client.role_delete(role)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0023(client,message):
    """
    Creates a role.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0023') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        data = await role_create(client, guild, name='Yukari')
        role_id=int(data['id'])
        await client.http.role_delete(guild.id,role_id,None)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0024(client, message):
    """
    Deletes a role.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0024') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')

        top_role = client.top_role_at(guild)
        if (top_role is not None) and (top_role.position < 2):
            await RLT.send('My top role\'s position is not enough high.')
        
        role = await client.role_create(guild,name='Sakuya')
        await role_delete(client, role)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0025(client,message):
    """
    Edits 2 channel.
    """
    channel_1 = message.channel
    with RLTCTX(client,channel_1,'rate_limit_test_0025') as RLT:
        if channel_1.guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel_1.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        parent = channel_1.parent
        if parent is None:
            await RLT.send('The channel should be at a category')
        
        channel_2=None
        for channel in parent.channels:
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

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0026(client,message):
    """
    Edits 2 roles at the same guild.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0026') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        role_1 = await client.role_create(guild,name='Sanae')
        role_2 = await client.role_create(guild,name='Reimu')
        await role_edit(client, role_1, name='Chiruno')
        await role_edit(client, role_2, name='Ririi')
        await client.role_delete(role_1)
        await client.role_delete(role_2)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0027(client, message, guild_id:str=''):
    """
    Edits 1-1 roles at separate guilds.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0027') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
            
        if not guild_1.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        if not guild_2.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission at the other guild as well')
            
        role_1 = await client.role_create(guild_1,name='Sanae')
        role_2 = await client.role_create(guild_2,name='Reimu')
        await role_edit(client, role_1, name='Chiruno')
        await role_edit(client, role_2, name='Ririi')
        await client.role_delete(role_1)
        await client.role_delete(role_2)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0028(client, message, guild_id:str=''):
    """
    Creates 1-1 roles at separate guilds
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0027') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
            
        if not guild_1.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        if not guild_2.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission at the other guild as well')
            
        role_1_data = await role_create(client, guild_1, name='Yuyuko')
        role_2_data = await role_create(client, guild_2, name='Yoshika')
        role_1_id = int(role_1_data['id'])
        role_2_id = int(role_2_data['id'])
        await client.http.role_delete(guild_1.id, role_1_id, None)
        await client.http.role_delete(guild_2.id, role_2_id, None)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0029(client,message):
    """
    Moves a role.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0029') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        top_role = client.top_role_at(guild)
        if (top_role is not None) and (top_role.position < 3):
            await RLT.send('My top role\'s position is not enough high.')
        
        role = await client.role_create(guild, name='Sakuya')
        await role_move(client,role,2)
        await client.role_delete(role)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0030(client, message):
    """
    Crossposts 2 message at the current channel.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0030') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if channel.type != 5:
            await RLT.send('Pls perform this action at a news channel.')
        
        message_1 = await client.message_create(channel, 'Hatate')
        message_2 = await client.message_create(channel, 'Iku')
        
        await message_crosspost(client, message_1)
        await message_crosspost(client, message_2)
        
        await client.message_delete(message_1)
        await client.message_delete(message_2)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0031(client, message):
    """
    Crossposts 1-1 messages at 2 different channels.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0031') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if channel.type != 5:
            await RLT.send('Pls perform this action at a news channel.')
        
        parent = channel.parent
        if parent is None:
            await RLT.send('Pls perform this action at a channel within a category.')
        
        for channel_ in parent.channels:
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

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0032(client, message):
    """
    Requests a user (myself) at 2 guilds.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0032') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
            
        for guild_2_id in client.guild_profiles.keys():
            if guild_2_id == guild_1.id:
                continue
            
            break
        
        else:
            await RLT.send('I must have at least 2 guilds.')
        
        await guild_user_get(client, guild_1, client.id)
        await guild_user_get(client, GUILDS[guild_2_id], client.id)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0033(client, message):
    """
    Requests users with name `nyan` at 2 guilds.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0033') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
            
        for guild_2_id in client.guild_profiles.keys():
            if guild_2_id is guild_1.id:
                continue
            
            break
        
        else:
            await RLT.send('I must have at least 2 guilds.')
        
        await guild_user_search(client, guild_1, 'nyan')
        await guild_user_search(client, GUILDS[guild_2_id], 'nyan')

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0034(client, message):
    """
    Requests an application's owner's access.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0034') as RLT:
        for client_ in CLIENTS.values():
            if (type(client_.application.owner) is not Team) and client_.is_bot and (client_.secret is not None):
                break
        else:
            client_ = None
        
        if client_ is None:
            await RLT.send('Needs a bot client which is not owned by a team and with secret set.')
        
        await oauth2_token(client_)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0035(client, message):
    """
    Follows a channel like a boss.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0035') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
            
        for channel_ in guild.channels.values():
            if channel_.type ==5:
                source_channel = channel_
                break
        else:
            source_channel = None
        
        if source_channel is None:
            await RLT.send('The guild should have at least 1 news channel')
        
        webhooks = await client.webhook_get_all_guild(guild)
        used_channels = set()
        for webhook in webhooks:
            if webhook.type is WebhookType.server:
                used_channels.add(webhook.channel)
        
        for channel_ in guild.channels.values():
            if channel_.type not in (0,5):
                continue
            if channel_ is source_channel:
                continue
            if channel_ in used_channels:
                continue
            
            target_channel = channel_
            break
        
        else:
            target_channel = None
        
        if target_channel is None:
            await RLT.send('The guild should have at least 1 non server webhooked channel, what is not the same as '
                'the first found announcements channel.')
        
        webhook = await channel_follow(client, source_channel, target_channel)
        await client.webhook_delete(webhook)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0036(client, message):
    """
    Gets the invites of the channel
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0036') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        # I dunno what perm u need, so lets check all ^^'
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await invite_get_channel(client, channel)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0037(client, message):
    """
    Requests the messages of the channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0037') as RLT:
        if not channel.cached_permissions_for(client).can_read_message_history:
            await RLT.send('I need permission to read message history to execute this command.')
        
        await message_get_chunk(client, channel)
        
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0038(client, message):
    """
    Gets the source message.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0038') as RLT:
        await message_get(client, channel, message.id)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0039(client, message):
    """
    Requests the reactors of an emoji on the source message.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0039') as RLT:
        if not channel.cached_permissions_for(client).can_add_reactions:
            await RLT.send('I need permission to add reactions to execute this command.')
        
        emoji = BUILTIN_EMOJIS['x']
        await client.reaction_add(message, emoji)
        
        await reaction_user_get_chunk(client, message, emoji)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0040(client, message):
    """
    Removes a permission overwrite from a channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0040') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        # I dunno what perm u need, so lets check all ^^'
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        roles = guild.role_list
        if len(roles) < 2:
            await RLT.send('The guild needs at least 1 role.')
        
        role = roles[1]
        
        if not client.has_higher_role_than(role):
            await RLT.send('There is no lower role than my own for the channel.')
        
        for channel_ in guild.channels.values():
            for overwrite in channel_.permission_overwrites:
                if overwrite.target is role:
                    break
            else:
                target_channel = channel_
                break
        else:
            target_channel = channel_
        
        if target_channel is None:
            await RLT.send('Every channel has an overwrite for the bottom role.')
        
        permission_overwrite = await client.permission_overwrite_create(channel, role, 0b1000, 0b0100)
        await permission_overwrite_delete(client, channel, permission_overwrite)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0041(client, message):
    """
    Creates a permission overwrite at a channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0041') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        # I dunno what perm u need, so lets check all ^^'
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        roles = guild.role_list
        if len(roles) < 2:
            await RLT.send('The guild needs at least 1 role.')
        
        role = roles[1]
        
        if not client.has_higher_role_than(role):
            await RLT.send('There is no lower role than my own for the channel.')
        
        for channel_ in guild.channels.values():
            for overwrite in channel_.permission_overwrites:
                if overwrite.target is role:
                    break
            else:
                target_channel = channel_
                break
        else:
            target_channel = channel_
        
        if target_channel is None:
            await RLT.send('Every channel has an overwrite for the bottom role.')
        
        permission_overwrite = await permission_overwrite_create(client, target_channel, role, 0b1000, 0b0100)
        await client.permission_overwrite_delete(channel, permission_overwrite)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0042(client, message):
    """
    Gets the webhooks of the channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0042') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await webhook_get_all_channel(client, channel)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0043(client, message):
    """
    Creates a webhook at the channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0043') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        webhook = await webhook_create(client, channel, 'cake')
        await client.webhook_delete(webhook)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0044(client, message):
    """
    Gets the current guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0044') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await guild_get(client, guild.id)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0045(client, message):
    """
    Edits the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0045') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
    
        afk_channel = guild.afk_channel
        
        for channel_ in guild.channels.values():
            if type(channel_) is not ChannelVoice:
                continue
            
            if channel_ is afk_channel:
                continue
            
            target_channel = channel_
            break
        else:
            target_channel = None
        
        if afk_channel is target_channel: #both is None
            await RLT.send('The guild should have at least 1 voice channel.')

        await guild_edit(client, guild, afk_channel=target_channel)
        await client.guild_edit(guild, afk_channel=afk_channel)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0046(client, message):
    """
    Requests audit logs from the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0046') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_view_audit_log_get_chunk:
            await RLT.send('I need view audit log permission to complete this command.')
        
        await audit_log_get_chunk(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0047(client, message):
    """
    Gets the bans of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0047') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await guild_ban_get_all(client, guild)

@RATE_LIMIT_COMMANDS
@configure_converter('user', everywhere=True)
async def rate_limit_test_0048(client, message, user:'user'=None):
    """
    Bans gets the ban and un-bans the given user.
    
    Derpy, right?
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0048') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if user is None:
            await RLT.send('please pass a user as well.')
        
        if user.id in guild.users:
            await RLT.send('Please don\'t ban a member of your guild, hehe.')
        
        await guild_ban_add(client, guild, user.id)
        await guild_ban_get(client, guild, user.id)
        await guild_ban_delete(client, guild, user.id)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0049(client, message):
    """
    Gets the channels of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0049') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await guild_channels(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0050(client, message):
    """
    Moves a channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0050') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        target_channel = await client.channel_create(guild, name='tesuto_next:gen', parent=channel.parent, type_=0)
        if channel.position == 0:
            position = 1
        else:
            position = 0
        
        await channel_move(client, target_channel, position)
        
        await client.channel_delete(target_channel)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0051(client, message):
    """
    Creates a channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0051') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        created_channel = await channel_create(client, guild, name='tesuto_next:gen2', type_=0)
        
        await client.channel_delete(created_channel)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0052(client, message):
    """
    Gets the emojis of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0052') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await emoji_guild_get_all(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0053(client, message):
    """
    Gets the emojis of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0053') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        emojis = guild.emojis
        if not emojis:
            await RLT.send('The guild should have at least 1 emoji.')
        
        emoji = next(iter(emojis.values()))
        
        await emoji_get(client, emoji)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0054(client, message):
    """
    Estimates guild prune.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0054') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await guild_prune_estimate(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0055(client, message):
    """
    Guild prunes.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0055') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await guild_prune(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0056(client, message):
    """
    Gets he guild's regions.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0056') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await guild_voice_region_get_all(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0057(client, message):
    """
    Gets the guild's roles.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0057') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await guild_role_get_all(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0058(client, message):
    """
    Gets the guild's vanity code. This endpoint is not used tho.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0058') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await vanity_invite_get(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0059(client, message):
    """
    Gets the webhooks of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0059') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await webhook_get_all_guild(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0060(client, message):
    """
    Creates and deletes an invite.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0060') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        invite = await client.invite_create_preferred(guild)
        await invite_delete(client, invite)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0061(client, message):
    """
    Gets the client's application info.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0061') as RLT:
        await client_application_get(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0062(client, message):
    """
    Requests the application owner's user information.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0062') as RLT:
        for client_ in CLIENTS.values():
            if (type(client_.application.owner) is not Team) and client_.is_bot and (client_.secret is not None):
                break
        else:
            client_ = None
        
        if client_ is None:
            await RLT.send('Needs a bot client which is not owned by a team and with secret set.')
        
        access = await client_.owners_access(['email', 'bot', 'connections', 'guilds', 'identify']) # random access
        await user_info_get(client_, access)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0063(client, message):
    """
    Requests the client's profile.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0063') as RLT:
        await client_user_get(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0064(client, message):
    """
    Gets the private channels of the client.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0064') as RLT:
        await channel_private_get_all(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0065(client, message):
    """
    Gets the client's connections.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0065') as RLT:
        await client_connection_get_all(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0066(client, message):
    """
    Requests the owner's connections.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0066') as RLT:
        for client_ in CLIENTS.values():
            if (type(client_.application.owner) is not Team) and client_.is_bot and (client_.secret is not None):
                break
        else:
            client_ = None
        
        if client_ is None:
            await RLT.send('Needs a bot client which is not owned by a team and with secret set.')
        
        access = await client_.owners_access(['email', 'bot', 'connections', 'guilds', 'identify']) # random access
        await user_connection_get_all(client_, access)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0067(client, message):
    """
    Requests the owner's guilds.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0067') as RLT:
        for client_ in CLIENTS.values():
            if (type(client_.application.owner) is not Team) and client_.is_bot and (client_.secret is not None):
                break
        else:
            client_ = None
        
        if client_ is None:
            await RLT.send('Needs a bot client which is not owned by a team and with secret set.')
        
        access = await client_.owners_access(['email', 'bot', 'connections', 'guilds', 'identify']) # random access
        await user_guild_get_all(client_, access)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0068(client, message):
    """
    Requests the client's guilds.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0068') as RLT:
        await guild_get_all(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0069(client, message):
    """
    Requests the owner's and the client' guilds.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0069') as RLT:
        for client_ in CLIENTS.values():
            if (type(client_.application.owner) is not Team) and client_.is_bot and (client_.secret is not None):
                break
        else:
            client_ = None
        
        if client_ is None:
            await RLT.send('Needs a bot client which is not owned by a team and with secret set.')
        
        access = await client_.owners_access(['email', 'bot', 'connections', 'guilds', 'identify']) # random acess
        tasks = []
        loop = client.loop
        task = Task(user_guild_get_all(client_, access), loop)
        tasks.append(task)
        task = Task(guild_get_all(client), loop)
        tasks.append(task)
        
        done, pending = await WaitTillExc(tasks, loop)
        
        for task in pending:
            task.cancel()
        
        for task in done:
            task.result()

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0070(client, message):
    """
    Edits a webhook.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0070') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        webhook = await client.webhook_create(channel,name='Suzuya')
        await webhook_edit(client, webhook, 'Saki')
        await client.webhook_delete(webhook)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0071(client, message):
    """
    Edits a webhook with it's token.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0071') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        webhook = await client.webhook_create(channel, name='Suzuya')
        await webhook_edit_token(client, webhook, 'Saki')
        await client.webhook_delete(webhook)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0072(client, message):
    """
    Requests the guild's discovery object.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0072') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_manage_guild:
            await RLT.send('I need manage guild permission to complete this command.')
        
        await guild_discovery_get(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0073(client, message):
    """
    Edits the guild's discovery object.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0073') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_manage_guild:
            await RLT.send('I need manage guild permission to complete this command.')
        
        guild_discovery = await client.guild_discovery_get(guild)
        discovery = guild_discovery.emoji_discovery
        
        await guild_discovery_edit(client, guild, emoji_discovery = (not discovery))
        await client.guild_discovery_edit(guild, emoji_discovery = discovery)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0074(client, message):
    """
    Adds and deletes or deletes and adds a subcategory to the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0074') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_manage_guild:
            await RLT.send('I need manage guild permission to complete this command.')
        
        discovery_category_get_all = await client.discovery_category_get_all()
        guild_discovery = await client.guild_discovery_get(guild)
        
        actual_category_ids = guild_discovery.category_ids
        if actual_category_ids:
            remove_first = True
            id_ = next(iter(actual_category_ids))
        else:
            remove_first = False
            for category in discovery_category_get_all:
                id_ = category.id
                
                if id_ == guild_discovery.primary_category_id:
                    continue
                
                break
            else:
                await RLT.send('There are not enough category ids, lol.')
        
        if remove_first:
            actions = (guild_discovery_delete_subcategory, guild_discovery_add_subcategory)
        else:
            actions = (guild_discovery_add_subcategory, guild_discovery_delete_subcategory)
        
        for action in actions:
            await action(client, guild, id_)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0075(client, message):
    """
    Requests the discovery categories.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0075') as RLT:
        await discovery_category_get_all(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0076(client, message):
    """
    Validates a discovery search term.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0076') as RLT:
        await discovery_validate_term(client, 'gaming')

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0077(client, message):
    """
    Requests the detectable applications.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0077') as RLT:
        await applications_detectable(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0078(client, message):
    """
    Requests an eula.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0078') as RLT:
        await eula_get(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0079(client, message):
    """
    Requests the guild's welcome screen.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0079') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await welcome_screen_get(client, guild.id)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0080(client, message):
    """
    Request all the voice regions.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0080') as RLT:
        await voice_regions(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0081(client, message):
    """
    Requests integrations.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0081') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await integration_get_all(client, guild)
    
@RATE_LIMIT_COMMANDS
async def rate_limit_test_0082(client, message, name:str, emoji:'Emoji'):
    """
    Creates an emoji in 2 guilds and then deletes it. Checks emoji deletion.
    
    Please also give a name for the emoji and an emoji as well.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0082') as RLT:
        if len(client.guild_profiles) < 2:
            await RLT.send('The client should be at least in 2 guilds.')
        
        for index, guild_id in enumerate(client.guild_profiles.keys()):
            guild = GUILDS[guild_id]
            if index == 0:
                guild1 = guild
            else:
                guild2 = guild
        
        async with client.http.get(emoji.url) as response:
            emoji_data = await response.read()
        
        emoji1 = await client.emoji_create(guild1, name, emoji_data)
        emoji2 = await client.emoji_create(guild2, name, emoji_data)
        
        await emoji_delete(client, emoji1)
        await emoji_delete(client, emoji2)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0083(client, message, name:str, emoji:'Emoji'):
    """
    Creates an emoji in 2 guilds and then deletes it. Checks emoji creation.
    
    Please also give a name for the emoji and an emoji as well.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0083') as RLT:
        if len(client.guild_profiles) < 2:
            await RLT.send('The client should be at least in 2 guilds.')
        
        for index, guild_id in enumerate(client.guild_profiles.keys()):
            guild = GUILDS[guild_id]
            if index == 0:
                guild1 = guild
            else:
                guild2 = guild
        
        async with client.http.get(emoji.url) as response:
            emoji_data = await response.read()
        
        emoji1 = await emoji_create(client, guild1, name, emoji_data)
        emoji2 = await emoji_create(client, guild2, name, emoji_data)
        
        await client.emoji_delete(emoji1)
        await client.emoji_delete(emoji2)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0084(client, message, name:str, emoji:'Emoji'):
    """
    Creates 2 emoji in 1 guild and then deletes it. Checks emoji creation.
    
    Please also give a name for the emoji and an emoji as well.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0084') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        async with client.http.get(emoji.url) as response:
            emoji_data = await response.read()
        
        emoji1 = await emoji_create(client, guild, name, emoji_data)
        await client.emoji_delete(emoji1)
        
        emoji2 = await emoji_create(client, guild, name, emoji_data)
        await client.emoji_delete(emoji2)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0085(client, message, name:str, emoji:'Emoji'):
    """
    Creates an emoji, edits and then deletes it. Checks emoji edition.
    
    Please also give a name for the emoji and an emoji as well.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0085') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        async with client.http.get(emoji.url) as response:
            emoji_data = await response.read()
        
        emoji = await client.emoji_create( guild, name, emoji_data)
        await emoji_edit(client, emoji, name='cake_hater')
        await client.emoji_delete(emoji)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0086(client, message, name:str,):
    """
    Edits my nick desu.
    
    Please also give a name.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0086') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await client_guild_profile_nick_edit(client, guild, name)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0087(client, message, user:'user',):
    """
    Kicks the given user from the guild.
    
    Please also give a user to kick.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0087') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await guild_user_delete(client, guild, user)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0088(client, message):
    """
    Creates a private channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0088') as RLT:
        await channel_private_create(client, message.author)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0089(client, message):
    """
    Creates a message with a webhook, then edits it.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0089') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_manage_webhooks:
            await RLT.send('I need manage webhooks permission to complete this command.')
        
        channel = message.channel
        webhooks = await client.webhook_get_all_channel(channel)
        for webhook in webhooks:
            if webhook.type is WebhookType.bot:
                executor_webhook = webhook
                break
        
        else:
            executor_webhook = await client.webhook_create(channel, 'testing')
        
        new_message = await webhook_execute(client, executor_webhook, 'ayaya')
        await webhook_message_edit(client, executor_webhook, new_message, 'nya')

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0090(client, message):
    """
    Creates a message with a webhook, then deletes it.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0090') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_manage_webhooks:
            await RLT.send('I need manage webhooks permission to complete this command.')
        
        channel = message.channel
        webhooks = await client.webhook_get_all_channel(channel)
        for webhook in webhooks:
            if webhook.type is WebhookType.bot:
                executor_webhook = webhook
                break
        
        else:
            executor_webhook = await client.webhook_create(channel, 'testing')
        
        new_message = await webhook_execute(client, executor_webhook, 'ayaya')
        await webhook_message_delete(client, executor_webhook, new_message)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0091(client, message):
    """
    Creates 6 messages and deletes them.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0091') as RLT:
        messages = []
        for index in range(6):
            message = await client.message_create(channel, str(index))
            messages.append(message)
        
        for message in messages:
            await message_delete(client, message)

PERMISSION_MASK_MESSAGING = Permission().update_by_keys(
    send_messages = True,
    send_messages_in_threads = True,
)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0092(client, message, channel2:ChannelText=None):
    """
    Creates 3 messages in 2 channels and deletes them. Please also define an other channel.
    """
    channel1 = message.channel
    with RLTCTX(client, channel1, 'rate_limit_test_0092') as RLT:
        if channel2 is None:
            await RLT.send('No second channel was given.')
        
        if not channel2.cached_permissions_for(client) & PERMISSION_MASK_MESSAGING:
            await RLT.send('I have no permissions to send messages at the other channel.')
        
        messages = []
        for index in range(3):
            message = await client.message_create(channel1, str(index))
            messages.append(message)
        
        for index in range(3):
            message = await client.message_create(channel2, str(index))
            messages.append(message)
        
        for message in messages:
            await message_delete(client, message)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0093(client, message):
    """
    Creates and edits messages.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0093') as RLT:
        messages = []
        for index in range(3):
            message = await message_create(client, channel, str(index))
            messages.append(message)
        
        for index, message in enumerate(messages, 3):
            await message_edit(client, message, str(index))
        
        for message in messages:
            await client.message_delete(message)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0094(client, message):
    """
    Creates 7 messages and deletes 5 1 by 1 and the last 2 together.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0094') as RLT:
        messages = []
        for index in range(7):
            message = await client.message_create(channel, str(index))
            messages.append(message)
        
        for index in range(5):
            message = messages[index]
            await message_delete(client, message)
        
        await message_delete_multiple(client, messages[5:])

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0095(client, message):
    """
    Edits the channel's name 3 times.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0095') as RLT:
        if channel.guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        for name in ('ayaya', 'nyan', 'ahaha'):
            await channel_edit(client, channel, name=name)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0096(client, message):
    """
    Gets the global application commands.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0096') as RLT:
        await application_command_global_get_all(client)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0097(client, message):
    """
    Creates, edits and the deletes an application command.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0097') as RLT:
        application_command_schema = ApplicationCommand(
            'This-command_cake',
            'But does nothing for real, pls don\'t use it.',
                )
        
        application_command = await application_command_global_create(client, application_command_schema)
        
        application_command_schema.description = 'The floor is lava.'
        application_command_schema.name = 'derping-out'
        
        await application_command_global_edit(client, application_command, application_command_schema)
        await application_command_global_delete(client, application_command)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0098(client, message):
    """
    Gets the guild application commands for the channel's respective guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0098') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await application_command_guild_get_all(client, guild)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0099(client, message):
    """
    Creates, edits and the deletes a guild bound application command.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0099') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command_schema = ApplicationCommand(
            'This-command_cake',
            'But does nothing for real, pls don\'t use it.',
                )
        
        application_command = await application_command_guild_create(client, guild, application_command_schema)
        
        application_command_schema.description = 'The floor is lava.'
        application_command_schema.name = 'derping-out'
        
        await application_command_guild_edit(client, guild, application_command, application_command_schema)
        await application_command_guild_delete(client, guild, application_command)

class check_interacter:
    __slots__ = ('user', 'channel', 'application_command')
    def __init__(self, channel, user, application_command):
        self.channel = channel
        self.user = user
        self.application_command = application_command
        
    def __call__(self, event):
        channel, user, interaction_command = event
        if channel is not self.channel:
            return False
        
        if user is not self.user:
            return False
        
        if interaction_command.id != self.application_command.id:
            return False
        
        return True

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0100(client, message):
    """
    Adds a new interaction command to the guild, what u should use, then creates edits and deletes it's message.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0100') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command_schema = ApplicationCommand(
            'test_command',
            'ayaya',
                )
        
        # Command
        application_command = await client.application_command_guild_create(guild, application_command_schema)
        
        await client.message_create(channel, 'Please use `/test_command`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await RLT.send('timeout occurred.')
        else:
            await interaction_response_message_create(client, interaction, 'Ayaya')
            await interaction_response_message_edit(client, interaction, 'Nayaya?')
            await interaction_response_message_delete(client, interaction)
        finally:
            await client.application_command_guild_delete(guild, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0101(client, message):
    """
    Adds a new interaction command to the guild, what u should use twice, then creates edits and deletes it's message.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0101') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command_schema = ApplicationCommand(
            'test_command',
            'ayaya',
                )
        
        # Command
        application_command = await client.application_command_guild_create(guild, application_command_schema)
        
        await client.message_create(channel, 'Please use `/test_command` twice')
        
        # Wait
        try:
            try:
                interaction1 = await client.wait_for('interaction_create',
                    check_interacter(channel, message.author, application_command), timeout=300.0)
            except TimeoutError:
                await RLT.send('timeout occurred.')
            
            await interaction_response_message_create(client, interaction1, 'resp1')
            
            try:
                interaction2 = await client.wait_for('interaction_create',
                    check_interacter(channel, message.author, application_command), timeout=300.0)
            except TimeoutError:
                await RLT.send('timeout occurred.')
            
            await interaction_response_message_create(client, interaction2, 'resp2')
            
            await interaction_response_message_edit(client, interaction1, 'Nayaya?')
            await interaction_response_message_delete(client, interaction1)
            
            await interaction_response_message_edit(client, interaction2, 'Nayaya?')
            await interaction_response_message_delete(client, interaction2)
        finally:
            
            await client.application_command_guild_delete(guild, application_command)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0102(client, message):
    """
    Adds a new interaction command to the guild, what u should call and the does 2 messages edits an deletes them.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0102') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command_schema = ApplicationCommand(
            'test_command',
            'ayaya',
        )
        
        # Command
        application_command = await client.application_command_guild_create(guild, application_command_schema)
        
        await client.message_create(channel, 'Please use `/test_command`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await RLT.send('timeout occurred.')
        else:
            await interaction_response_message_create(client, interaction, 'Ayaya')
            await interaction_response_message_edit(client, interaction, 'Nayaya?')
            await interaction_response_message_delete(client, interaction)
            message = await interaction_followup_message_create(client, interaction, 'Ayaya')
            await interaction_followup_message_edit(client, interaction, message, 'Nayaya?')
            await interaction_followup_message_get(client, interaction, message)
            await interaction_followup_message_delete(client, interaction, message)
        finally:
            await client.application_command_guild_delete(guild, application_command)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0103(client, message):
    """
    Gets the verification screen of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0103') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await verification_screen_get(client, guild)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0104(client, message):
    """
    Edits the verification screen of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0104') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await verification_screen_edit(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0105(client, message):
    """
    Edits the welcome screen of the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0105') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await welcome_screen_edit(client, guild)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0106(client, message, guild2:'guild'=None):
    """
    Edits the welcome screen of 2 guilds. Please also define the second guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0106') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if guild2 is None:
            await RLT.send('Second guild unknown.')
        
        await welcome_screen_edit(client, guild)
        await welcome_screen_edit(client, guild2)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0107(client, message):
    """
    Gets a global application command.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0107') as RLT:
        application_commands = await client.application_command_global_get_all()
        if application_commands:
            application_command = application_commands[0]
            delete_after = False
        else:
            application_command = client.application_command_global_create(ApplicationCommand('test_command', 'ayaya'))
            delete_after = True
        
        try:
            await application_command_global_get(client, application_command.id)
        finally:
            if delete_after:
                await client.application_command_global_delete(application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0108(client, message):
    """
    Gets a guild bound application command.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0108') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_commands = await client.application_command_guild_get_all(guild)
        if application_commands:
            application_command = application_commands[0]
            delete_after = False
        else:
            application_command = client.application_command_guild_create(guild,
                ApplicationCommand('test_command', 'ayaya'))
            delete_after = True
        
        try:
            await application_command_guild_get(client, guild, application_command.id)
        finally:
            if delete_after:
                await client.application_command_guild_delete(guild, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0109(client, message):
    """
    Adds guild and global command with the update many endpoint, then deletes them.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0109') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_commands = await client.application_command_global_get_all()
        if application_commands:
            application_command = application_commands[0]
            delete_command_after = False
        else:
            application_command = ApplicationCommand('test_command', 'ayaya')
            delete_command_after = True
        
        try:
            application_commands = await application_command_global_update_multiple(client, [application_command])
        finally:
            if delete_command_after:
                application_command = application_commands[0]
                await client.application_command_global_delete(application_command)
        
        application_commands = await client.application_command_guild_get_all(guild)
        if application_commands:
            application_command = application_commands[0]
            delete_command_after = False
        else:
            application_command = ApplicationCommand('test_command', 'ayaya')
            delete_command_after = True
        
        try:
            application_commands = await application_command_guild_update_multiple(client, guild, [application_command])
        finally:
            if delete_command_after:
                application_command = application_commands[0]
                await client.application_command_guild_delete(guild, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0110(client, message, guild2:'guild'=None):
    """
    Adds command with 2 guilds, then uses the update many endpoint. Please give an additional guild to use the command
    within.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0110') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if guild2 is None:
            await RLT.send('Second guild unknown.')
        
        application_commands = await client.application_command_guild_get_all(guild2)
        if application_commands:
            application_command = application_commands[0]
            delete_command_after = False
        else:
            application_command = ApplicationCommand('test_command', 'ayaya')
            delete_command_after = True
        
        try:
            application_commands = await application_command_guild_update_multiple(client, guild2, [application_command])
        finally:
            if delete_command_after:
                application_command = application_commands[0]
                await client.application_command_guild_delete(guild2, application_command)
        
        application_commands = await client.application_command_guild_get_all(guild)
        if application_commands:
            application_command = application_commands[0]
            delete_command_after = False
        else:
            application_command = ApplicationCommand('test_command', 'ayaya')
            delete_command_after = True
        
        try:
            application_commands = await application_command_guild_update_multiple(client, guild, [application_command])
        finally:
            if delete_command_after:
                application_command = application_commands[0]
                await client.application_command_guild_delete(guild, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0111(client, message, guild2:'guild'=None):
    """
    Creates application command within 2 guilds. Please define a second guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0111') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if guild2 is None:
            await RLT.send('Second guild unknown.')
        
        application_command = ApplicationCommand('test_command', 'ayaya')
        application_command = await application_command_guild_create(client, guild2, application_command)
        await client.application_command_guild_delete(guild2, application_command)
        
        application_command = ApplicationCommand('test_command', 'ayaya')
        application_command = await application_command_guild_create(client, guild, application_command)
        await client.application_command_guild_delete(guild, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0112(client, message, guild2:'guild'=None):
    """
    Creates, edits and the deletes a guild bound application command. Please define a second guild as well.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0112') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if guild2 is None:
            await RLT.send('Second guild unknown.')
        
        application_command_schema = ApplicationCommand(
            'This-command_cake',
            'But does nothing for real, pls don\'t use it.',
                )
        
        application_command = await application_command_guild_create(client, guild, application_command_schema)
        
        application_command_schema.description = 'The floor is lava.'
        application_command_schema.name = 'derping-out'
        
        await application_command_guild_edit(client, guild, application_command, application_command_schema)
        await application_command_guild_delete(client, guild, application_command)
        
        application_command_schema = ApplicationCommand(
            'This-command_cake',
            'But does nothing for real, pls don\'t use it.',
                )
        
        application_command = await application_command_guild_create(client, guild2, application_command_schema)
        
        application_command_schema.description = 'The floor is lava.'
        application_command_schema.name = 'derping-out'
        
        await application_command_guild_edit(client, guild2, application_command, application_command_schema)
        await application_command_guild_delete(client, guild2, application_command)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0113(client, message):
    """
    Request all the application command permissions in the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0113') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await application_command_permission_get_all_guild(client, guild)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0114(client, message):
    """
    Request an application command's permissions in the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0114') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command = ApplicationCommand('test_command_56', 'ayaya')
        application_command = await client.application_command_guild_create(guild, application_command)
        
        await application_command_permission_edit(client, guild, application_command,
            [ApplicationCommandPermissionOverwrite(client.owner, True)])
        await application_command_permission_get(client, guild, application_command)
        
        await client.application_command_guild_delete(guild, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0115(client, message):
    """
    Edits an application command's permissions in the guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0115') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command = ApplicationCommand('test_command_56', 'ayaya')
        application_command = await client.application_command_guild_create(guild, application_command)
        
        await application_command_permission_edit(client, guild, application_command,
            [ApplicationCommandPermissionOverwrite(client.owner, True)])
        
        await client.application_command_guild_delete(guild, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0116(client, message):
    """
    Edits a guild and a global application command inside of the same guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0116') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command = ApplicationCommand('test_command_56', 'ayaya')
        application_command = await client.application_command_guild_create(guild, application_command)
        
        await application_command_permission_edit(client, guild, application_command,
            [ApplicationCommandPermissionOverwrite(client.owner, True)])
        
        await client.application_command_guild_delete(guild, application_command)

        application_command = ApplicationCommand('test_command_56', 'ayaya')
        application_command = await client.application_command_global_create(application_command)
        
        await application_command_permission_edit(client, guild, application_command,
            [ApplicationCommandPermissionOverwrite(client.owner, True)])
        
        await client.application_command_global_delete(application_command)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0117(client, message, guild2:'guild'=None):
    """
    Creates and edits application commands inside of 2 guilds.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0117') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if guild2 is None:
            await RLT.send('Second guild unknown.')

        application_command = ApplicationCommand('test_command_56', 'ayaya')
        application_command = await client.application_command_guild_create(guild, application_command)
        
        await application_command_permission_edit(client, guild, application_command,
            [ApplicationCommandPermissionOverwrite(client.owner, True)])
        
        await client.application_command_guild_delete(guild, application_command)
        
        application_command = ApplicationCommand('test_command_56', 'ayaya')
        application_command = await client.application_command_guild_create(guild2, application_command)
        
        await application_command_permission_edit(client, guild2, application_command,
            [ApplicationCommandPermissionOverwrite(client.owner, True)])
        
        await client.application_command_guild_delete(guild2, application_command)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0118(client, message):
    """
    Joins to a stage channel.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0118') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
            
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        stage_channels = guild.stage_channels
        if not stage_channels:
            await RLT.send('The guild has no stage channels.')
        
        stage_channel = stage_channels[0]
        
        voice_client = await client.join_voice(stage_channel)
        await voice_state_client_edit(client, stage_channel)
        await voice_client.disconnect()


async def rate_limit_test_0119_parallel(client, stage_channel):
    voice_client = await client.join_voice(stage_channel)
    await voice_state_client_edit(client, stage_channel)
    await voice_client.disconnect()


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0119(client, message, guild2:'guild'=None):
    """
    Joins to 2 stage channels. Please also define a second guild.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0119') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if guild2 is None:
            await RLT.send('Second guild unknown.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        stage_channels_1 = guild.stage_channels
        if not stage_channels_1:
            await RLT.send('The guild has no stage channels.')
        
        stage_channels_2 = guild.stage_channels
        if not stage_channels_2:
            await RLT.send('The second guild has no stage channels.')
        
        tasks = []
        for stage_channel in (stage_channels_1[0], stage_channels_2[0]):
            task = Task(rate_limit_test_0119_parallel(client, stage_channel), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)

async def rate_limit_test_0120_parallel(client, stage_channel, user):
    voice_client = await client.join_voice(stage_channel)
    await voice_state_user_edit(client, stage_channel, user, True)
    await voice_client.disconnect()

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0120(client, message, guild2:'guild'=None):
    """
    Moves 2 users in stage channels. Please also define an other guild.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0120') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if guild2 is None:
            await RLT.send('Second guild unknown.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        stage_channels_1 = guild.stage_channels
        if not stage_channels_1:
            await RLT.send('The guild has no stage channels.')
        
        stage_channel_1 = stage_channels_1[0]
        
        users_1 = stage_channel_1.voice_users
        if not users_1:
            await RLT.send('The stage channel has no users in it.')
        
        user_1 = users_1[0]
        
        stage_channels_2 = guild.stage_channels
        if not stage_channels_2:
            await RLT.send('The second guild has no stage channels.')
        
        stage_channel_2 = stage_channels_2[0]
        
        users_2 = stage_channel_2.voice_users
        if not users_2:
            await RLT.send('The second guild has no stage channels.')
        
        user_2 = users_2[0]
        
        tasks = []
        for stage_channel, user in ((stage_channel_1, user_1), (stage_channel_2, user_2)):
            task = Task(rate_limit_test_0120_parallel(client, stage_channel, user), KOKORO)
            tasks.append(task)
        
        await WaitTillAll(tasks, KOKORO)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0121(client, message):
    """
    Gets stage discovery.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0121') as RLT:
        await stage_discovery_get(client)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0122(client, message):
    """
    Gets stage channels and such maybe?.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0122') as RLT:
        try:
            await stage_get_all(client)
        except DiscordException as err:
            if err.code == ERROR_CODES.bots_not_allowed:
                pass
            else:
                raise

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0123(client, message, stage_channel:'channel'=None):
    """
    Edits a stage channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0123') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if stage_channel is None:
            await RLT.send('Please define a channel.')
        
        if not isinstance(stage_channel, ChannelStage):
            await RLT.send('Stage channel only.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        
        await stage_create(client, stage_channel, 'Ayaya')


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0124(client, message, stage_channel:'channel'=None):
    """
    Edits a stage channel's topic only.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0124') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if stage_channel is None:
            await RLT.send('Please define a channel.')
        
        if not isinstance(stage_channel, ChannelStage):
            await RLT.send('Stage channel only.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await stage_edit(client, stage_channel, 'Ayaya')


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0125(client, message):
    """
    Gets the discoverable guilds.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0125') as RLT:
        await guild_discovery_get_all(client)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0126(client, message, stage_channel:'channel'=None):
    """
    Deletes a stage.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0126') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if stage_channel is None:
            await RLT.send('Please define a channel.')
        
        if not isinstance(stage_channel, ChannelStage):
            await RLT.send('Stage channel only.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await stage_delete(client, stage_channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0127(client, message):
    """
    Creates a message with a webhook, then gets it. Ayyy.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0127') as RLT:
        guild = message.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_manage_webhooks:
            await RLT.send('I need manage webhooks permission to complete this command.')
        
        channel = message.channel
        webhooks = await client.webhook_get_all_channel(channel)
        for webhook in webhooks:
            if webhook.type is WebhookType.bot:
                executor_webhook = webhook
                break
        
        else:
            executor_webhook = await client.webhook_create(channel, 'testing')
        
        new_message = await webhook_execute(client, executor_webhook, 'ayaya')
        await webhook_message_get(client, executor_webhook, new_message.id)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0128(client, message):
    """
    Adds a new interaction command to the guild, what u should use, then creates and gets the message.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0128') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        application_command_schema = ApplicationCommand(
            'test_command',
            'ayaya',
        )
        
        # Command
        application_command = await client.application_command_guild_create(guild, application_command_schema)
        
        await client.message_create(channel, 'Please use `/test_command`')
        
        # Wait
        try:
            interaction = await client.wait_for('interaction_create',
                check_interacter(channel, message.author, application_command), timeout=300.0)
        except TimeoutError:
            await RLT.send('timeout occurred.')
        else:
            await client.interaction_response_message_create(interaction, 'Ayaya')
            await interaction_response_message_edit(client, interaction, 'Nayaya?')
            await interaction_response_message_get(client, interaction)
        finally:
            await client.application_command_guild_delete(guild, application_command)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0129(client, message):
    """
    Creates a thread channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0129') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_create(client, channel, 11, 'ayaya')


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0130(client, message):
    """
    Joins thread??
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0130') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_join(client, channel)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0131(client, message):
    """
    hata superiority test.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0131') as RLT:
        await application_button_create(client, {'type': ComponentType.button.value})


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0132(client, message):
    """
    Leaves from the thread.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0132') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_leave(client, channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0133(client, message):
    """
    Leaves from a guild.
    
    Method not allowed.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0133') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_get_self(client, channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0134(client, message):
    """
    Gets a thread's user.
    
    Method not allowed.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0134') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_user_get(client, channel, message.author)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0135(client, message):
    """
    Adds a user to a thread.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0135') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_user_add(client, channel, message.author)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0136(client, message):
    """
    Deletes a thread's user.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0136') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_user_delete(client, channel, message.author)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0137(client, message):
    """
    Edits thread settings.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0137') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_self_settings_edit(client, channel, {'type': 11})


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0138(client, message):
    """
    Gets the archived public threads of the channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0138') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await channel_thread_get_chunk_archived_public(client, channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0139(client, message):
    """
    Gets the threads from my archive?
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0139') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await channel_thread_get_chunk_self_archived(client, channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0140(client, message):
    """
    Gets the guilds?
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0140') as RLT:
        await servers_get(client)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0141(client, message, stage_channel:'channel'=None):
    """
    Gets a stage channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0141') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if stage_channel is None:
            await RLT.send('Please define a channel.')
        
        if not isinstance(stage_channel, ChannelStage):
            await RLT.send('Stage channel only.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await stage_get(client, stage_channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0142(client, message):
    """
    Edits my avatar.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0142') as RLT:
        attachment = message.attachment
        if attachment is None:
            await RLT.send('attachment is required.')
        
        content_type = attachment.content_type
        if (content_type is None) or (not content_type.startswith(content_type)):
            await RLT.send('Image is required')
        
        avatar = await client.download_attachment(attachment)
        await client_edit(client, avatar=avatar)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0143(client, message):
    """
    Requests the guild's stickers.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0143') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await sticker_guild_get_all(client, guild)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0144(client, message):
    """
    Requests the sticker packs.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0144') as RLT:
        await sticker_pack_get_all(client)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0145(client, message, sticker_id:int=None):
    """
    Requests a sticker. Defaults to `0`.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0145') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if sticker_id is None:
            await RLT.send('`sticker_id` parameter not satisfied.')
        
        await sticker_guild_get(client, guild, sticker_id)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0146(client, message, emoji1: 'emoji' = None, emoji2: 'emoji'=None):
    """
    Creates a sticker from an emoji.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0146') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if emoji1 is None:
            await RLT.send('Please give an emoji to mimic.')
        
        if (emoji1.is_unicode_emoji()):
            await RLT.send('First emoji must be custom emoji.')
        
        if emoji2 is None:
            await RLT.send('Please give a second emoji to use as tag.')
        
        if (emoji2.is_custom_emoji()):
            await RLT.send('Second emoji must be unicode emoji.')
        
        async with client.http.get(emoji1.url) as response:
            file = await response.read()
        
        name = emoji1.name
        description = name
        tags = [emoji2.name, 'egg']
        
        await sticker_guild_create(client, guild, name, description, file, tags)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0147(client, message, sticker_id:int=None):
    """
    Deletes a sticker.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0147') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if sticker_id is None:
            await RLT.send('`sticker_id` parameter not satisfied.')
        
        await sticker_guild_delete(client, guild, sticker_id)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0148(client, message):
    """
    Gets a sticker, nya.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0148') as RLT:
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        await sticker_get(client, 819131232642007062)

@RATE_LIMIT_COMMANDS
async def rate_limit_test_0149(client, message, name:str,):
    """
    Edits my nick desu.
    
    Please also give a name.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0149') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await client_guild_profile_edit(client, guild, name)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0150(client, message, name:str, guild_id:str=''):
    """
    Edits my nick in 2 guilds. Please give a name and the second guild.
    """
    channel = message.channel
    with RLTCTX(client,channel,'rate_limit_test_0150') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        await client_guild_profile_edit(client, guild_1, name)
        await client_guild_profile_edit(client, guild_2, name)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0151(client, message, sticker_id:int=None, name:str=None):
    """
    Edits a sticker.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0151') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not channel.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission to complete this command.')
        
        if sticker_id is None:
            await RLT.send('`sticker_id` parameter not satisfied.')
        
        if name is None:
            await RLT.send('Please also pass a new name for the sticker.')
        
        sticker = await client.sticker_get(sticker_id)
        
        await sticker_guild_edit(client, guild, sticker, name=name)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0152(client, message, name:str):
    """
    Edits the guild's vanity invite.
    
    Please also give a name.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0152') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await vanity_invite_edit(client, guild, name)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0153(client, message):
    """
    status_incident_unresolved
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0153') as RLT:
        await status_incident_unresolved(client)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0154(client, message):
    """
    status_maintenance_active
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0154') as RLT:
        await status_maintenance_active(client)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0155(client, message):
    """
    status_maintenance_upcoming
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0155') as RLT:
        await status_maintenance_upcoming(client)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0156(client, message):
    """
    greet!
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0156') as RLT:
        private_channel = await client.channel_private_create(message.author)
        await greet(client, private_channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0157(client, message, directory_channel:'channel'=None, name:'str'=None):
    """
    Gets directory sub-channel by name?
    
    Please define channel and name.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0157') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if directory_channel is None:
            await RLT.send('Please define a channel.')
        
        if not isinstance(directory_channel, ChannelDirectory):
            await RLT.send('Directory channel only.')
        
        if name is None:
            await RLT.send('Please define a name to query.')
        
        await channel_directory_search(client, directory_channel, 'Ayaya')


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0158(client, message, directory_channel:'channel'=None):
    """
    Gets directory sub-channel count?
    
    Please define channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0158') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if directory_channel is None:
            await RLT.send('Please define a channel.')
        
        if not isinstance(directory_channel, ChannelDirectory):
            await RLT.send('Directory channel only.')
        
        await channel_directory_counts(client, directory_channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0159(client, message, directory_channel:'channel'=None):
    """
    Gets directory sub-channels?
    
    Please define channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0159') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if directory_channel is None:
            await RLT.send('Please define a channel.')
        
        if not isinstance(directory_channel, ChannelDirectory):
            await RLT.send('Directory channel only.')
        
        await channel_directory_get_all(client, directory_channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0160(client, message):
    """
    Creates a thread channel from the sent message.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0160') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_create_from_message(client, message, 10, 'ayaya')


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0161(client, message):
    """
    Gets the archived private threads of the channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0161') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await channel_thread_get_chunk_archived_private(client, channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0162(client, message):
    """
    Gets the active threads of the channel.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0162') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await channel_thread_get_chunk_active(client, channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0163(client, message):
    """
    Gets the users of the thread.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0163') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await thread_user_get_all(client, channel)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0164(client, message):
    """
    Gets the active threads of a guild.
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0164') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        if not guild.cached_permissions_for(client).can_adminIgnoreCaseStringator:
            await RLT.send('I need admin permission in the second guild as well to complete this command.')
        
        await guild_thread_get_all_active(client, guild)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0165(client, message):
    """
    Requests a sticker pack
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0165') as RLT:
        sticker_packs = await client.sticker_pack_get_all()
        if not sticker_packs:
            await RLT.send('No sticker packs detected.')
        
        sticker_pack_id = sticker_packs[0].id
        
        await sticker_pack_get(client, sticker_pack_id)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0166(client, message):
    """
    scheduled_event_get_all_guild
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0166') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        await scheduled_event_get_all_guild(client, guild)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0167(client, message, guild_id:str=''):
    """
    scheduled_event_get_all_guild | 2 guilds, please pass a second guild_id
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0167') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        await scheduled_event_get_all_guild(client, guild_1)
        await scheduled_event_get_all_guild(client, guild_2)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0168(client, message):
    """
    scheduled_event_create
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0168') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        voice_channels = guild.voice_channels
        if (not voice_channels):
            await RLT.send('The guild has no voice channel, please create one..')
            
        voice = voice_channels[0]
        
        await scheduled_event_create(client, guild, voice, 'ayaya')


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0169(client, message, guild_id:str=''):
    """
    scheduled_event_create | 2 guilds, please pass a second guild_id
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0169') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        guild_1_voice_channels = guild_1.voice_channels
        if (not guild_1_voice_channels):
            await RLT.send('The guild has no voice channel, please create one..')
            
        voice_1 = guild_1_voice_channels[0]
        
        guild_2_voice_channels = guild_2.voice_channels
        if (not guild_2_voice_channels):
            await RLT.send('The other guild has no voice channel, please create one..')
        
        voice_2 = guild_2_voice_channels[0]
        
        await scheduled_event_create(client, guild_1, voice_1, 'ayaya')
        await scheduled_event_create(client, guild_2, voice_2, 'ayaya')


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0170(client, message):
    """
    scheduled_event_get
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0170') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        scheduled_events = await client.scheduled_event_get_all_guild(guild)
        if not scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        scheduled_event_id = scheduled_events[0].id
        
        await scheduled_event_get(client, guild, scheduled_event_id)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0171(client, message, guild_id:str=''):
    """
    scheduled_event_get | 2 guild
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0171') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        guild_1_scheduled_events = await client.scheduled_event_get_all_guild(guild_1)
        if not guild_1_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_1_scheduled_event_id = guild_1_scheduled_events[0].id
        
        guild_2_scheduled_events = await client.scheduled_event_get_all_guild(guild_2)
        if not guild_2_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_2_scheduled_event_id = guild_2_scheduled_events[0].id
        
        await scheduled_event_get(client, guild_1, guild_1_scheduled_event_id)
        await scheduled_event_get(client, guild_2, guild_2_scheduled_event_id)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0172(client, message):
    """
    scheduled_event_edit
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0172') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        scheduled_events = await client.scheduled_event_get_all_guild(guild)
        if not scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        scheduled_event = scheduled_events[0]
        if scheduled_event.name == 'ayaya':
            name = 'apple'
        else:
            name = 'ayaya'
        
        await scheduled_event_edit(client, scheduled_event, name)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0173(client, message, guild_id:str=''):
    """
    scheduled_event_edit | 2 guild
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0173') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        guild_1_scheduled_events = await client.scheduled_event_get_all_guild(guild_1)
        if not guild_1_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_1_scheduled_event = guild_1_scheduled_events[0]
        if guild_1_scheduled_event.name == 'ayaya':
            guild_1_name = 'apple'
        else:
            guild_1_name = 'ayaya'
        
        guild_2_scheduled_events = await client.scheduled_event_get_all_guild(guild_2)
        if not guild_2_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_2_scheduled_event = guild_2_scheduled_events[0]
        if guild_2_scheduled_event.name == 'ayaya':
            guild_2_name = 'apple'
        else:
            guild_2_name = 'ayaya'
        
        await scheduled_event_edit(client, guild_1_scheduled_event, guild_1_name)
        await scheduled_event_edit(client, guild_2_scheduled_event, guild_2_name)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0174(client, message, guild_id:str=''):
    """
    scheduled_event_delete | 2 guild
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0174') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        guild_1_scheduled_events = await client.scheduled_event_get_all_guild(guild_1)
        if not guild_1_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_1_scheduled_event = guild_1_scheduled_events[0]
        
        guild_2_scheduled_events = await client.scheduled_event_get_all_guild(guild_2)
        if not guild_2_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_2_scheduled_event = guild_2_scheduled_events[0]
        
        await scheduled_event_delete(client, guild_1_scheduled_event)
        await scheduled_event_delete(client, guild_2_scheduled_event)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0175(client, message):
    """
    scheduled_event_edit + scheduled_event_delete
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0175') as RLT:
        guild = channel.guild
        if guild is None:
            await RLT.send('Please use this command at a guild.')
        
        scheduled_events = await client.scheduled_event_get_all_guild(guild)
        if not scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        scheduled_event = scheduled_events[0]
        if scheduled_event.name == 'ayaya':
            name = 'apple'
        else:
            name = 'ayaya'
        
        await scheduled_event_edit(client, scheduled_event, name)
        await scheduled_event_delete(client, scheduled_event)


@RATE_LIMIT_COMMANDS
async def rate_limit_test_0176(client, message, guild_id:str=''):
    """
    scheduled_event_user_get_chunk | 2 guild
    """
    channel = message.channel
    with RLTCTX(client, channel, 'rate_limit_test_0176') as RLT:
        guild_1 = channel.guild
        if guild_1 is None:
            await RLT.send('Please use this command at a guild.')
        
        try:
            guild_2 = GUILDS[int(guild_id)]
        except (KeyError, ValueError):
            await RLT.send('Please pass a guild id as well, where I am as well.')
        
        guild_1_scheduled_events = await client.scheduled_event_get_all_guild(guild_1)
        if not guild_1_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_1_scheduled_event = guild_1_scheduled_events[0]
        
        guild_2_scheduled_events = await client.scheduled_event_get_all_guild(guild_2)
        if not guild_2_scheduled_events:
            await RLT.send('Please create a scheduled event first.')
        
        guild_2_scheduled_event = guild_2_scheduled_events[0]
        
        await scheduled_event_user_get_chunk(client, guild_1_scheduled_event)
        await scheduled_event_user_get_chunk(client, guild_2_scheduled_event)
