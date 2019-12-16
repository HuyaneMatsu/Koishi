import os
from io import StringIO
from os.path import join
import re
from weakref import WeakSet, WeakKeyDictionary

from hata.others import filter_content
from hata.prettyprint import pchunkify, pconnect
from hata.ios import ReuAsyncIO
from hata.client import Achievement
from hata.others import bytes_to_base64, parse_oauth2_redirect_url, Unknown
from hata.emoji import BUILTIN_EMOJIS, parse_emoji
from hata.futures import sleep, render_exc_to_list, Task, Future
from hata.dereaddons_local import alchemy_incendiary
from hata.invite import Invite
from hata.exceptions import DiscordException
from hata.embed import Embed
from hata.channel import CHANNELS
from hata.events_compiler import ContentParser
from hata.parsers import eventlist, EventHandlerBase
from hata.events import Pagination, wait_for_message, GUI_STATE_READY,      \
    GUI_STATE_SWITCHING_PAGE, GUI_STATE_CANCELLING, GUI_STATE_CANCELLED,    \
    GUI_STATE_SWITCHING_CTX, multievent, asynclist, CommandProcesser,       \
    EventDescriptor

commands = eventlist()

def entry(client):
    event=client.events.message_create.shortcut.extend(commands)

def exit(client):
    event=client.events.message_create.shortcut.unextend(commands)
    
    #unload CustomLinkCommand
    CustomLinkCommand.unload(client)
    
    #unload keep_checking_emoji
    keep_checking_emoji.unload(client)

# works
@commands
async def achievement_create(client,message,content):
    if not client.is_owner(message.author):
        return
        
    content=filter_content(content)
    if len(content)<2:
        await client.message_create(message.channel,
            'expected at least 2 content parts')
        return

    image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
    with (await ReuAsyncIO(image_path)) as file:
        image = await file.read()
    try:
        achievement = await client.achievement_create(
            content[0],content[1],image)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_create;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return
    
    chunks=pchunkify(achievement)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)

# icon cannot be None
@commands
async def achievement_create_no_avatar_1(client,message,content):
    if not client.is_owner(message.author):
        return
        
    data = {
        'name'          : {
            'default'   : 'Nice',
                },
        'description'   : {
            'default'   : 'You are qt!',
                },
        'secret'        : False,
        'secure'        : False,
        'icon'          : None,
            }

    application_id=client.application.id
    
    try:
        data = await client.http.achievement_create(application_id,data)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_create;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return
    
    achievement=Achievement(data)
    
    chunks=pchunkify(achievement)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)

# icon must be passed
@commands
async def achievement_create_no_avatar_2(client,message,content):
    if not client.is_owner(message.author):
        return

    data = {
        'name'          : {
            'default'   : 'Nice',
                },
        'description'   : {
            'default'   : 'Nekos are qt',
                },
        'secret'        : False,
        'secure'        : False,
            }

    application_id=client.application.id
    
    try:
        data = await client.http.achievement_create(application_id,data)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_create;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return
    
    achievement=Achievement(data)
    
    chunks=pchunkify(achievement)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)

# the return is not `icon`, but `icon_hash`
@commands
async def achievement_create_pure_data(client,message,content):
    if not client.is_owner(message.author):
        return

    image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
    with (await ReuAsyncIO(image_path)) as file:
        image = await file.read()

    icon_data=bytes_to_base64(image)
        
    data = {
        'name'          : {
            'default'   : 'OwO',
                },
        'description'   : {
            'default'   : 'Whats this?',
                },
        'secret'        : False,
        'secure'        : False,
        'icon'          : icon_data,
            }

    application_id=client.application.id
    
    try:
        data = await client.http.achievement_create(application_id,data)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_create;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return

    content=data.__repr__()
    await client.message_create(message.channel,content)

# works
@commands
async def achievement_get_all(client,message,content):
    if not client.is_owner(message.author):
        return
        
    try:
        achievements = await client.achievement_get_all()
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_get_all;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return
    
    chunks=pchunkify(achievements)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)

# works
@commands
async def achievement_get(client,message,content):
    if not client.is_owner(message.author):
        return
    
    try:
        id_=int(content)
    except ValueError:
        await client.message_create(message.channel,'pass id pls')
        return
    
    try:
        achievement = await client.achievement_get(id_)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_get;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return

    chunks=pchunkify(achievement)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)
    return

# works, all data is optional
@commands
async def achievement_edit(client,message,content):
    if not client.is_owner(message.author):
        return

    try:
        id_=int(content)
    except ValueError:
        await client.message_create(message.channel,'pass id pls')
        return

    try:
        achievement = await client.achievement_get(id_)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_get;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return
    
    try:
        await client.achievement_edit(achievement,name='woaaa')
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_edit;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return

    chunks=pchunkify(achievement)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)
    return

# works
@commands
async def achievement_delete(client,message,content):
    if not client.is_owner(message.author):
        return

    try:
        id_=int(content)
    except ValueError:
        await client.message_create(message.channel,'pass id pls')
        return

    try:
        achievement = await client.achievement_get(id_)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_get;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return
    
    try:
        await client.achievement_delete(achievement)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At achievement_delete;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return

    chunks=pchunkify(achievement)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)

# https://github.com/discordapp/discord-api-docs/issues/1230
# unintentionally documented and will never work.


class check_is_owner(object):
    __slots__=('client', )
    def __init__(self,client):
        self.client=client
    
    def __call__(self,message):
        return self.client.is_owner(message.author)

# DiscordException UNAUTHORIZED (401): 401: Unauthorized
@commands
async def user_achievements(client,message,content):
    if not client.is_owner(message.author):
        return

    await client.message_create(message.channel, (
        'Please authorize yourself and resend the redirected url after it\n'
        'https://discordapp.com/oauth2/authorize?client_id=486565096164687885'
        '&redirect_uri=https%3A%2F%2Fgithub.com%2FHuyaneMatsu'
        '&response_type=code&scope=identify%20applications.store.update'))
    
    try:
        message = await wait_for_message(client,message.channel,check_is_owner(client),60.)
    except TimeoutError:
        await client.message_create('Timeout meanwhile waiting for redirect url.')
        return
    
    Task(client.message_delete(message),client.loop)
    try:
        result=parse_oauth2_redirect_url(message.content)
    except ValueError:
        await client.message_create(message.channel,'Bad redirect url.')
        return
    
    access = await client.activate_authorization_code(*result,['identify', 'applications.store.update'])
    
    if access is None:
        await client.message_create(message.channel,'Too old redirect url.')
        return
        
    try:
        achievements = await client.user_achievements(access)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At user_achievements;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return

    chunks=pchunkify(achievements)
    pages=[Embed(description=chunk) for chunk in chunks]
    await Pagination(client,message.channel,pages)

# https://github.com/discordapp/discord-api-docs/issues/1230
# Seems like first update must come from game SDK.
# Only secure updates are supported, if they are even.

# when updating secure achievement:
#     DiscordException NOT FOUND (404), code=10029: Unknown Entitlement
# when updating non secure:
#     DiscordException FORBIDDEN (403), code=40001: Unauthorized
@commands
async def user_achievement_update(client,message,content):
    if not client.is_owner(message.author):
        return

    try:
        id_=int(content)
    except ValueError:
        await client.message_create(message.channel,'pass id pls')
        return
    
    try:
        await client.user_achievement_update(message.author,id_,100)
    except BaseException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'At user_achievement_update;\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)
        return

    await client.message_create(message.channel,'success')
    
    
# 'target_user_type', as 0:
#     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
#     target_user_type.BASE_TYPE_CHOICES('Value must be one of (1,).')
@commands
async def target_user_type_invite_test_0(client,message,content):
    if not client.is_owner(message.author):
        return

    channel=message.channel
    if channel.guild is None:
        await client.message_create(channel,'Guild only!')
        return

    data = {
        'max_age'           : 0,
        'max_uses'          : 0,
        'temporary'         : True,
        'unique'            : True,
        'target_user_type'  : 0,
            }

    try:
        data = await client.http.invite_create(channel.id,data)
    except DiscordException as err:
        result=repr(err)
    else:
        result=repr(data)
        await client.http.invite_delete(data['code'],'just testin')

    await client.message_create(channel,result)

# 'target_user_type', as 1:
#     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
#     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
@commands
async def target_user_type_invite_test_1(client,message,content):
    if not client.is_owner(message.author):
        return

    channel=message.channel
    if message.channel.guild is None:
        client.message_create(channel,'Guild only!')
        return

    data = {
        'max_age'           : 0,
        'max_uses'          : 0,
        'temporary'         : False,
        'unique'            : True,
        'target_user_type'  : 1,
            }

    try:
        data = await client.http.invite_create(channel.id,data)
    except DiscordException as err:
        result=repr(err)
    else:
        result=repr(data)
        await client.http.invite_delete(data['code'],'just testin')

    await client.message_create(channel,result)

# 'target_user_id' :
#     DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
#     target_user_type.GUILD_INVITE_INVALID_TARGET_USER_TYPE('Invalid target user type')
@commands
async def target_user_id_invite_test(client,message,content):
    if not client.is_owner(message.author):
        return

    channel=message.channel
    if channel.guild is None:
        await client.message_create(channel,'Guild only!')
        return

    data = {
        'max_age'           : 0,
        'max_uses'          : 0,
        'temporary'         : False,
        'unique'            : True,
        'target_user_id'    : 319854926740062208,
            }

    try:
        data = await client.http.invite_create(channel.id,data)
    except DiscordException as err:
        result=repr(err)
    else:
        result=repr(data)
        await client.http.invite_delete(data['code'],'just testin')

    await client.message_create(channel,result)

# 'target_user_id' and 'target_user_type' together:
#    DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
#    target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
@commands
async def target_user_id_with_type_test(client,message,content):
    if not client.is_owner(message.author):
        return

    channel=message.channel
    if channel.guild is None:
        await client.message_create(channel,'Guild only!')
        return

    data = {
        'max_age'           : 0,
        'max_uses'          : 0,
        'temporary'         : False,
        'unique'            : True,
        'target_user_type'  : 1,
        'target_user_id'    : 319854926740062208,
            }

    try:
        data = await client.http.invite_create(channel.id,data)
    except DiscordException as err:
        result=repr(err)
    else:
        result=repr(data)
        await client.http.invite_delete(data['code'],'just testin')

    await client.message_create(channel,result)

# 'target_user_id' and 'target_user_type' with not correct channel:
#    DiscordException BAD REQUEST (400), code=50035: Invalid Form Body
#    target_user_id.GUILD_INVITE_INVALID_STREAMER('The specified user is currently not streaming in this channel')
@commands
async def target_user_stream_test_0(client,message,content):
    if not client.is_owner(message.author):
        return

    channel=message.channel
    guild=channel.guild
    if guild is None:
        await client.message_create(channel,'Guild only!')
        return

    voice_states=guild.voice_states
    if not voice_states:
        await client.message_create(channel,'No voice state at the guild.')
        return

    for voice_state in voice_states.values():
        if voice_state.self_video:
            break
    else:
        await client.message_create(channel,'No 1 is streaming at that specific guild.')
        return

    data = {
        'max_age'           : 0,
        'max_uses'          : 0,
        'temporary'         : False,
        'unique'            : True,
        'target_user_type'  : 1,
        'target_user_id'    : voice_state.user.id,
            }

    try:
        data = await client.http.invite_create(channel.id,data)
    except DiscordException as err:
        result=repr(err)
    else:
        result=repr(data)
        await client.http.invite_delete(data['code'],'just testin')

    await client.message_create(channel,result)

#works
@commands
async def target_user_stream_test_1(client,message,content):
    if not client.is_owner(message.author):
        return

    channel=message.channel
    guild=channel.guild
    if guild is None:
        await client.message_create(channel,'Guild only!')
        return

    for channel_ in guild.all_channel.values():
        if channel_.type==5:
            target_channel_id=channel.id
            break
    else:
        await client.message_create(channel,'No NEWS channel found at the guild!')
        return

    voice_states=guild.voice_states
    if not voice_states:
        await client.message_create(channel,'No voice state at the guild.')
        return

    for voice_state in voice_states.values():
        if voice_state.self_video:
            break
    else:
        await client.message_create(channel,'No 1 is streaming at that specific guild.')
        return

    data = {
        'max_age'           : 0,
        'max_uses'          : 0,
        'temporary'         : False,
        'unique'            : True,
        'target_user_type'  : 1,
        'target_user_id'    : voice_state.user.id,
            }

    try:
        data = await client.http.invite_create(target_channel_id,data)
    except DiscordException as err:
        result=repr(err)
    else:
        result=repr(data)
        await client.http.invite_delete(data['code'],'just testin')

    await client.message_create(channel,result)

#url works as well
@commands
async def target_user_stream_test_url(client,message,content):
    if not client.is_owner(message.author):
        return

    channel=message.channel
    guild=channel.guild
    if guild is None:
        await client.message_create(channel,'Guild only!')
        return

    voice_states=guild.voice_states
    if not voice_states:
        await client.message_create(channel,'No voice state at the guild.')
        return

    for voice_state in voice_states.values():
        if voice_state.self_video:
            break
    else:
        await client.message_create(channel,'No 1 is streaming at that specific guild.')
        return

    data = {
        'max_age'           : 0,
        'max_uses'          : 0,
        'temporary'         : False,
        'unique'            : True,
        'target_user_type'  : 1,
        'target_user_id'    : voice_state.user.id,
            }

    try:
        data = await client.http.invite_create(voice_state.channel.id,data)
    except DiscordException as err:
        result=repr(err)
    else:
        invite=Invite(data)
        result=invite.url

    await client.message_create(channel,result)

#works
@commands
async def follow_test(client,message,content):
    if not client.is_owner(message.author):
        return

    content=filter_content(content)
    if len(content)<2:
        await client.message_create(message.channel,'Please include 2 channel ids.')
        return

    try:
        source_channel_id=int(content[0])
    except ValueError:
        await client.message_create(message.channel,'Source channel id is not integer.')
        return

    try:
        target_channel_id=int(content[1])
    except ValueError:
        await client.message_create(message.channel,'Target channel id is not integer.')
        return

    try:
        source_channel=CHANNELS[source_channel_id]
    except KeyError:
        await client.message_create(message.channel,'I dont share a guild with that source channel.')
        return

    try:
        target_channel=CHANNELS[target_channel_id]
    except KeyError:
        await client.message_create(message.channel,'I dont share a guild with the target channel.')
        return

    try:
        webhook = await client.channel_follow(source_channel,target_channel)
    except ValueError as err:
        text=err.args[0]
    except BaseException as err:
        text=''.join(client.loop.run_in_exceutor(alchemy_incendiary,render_exc_to_list,(err,),),)
    else:
        text=pconnect(webhook)

    await client.message_create(message.channel,text)

#works
@commands
async def show_invite_data(client,message,content):
    if not client.is_owner(message.author):
        return
    
    data = await client.http.invite_get(content,{'with_counts':True})
    text=repr(data)
    await client.message_create(message.channel,text)

#invite data was updated after `show_invite_data`
@commands
async def show_invite(client,message,content):
    if not client.is_owner(message.author):
        return
    invite = await client.invite_get(content)
    text=pconnect(invite)
    await client.message_create(message.channel,text)

# ContentParser functionality test
@commands
class userlist1(object):
    def __init__(self):
        self.users=[None for _ in range(10)]
        self.position=0

    @ContentParser('user, flags=mni',is_method=True)
    async def __call__(self,client,message,user):
        position=self.position
        
        users=self.users
        users[position]=user
        
        if position==9:
            position=0
        else:
            position=position+1
        self.position=position

        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel,text)

# ContentParser functionality test
@commands
@ContentParser('user, flags=mni')
class userlist2(object):
    def __init__(self):
        self.users=[None for _ in range(10)]
        self.position=0
    
    async def __call__(self,client,message,user):
        position=self.position
        
        users=self.users
        users[position]=user
        
        if position==9:
            position=0
        else:
            position=position+1
        self.position=position

        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel,text)

# ContentParser functionality test
class UserList1(object):
    users=[None for _ in range(10)]
    position=0

    @ContentParser('user, flags=mni',is_method=True)
    async def userlist3(cls,client,message,user):
        position=cls.position
        
        users=cls.users
        users[position]=user
        
        if position==9:
            position=0
        else:
            position=position+1
        cls.position=position

        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel,text)

commands(UserList1.userlist3)

# ContentParser functionality test
class UserList2(object):
    users=[None for _ in range(10)]
    position=0

    @ContentParser('user, flags=mni',is_method=True)
    async def userlist4(cls,client,message,user):
        position=cls.position
        
        users=cls.users
        users[position]=user
        
        if position==9:
            position=0
        else:
            position=position+1
        cls.position=position

        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel,text)

    @ContentParser('user, flags=mni',is_method=True)
    async def userclear1(cls,client,message,user):
        users=cls.users
        count=0
        for index in reversed(range(len(users))):
            user_=users[index]
            if user_ is user:
                del users[index]
                users.append(None)
                count+=1
        
        await client.message_create(message.channel,f'{user:f} removed {count} times.')

    @classmethod
    async def usershow1(cls,client,message,content):
        users=cls.users
        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        if names:
            text=', '.join(names)
        else:
            text='No users are added yet.'
        
        await client.message_create(message.channel,text)
    
commands(UserList2.userlist4)
commands(UserList2.userclear1)
commands(UserList2.usershow1)

# ContentParser functionality test
@commands
class userlist5(object):
    def __init__(self):
        self.users=[None for _ in range(10)]
        self.position=0

    @ContentParser('str, default="\'\'"', 'rest', is_method=True)
    async def __call__(self,client,message,subcommand,rest):
        subcommand=subcommand.lower()
        if subcommand=='add':
            await self.add(client,message,rest)
            return
        
        if subcommand=='clear':
            await self.clear(client,message,rest)
            return

        if subcommand=='show':
            await self.show(client,message)
            return

        await self.help(client,message)

    @ContentParser('user, flags=mni',is_method=True)
    async def add(self,client,message,user):
        position=self.position
        
        users=self.users
        users[position]=user
        
        if position==9:
            position=0
        else:
            position=position+1
        self.position=position

        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        text=', '.join(names)
        
        await client.message_create(message.channel,text)

    @ContentParser('user, flags=mni',is_method=True)
    async def clear(self,client,message,user):
        users=self.users
        count=0
        for index in reversed(range(len(users))):
            user_=users[index]
            if user_ is user:
                del users[index]
                users.append(None)
                count+=1
        
        await client.message_create(message.channel,f'{user:f} removed {count} times.')

    async def show(self,client,message):
        users=self.users
        names=[]
        for user in users:
            if user is None:
                break
            names.append(user.full_name)

        if names:
            text=', '.join(names)
        else:
            text='No users are added yet.'
        
        await client.message_create(message.channel,text)

    async def help(self,client,message):
        prefix=client.events.message_create.prefix(message)
        text = (
            f'Use `{prefix}userlist add *user*` to add a user to the list.\n'
            f'Use `{prefix}userlist clear *user*` to clear a user from the list.\n'
            f'Use `{prefix}userlist show` to show up the list of the user.'
                )
        await client.message_create(message.channel,text)

#checking new emoji by one
@commands
async def is_emoji(client,message,content):
    emoji=parse_emoji(content)
    
    if emoji is None:
        result = content.encode().__repr__()
    else:
        result = 'yes'
        
    await client.message_create(message.channel,result)

# keep checking new emojis class
@commands
class keep_checking_emoji(object):
    __slots__=('channel',)
    def __init__(self):
        self.channel=None
        
    async def __call__(self,client,message,content):
        if not client.is_owner(message.author):
            return
        
        content=content.lower()

        if content=='start':
            channel=self.channel
            if channel is not None:
                client.events.message_create.remove(self.worker(self),channel)
            
            channel=message.channel
            client.events.message_create.append(self.worker(self),channel)
            self.channel=channel
            return

        if content=='stop':
            channel=self.channel
            if channel is not None:
                client.events.message_create.remove(self.worker(self),channel)
            self.channel=None
            return
        
    @staticmethod
    class worker(object):
        __slots__=('client',)
        def __init__(self,client):
            self.client=client
            
        async def __call__(self,message):
            if not self.client.is_owner(message.author):
                return
    
            content=message.content
            emoji=parse_emoji(content)
            
            if emoji is None:
                result = f'new : {content.encode()!r}'
            else:
                result = 'old'
    
            await self.client.message_create(message.channel,result)
            
    def __eq__(self,other):
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.client is other.client)
    
    def unload(self,client):
        channel=self.channel
        if channel is None:
            return
        
        client.events.message_create.remove(self.worker(self),channel)
        
#keep checking more emojis command
@commands
async def multy_emoji_test(client,message,content):
    if not client.is_owner(message.author):
        return
    
    message = await client.message_create(message.channel,
        'Will add 2 same emojis, lets se, what happens')

    emoji=BUILTIN_EMOJIS['heart']
    await client.reaction_add(message,emoji)

    emoji=BUILTIN_EMOJIS['heart_old']
    try:
        await client.reaction_add(message,emoji)
    except DiscordException as err:
        await client.message_create(message.channel,err.__repr__())

# CustomLinkCommand for Proxy

CLC_RP=re.compile('CustomLinkCommand[ \n\t]*(\d{7,21})[ \n\t]*')

class CustomLinkCommand(object):
    INSTANCES=WeakSet()
    __slots__ = ('__weakref__', 'client', 'channel',)
    def __init__(self,client, channel):
        self.client=client
        self.channel=channel
        self.INSTANCES.add(self)
        
    async def __call__(self, message):
        if message.author.id != 184734189386465281:
            return

        content = message.clean_content
        parsed = CLC_RP.match(content)
        if parsed is None:
            return

        if parsed.end() == len(content):
            return
        
        channel_id = int(parsed.group(1))
        try:
            channel = CHANNELS[channel_id]
        except KeyError:
            return

        content = content[parsed.end():]
        
        await self.client.message_create(channel,content)

    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        return (self.client is other.client)
    
    @classmethod
    def unload(cls,client):
        for entity in CustomLinkCommand.INSTANCES:
            client.events.message_create.remove(entity,entity.channel)
        
@commands
async def CustomLinkCommand_on(client, message, content):
    if not client.is_owner(message.author):
        return
    
    channel=message.channel
    client.events.message_create.append(CustomLinkCommand(client,channel),channel)

@commands
async def CustomLinkCommand_off(client, message, content):
    if not client.is_owner(message.author):
        return
    
    channel=message.channel
    client.events.message_create.remove(CustomLinkCommand(client,channel),channel)
    
# shows the representation of AuditLogEntry-s
@commands
async def test_logs_entry_repr(client, message, content):
    if not client.is_owner(message.author):
        return
    
    guild=message.guild
    if guild is None:
        await client.message_create(message.channel,'Guild only')
        return
    
    if not guild.cached_permissions_for(client).can_view_audit_log:
        await client.message_create(message.channel,
            'I have no permissions at the guild, to request audit logs.')
        return
    
    with client.keep_typing(message.channel):
        iterator = client.audit_log_iterator(guild,)
        await iterator.load_all()
        logs = iterator.transform()
    
    if not logs:
        await client.message_create(message.channel,'The guild has no logs.')
        return
        
    pages=[]
    page=Embed()
    pages.append(page)
    field_count=0
    
    index=0
    limit=len(logs)
    
    while True:
        if index==limit:
            break
            
        page.add_field(f'entry {index}',logs[index].__repr__())
        
        field_count=field_count+1
        index=index+1
        
        if field_count!=20:
            continue
        
        field_count=0
        
        # dont create a new page if we are at the end
        if index==limit:
            break
            
        page=Embed()
        pages.append(page)
    
    await Pagination(client,message.channel,pages)

# list AuditLogChange's data science

class log_change_type_collecter(object):
    def __init__(self,name):
        self.name=name
        self.before_types=set()
        self.after_types=set()
        
@commands
async def test_logs_changes(client, message, content):
    if not client.is_owner(message.author):
        return
    
    guild=message.guild
    if guild is None:
        await client.message_create(message.channel,'Guild only')
        return
    
    if not guild.cached_permissions_for(client).can_view_audit_log:
        await client.message_create(message.channel,
            'I have no permissions at the guild, to request audit logs.')
        return
    
    with client.keep_typing(message.channel):
        iterator = client.audit_log_iterator(guild,)
        await iterator.load_all()
        logs = iterator.transform()
    
    if not logs:
        await client.message_create(message.channel,'The guild has no logs.')
        return
    
    changes = []
    for entry in logs:
        changes_=entry.changes
        if changes_ is None:
            continue
        
        changes.extend(changes_)
    
    if not changes:
        await client.message_create(message.channel,'The guild has no changes.')
        return
    
    # short
    index=0
    limit=len(changes)
    collectors={}
    
    while True:
        if index==limit:
            break
        
        change=changes[index]
        index=index+1
        
        name=change.attr
        try:
            collector=collectors[name]
        except KeyError:
            collector=log_change_type_collecter(name)
            collectors[name]=collector
        
        before=change.before
        if before is None:
            type_=None
        else:
            type_=type(before)
            if type_ is Unknown:
                type_=before.type
        
        collector.before_types.add(type_)
        
        after=change.after
        if after is None:
            type_=None
        else:
            type_=type(after)
            if type_ is Unknown:
                type_=after.type
        
        collector.after_types.add(type_)
    
    pages=[]
    page=Embed()
    pages.append(page)
    content_parts=[]
    field_count=0
    
    limit=len(collectors)
    index=0
    
    for collector in collectors.values():
        
        content_parts.append('**befores:**')
        for before in collector.before_types:
            content_parts.append(repr(before))
            content_parts.append(', ')
        
        del content_parts[-1]
        
        content_parts.append('\n**afters:**')
        for after in collector.after_types:
            content_parts.append(repr(after))
            content_parts.append(', ')
        
        del content_parts[-1]
        
        content=''.join(content_parts)
        content_parts.clear()
        
        page.add_field(collector.name,content)
        
        field_count=field_count+1
        index=index+1
        
        if field_count!=20:
            continue
        
        field_count=0
        
        # dont create a new page if we are at the end
        if index==limit:
            break
            
        page=Embed()
        pages.append(page)
        
    await Pagination(client,message.channel,pages)

# do not connects the messages somewhy
@commands
async def test_multyimage(client, message, content):
    if not client.is_owner(message.author):
        return
    
    avatar_url=client.avatar_url_as(size=4096)
    embed=Embed(client.full_name)
    embed.add_image(avatar_url)
    embeds=[embed]
    for _ in range(3):
        embed=Embed()
        embed.add_image(avatar_url)
        embeds.append(embed)

    webhooks = await client.webhook_get_channel(message.channel)
    if webhooks:
        webhook = webhooks[0]
    else:
        webhook = await client.webhook_create(message.channel,'UwU')
    
    await client.webhook_send(webhook,embed=embeds,name=message.author.name,avatar_url=message.author.avatar_url)
    

@commands
async def test_suppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    try:
        await client.message_suppress_embeds(message)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
@commands
async def test_unsuppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    try:
        await client.message_suppress_embeds(message,suppress=False)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return

@commands
async def test_get_suppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    content = ('False','True')[message.flags.embeds_suppressed]
    await client.message_create(message.channel,content)

@commands
async def test_get_could_suppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    content = ('False','True')[message.could_suppress_embeds]
    await client.message_create(message.channel,content)

@commands
async def test_edit_suppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    if message.author!=client:
        await client.message_create(message.channel,'The message must be sent by me')
        return

    if message.embeds is None:
        await client.message_create(message.channel,'The message must have embeds')
        return
    
    if message.flags.embeds_suppressed:
        await client.message_create(message.channel,'The message\'s embeds must be not unsupressed')
        return
    
    data={'flags':message.flags|4}
    try:
        await client.http.message_edit(message.channel.id,message.id,data)
    except DiscordException as err:
        content=repr(err)
    else:
        content='OwO?'
    
    await client.message_create(message.channel,content)

@commands
async def test_edit_unsuppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    if message.author!=client:
        await client.message_create(message.channel,'The message must be sent by me')
        return
    
    if not message.flags.embeds_suppressed:
        await client.message_create(message.channel,'The message\'s embeds must be supressed')
        return
    
    data={'flags':message.flags^4}
    try:
        await client.http.message_edit(message.channel.id,message.id,data)
    except DiscordException as err:
        content=repr(err)
    else:
        content='UwU?'
    
    await client.message_create(message.channel,content)

@commands
async def test_message_edit_suppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    if message.author!=client:
        await client.message_create(message.channel,'The message must be sent by me')
        return
    
    if message.flags.embeds_suppressed:
        await client.message_create(message.channel,'The message\'s embeds must be not supressed')
        return
    
    await client.message_edit(message,suppress=True)
    
@commands
async def test_message_edit_unsuppress(client, message, content):
    if not client.is_owner(message.author):
        return
    
    try:
        message_id=int(content)
    except ValueError:
        await client.message_create(message.channel,'Id please')
        return
        
    try:
        message = await client.message_get(message.channel,message_id)
    except DiscordException as err:
        await client.message_create(message.channel,repr(err))
        return
    
    if message.author!=client:
        await client.message_create(message.channel,'The message must be sent by me')
        return
    
    if not message.flags.embeds_suppressed:
        await client.message_create(message.channel,'The message\'s embeds must be supressed')
        return
    
    await client.message_edit(message,suppress=False)

class Timeouter(object):
    __slots__=('loop', 'handler', 'owner', 'timeout')
    def __init__(self,loop,owner,timeout):
        self.loop=loop
        self.owner=owner
        self.timeout=timeout
        self.handler=loop.call_later(timeout,self.__step,self)
        
    @staticmethod
    def __step(self):
        timeout=self.timeout
        if timeout>0.0:
            self.handler=self.loop.call_later(timeout,self.__step,self)
            self.timeout=0.0
            return
        
        self.handler=None
        owner=self.owner
        if owner is None:
            return
        
        self.owner=None
        
        canceller=owner.canceller
        if canceller is None:
            return
        owner.canceller=None
        Task(canceller(owner,TimeoutError()),self.loop)
        
        
    def cancel(self):
        handler=self.handler
        if handler is None:
            return
        
        self.handler=None
        handler.cancel()
        self.owner=None

class NewGenerationPagination(object):
    LEFT2   = BUILTIN_EMOJIS['track_previous']
    LEFT    = BUILTIN_EMOJIS['arrow_backward']
    RIGHT   = BUILTIN_EMOJIS['arrow_forward']
    RIGHT2  = BUILTIN_EMOJIS['track_next']
    CANCEL  = BUILTIN_EMOJIS['x']
    EMOJIS  = (LEFT2,LEFT,RIGHT,RIGHT2,CANCEL,)
    
    __slots__=('canceller', 'channel', 'client', 'message', 'page', 'pages',
        'task_flag', 'timeouter')
    
    async def __new__(cls,client,channel,pages,timeout=240.,message=None):
        self=object.__new__(cls)
        self.client=client
        self.channel=channel
        self.pages=pages
        self.page=0
        self.canceller=cls._canceller
        self.task_flag=GUI_STATE_READY
        self.message=message
        self.timeouter=None
        
        if message is None:
            message = await client.message_create(channel,embed=pages[0])
            self.message=message
        
        if not channel.cached_permissions_for(client).can_add_reactions:
            return self

        message.weakrefer()
        
        if len(self.pages)>1:
            for emoji in self.EMOJIS:
                await client.reaction_add(message,emoji)
        else:
            await client.reaction_add(message,self.CANCEL)
        
        self.timeouter=Timeouter(client.loop,self,timeout=timeout)
        client.events.reaction_add.append(self,message)
        client.events.reaction_delete.append(self,message)
        return self
    
    async def __call__(self,client,emoji,user):
        if user.is_bot or (emoji not in self.EMOJIS):
            return
        
        message=self.message
        
        can_manage_messages=self.channel.cached_permissions_for(client).can_manage_messages
        if can_manage_messages:
            if not message.did_react(emoji,user):
                return
            Task(self.reaction_remove(client,message,emoji,user),client.loop)
        
        task_flag=self.task_flag
        if task_flag!=GUI_STATE_READY:
            if task_flag==GUI_STATE_SWITCHING_PAGE:
                if emoji is self.CANCEL:
                    self.task_flag=GUI_STATE_CANCELLING
                return

            # ignore GUI_STATE_CANCELLED and GUI_STATE_SWITCHING_CTX
            return
        
        while True:
            if emoji is self.LEFT:
                page=self.page-1
                break
                
            if emoji is self.RIGHT:
                page=self.page+1
                break
                
            if emoji is self.CANCEL:
                self.task_flag=GUI_STATE_CANCELLED
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass
                self.cancel()
                return
            
            if emoji is self.LEFT2:
                page=0
                break
                
            if emoji is self.RIGHT2:
                page=len(self.pages)-1
                break
            
            return
        
        if page<0:
            page=0
        elif page>=len(self.pages):
            page=len(self.pages)-1
        
        if self.page==page:
            return

        self.page=page
        self.task_flag=GUI_STATE_SWITCHING_PAGE
        
        try:
            await client.message_edit(message,embed=self.pages[page])
        except DiscordException:
            self.task_flag=GUI_STATE_CANCELLED
            self.cancel()
            return
        
        if self.task_flag==GUI_STATE_CANCELLING:
            self.task_flag=GUI_STATE_CANCELLED
            if can_manage_messages:
                try:
                    await client.message_delete(message)
                except DiscordException:
                    pass

            self.cancel()
            return
            
        self.task_flag=GUI_STATE_READY
        
        timeouter=self.timeouter
        if timeouter.timeout<240.:
            timeouter.timeout+=30.
            
    @staticmethod
    async def reaction_remove(client,message,emoji,user):
        try:
            await client.reaction_delete(message,emoji,user)
        except DiscordException:
            pass
    
    async def _canceller(self,exception,):
        client=self.client
        message=self.message
        
        client.events.reaction_add.remove(self,message)
        client.events.reaction_delete.remove(self,message)
        
        if self.task_flag==GUI_STATE_SWITCHING_CTX:
            # the message is not our, we should not do anything with it.
            return

        self.task_flag=GUI_STATE_CANCELLED
        
        if exception is None:
            return
        
        if isinstance(exception,TimeoutError):
            if self.channel.cached_permissions_for(client).can_manage_messages:
                try:
                    await client.reaction_clear(message)
                except DiscordException:
                    pass
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        #we do nothing
    
    def cancel(self):
        canceller=self.canceller
        if canceller is None:
            return
        
        self.canceller=None
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,None),self.client.loop)
    
    def __repr__(self):
        result = [
            '<', self.__class__.__name__,
            ' pages=', repr(len(self.pages)),
            ', page=', repr(self.page),
            ', channel=', repr(self.channel),
            ', task_flag='
                ]
        
        task_flag=self.task_flag
        result.append(repr(task_flag))
        result.append(' (')
        
        task_flag_name = (
            'GUI_STATE_READY',
            'GUI_STATE_SWITCHING_PAGE',
            'GUI_STATE_CANCELLING',
            'GUI_STATE_CANCELLED',
            'GUI_STATE_SWITCHING_CTX',
                )[task_flag]
        
        result.append(task_flag_name)
        result.append(')>')
        
        return ''.join(result)


class NewGenerationWaitAndContinue(object):
    __slots__=('canceller', 'check', 'event', 'future', 'target', 'timeouter')
    def __init__(self, future, check, target, event, timeout):
        self.canceller=self.__class__._canceller
        self.future=future
        self.check=check
        self.event=event
        self.target=target
        self.timeouter=Timeouter(future._loop,self,timeout)
        event.append(self,target)
        
    async def __call__(self, client, *args):
        result = self.check(*args)
        if type(result) is bool:
            if not result:
                return
                
            if len(args)==1:
                self.future.set_result_if_pending(args[0],)
            else:
                self.future.set_result_if_pending(args,)
        
        else:
            args=(*args,result,)
            self.future.set_result_if_pending(args,)
        
        self.cancel()
        
    async def _canceller(self,exception):
        self.event.remove(self,self.target)
        if exception is None:
            self.future.set_result_if_pending(None)
            return
        
        self.future.set_exception_if_pending(exception)
        
        if not isinstance(exception,TimeoutError):
            return

        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
    def cancel(self):
        canceller=self.canceller
        if canceller is None:
            return
        
        timeouter=self.timeouter
        if timeouter is not None:
            timeouter.cancel()
        
        return Task(canceller(self,None),self.future._loop)
    
    
def new_generation_wait_for_reaction(client,message,case,timeout):
    future=Future(client.loop)
    NewGenerationWaitAndContinue(future,case,message,client.events.reaction_add,timeout)
    return future

def new_generation_wait_for_message(client,channel,case,timeout):
    future=Future(client.loop)
    NewGenerationWaitAndContinue(future,case,channel,client.events.message_create,timeout)
    return future

def test_new_generation_match(*args):
    for arg in args:
        if arg is not None:
            return False
    
    return True

class test_new_generation_case_message_delete(object):
    __slots__=('message')
    def __new__(cls,message):
        self=object.__new__(cls)
        self.message=message
        return self
        
    def __call__(self,message):
        return (self.message is message)
    
def test_new_generation_wait_for_message_delete(client,message,timeout):
    future=Future(client.loop)
    case=test_new_generation_case_message_delete(message)
    NewGenerationWaitAndContinue(future,case,message.channel,client.events.message_delete,timeout)
    return future

class MessageDeleteAltPatcher(EventHandlerBase):
    __slots__=('original', 'waitfors',)
    __event_name__='message_delete'
    
    @classmethod
    def apply(cls,client):
        actual=client.events.message_delete
        if actual is EventDescriptor.DEFAULT_EVENT:
            self=object.__new__(cls)
            self.original=None
            self.waitfors=WeakKeyDictionary()
            client.events.message_create=self
            return
        
        if hasattr(actual,'append') and hasattr(actual,'remove'):
            return
        
        self=object.__new__(cls)
        self.original=actual
        self.waitfors=WeakKeyDictionary()
        client.events.message_create=self
        return
        
    @classmethod
    def detach(cls,client):
        actual=client.events.message_delete
        if type(actual) is not cls:
            return
            
        original=actual.original
        if original is None:
            del client.events.message_delete
            return
        
        client.events.message_delete=original
            
    
    append=CommandProcesser.append
    remove=CommandProcesser.remove
    
    async def __call__(self,client,message):
        try:
            event=self.waitfors[message.channel]
        except KeyError:
            return
        
        if type(event) is asynclist:
            for event in event:
                Task(event(client,message),client.loop)
        else:
            Task(event(client,message),client.loop)
        
        original=self.original
        if original is None:
            return
        
        await original(client,message)
        
@commands
async def test_new_generation(client, message, content):
    if not client.is_owner(message.author):
        return
    
    channel=message.channel
    user=message.author
    
    # Test 1
    while True:
        pagination=None
        pages=[Embed(f'Page 1')]
        
        try:
            pagination = await NewGenerationPagination(client,channel,pages)
        except DiscordException as err:
            with StringIO() as buffer:
                await client.loop.render_exc_async(err,'Test 1 failed:\n\n',file=buffer)
                content=buffer.getvalue()
            break
        
        await sleep(0.1,client.loop)
        
        reaction_amount=len(pagination.message.reactions)
        if reaction_amount!=1:
            content = f'Test 1 failed:\nExpected 1 reaction on the pagination, found {reaction_amount}.'
            break
        
        content = 'Test 1 passed.'
        break
        
    await client.message_create(channel,content)
    
    if pagination is not None:
        try:
            await client.message_delete(pagination.message)
        except DiscordException:
            pass
    
    # Test 2
    while True:
        pagination=None
        pages=[]
        for index in range(1,6):
            pages.append(Embed(f'Page {index}'))
        
        try:
            pagination = await NewGenerationPagination(client,message.channel,pages)
        except DiscordException as err:
            with StringIO() as buffer:
                await client.loop.render_exc_async(err,'Test 2 failed:\n\n',file=buffer)
                content=buffer.getvalue()
            break
        
        await sleep(0.1,client.loop)
        
        reaction_amount=len(pagination.message.reactions)
        if reaction_amount!=5:
            content = f'Test 2 failed:\nExpected 5 reaction on the pagination, found {reaction_amount}.'
            break
            
        content = 'Test 2 passed.'
        break
        
    await client.message_create(message.channel,content)
    
    if pagination is not None:
        try:
            await client.message_delete(pagination.message)
        except DiscordException:
            pass
    
    # Test 3
    while True:
        pagination=None
        
        pages=[]
        for index in range(1,6):
            pages.append(Embed(f'Page {index}'))
        
        try:
            pagination = await NewGenerationPagination(client,message.channel,pages)
        except DiscordException as err:
            with StringIO() as buffer:
                await client.loop.render_exc_async(err,'Test 3 failed:\n\n',file=buffer)
                content=buffer.getvalue()
            break
            
        await sleep(0.1,client.loop)
        
        pagination.message.reactions[NewGenerationPagination.RIGHT].add(user)
        try:
            await pagination(client,NewGenerationPagination.RIGHT,user)
        except DiscordException as err:
            with StringIO() as buffer:
                await client.loop.render_exc_async(err,'Test 3 failed:\n\n',file=buffer)
                content=buffer.getvalue()
            break
        
        await sleep(0.1,client.loop)
        
        page=pagination.page
        if page!=1:
            content=f'Test 3 failed:\nExpected to be on page 1, but we are on page {page}'
            break
        
        embeds=pagination.message.embeds
        if embeds is None:
            content=f'Test 3 failed:\nExpected the page to have embed `Page 2`, but it does not even has any.'
            break
            
        if pages[1]!=embeds[0]:
            content=f'Test 3 failed:\nExpected the pagination to have `Page 2`, but has something else.'
            break
        
        content='Test 3 passed.'
        break
    
    await client.message_create(message.channel,content)
    
    if pagination is not None:
        try:
            await client.message_delete(pagination.message)
        except DiscordException:
            pass
    
    # Test 4
    MessageDeleteAltPatcher.apply(client)
    while True:
        pagination=None
        
        pages=[]
        for index in range(1,3):
            pages.append(Embed(f'Page {index}'))
        
        try:
            pagination = await NewGenerationPagination(client,channel,pages)
        except DiscordException as err:
            with StringIO() as buffer:
                await client.loop.render_exc_async(err,'Test 4 failed:\n\n',file=buffer)
                content=buffer.getvalue()
            break
        
        await sleep(0.4,client.loop)
        
        future=test_new_generation_wait_for_message_delete(client,pagination.message,2.0)
        
        pagination.message.reactions[NewGenerationPagination.CANCEL].add(user)
        try:
            await pagination(client,NewGenerationPagination.CANCEL,user)
        except DiscordException as err:
            future.cancel()
            with StringIO() as buffer:
                await client.loop.render_exc_async(err,'Test 3 failed:\n\n',file=buffer)
                content=buffer.getvalue()
            break
        
        try:
            await future
        except TimeoutError:
            content = f'Test 4 failed:\nExpected message deletetion but timeouted after 2s.'
            break
            
        content = 'Test 4 passed.'
        break
    MessageDeleteAltPatcher.detach(client)
    
    await client.message_create(channel,content)
    
    if pagination is not None:
        try:
            await client.message_delete(pagination.message)
        except DiscordException:
            pass
    
    # Test 5
    while True:
        pagination=None
        
        pages=[]
        for index in range(1,3):
            pages.append(Embed(f'Page {index}'))
        
        try:
            pagination = await NewGenerationPagination(client,channel,pages,timeout=0.5)
        except DiscordException as err:
            with StringIO() as buffer:
                await client.loop.render_exc_async(err,'Test 5 failed:\n\n',file=buffer)
                content=buffer.getvalue()
            break
        
        await sleep(3.0,client.loop)
        
        reaction_amount=len(pagination.message.reactions)
        if reaction_amount!=0:
            content = f'Test 5 failed:\nExpected 0 reaction on the pagination, found {reaction_amount}.'
            break
            
        content = 'Test 5 passed.'
        break
    
    await client.message_create(channel,content)
    
    if pagination is not None:
        try:
            await client.message_delete(pagination.message)
        except DiscordException:
            pass
    
    # Test 6
    while True:
        future=new_generation_wait_for_message(client,channel,test_new_generation_match,0.3)
        if __debug__:
            future.__silence__()
        
        waitfors=client.events.message_create.waitfors
        try:
            event=waitfors[channel]
        except KeyError:
            content='Test 6 failed:\nWaitfor event is added, but not found.\n(None at channel)'
            break
            
        if type(event) is asynclist:
            found=False
            for event in event:
                if type(event) is NewGenerationWaitAndContinue:
                    found=True
                    break
            
            if not found:
                content='Test 6 failed:\nWaitfor event is added, but not found.\n(Expects more, but no correct)'
                break
        else:
            if type(event) is not NewGenerationWaitAndContinue:
                content='Test 6 failed:\nWaitfor event is added, but not found.\n(1:1 no correct)'
                break
        
        await event(None)
        await sleep(0.1,client.loop)
        
        try:
            await future
        except TimeoutError:
            content = f'Test 6 failed:\nExpected `None` result, received `TimeoutError`.'
            break
    
        await sleep(0.1,client.loop)

        try:
            event=waitfors[channel]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                found=False
                for event in event:
                    if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                        found=True
                        break
                
                if found:
                    content='Test 6 failed:\nWaitfor event should be removed, but still found.\n(Expects more and matched)'
                    break
            else:
                if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                    content='Test 6 failed:\nWaitfor event should be removed, but still found.\n(1:1 match).'
                    break
        
        content = 'Test 6 passed'
        break
    
    await client.message_create(channel,content)
    
    # Test 7
    while True:
        future=new_generation_wait_for_message(client,channel,test_new_generation_match,0.1)
        if __debug__:
            future.__silence__()
            
        waitfors=client.events.message_create.waitfors
        try:
            event=waitfors[channel]
        except KeyError:
            content='Test 7 failed:\nWaitfor event is added, but not found.\n(None at channel)'
            break
            
        if type(event) is asynclist:
            found=False
            for event in event:
                if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                    found=True
                    break
            
            if not found:
                content='Test 7 failed:\nWaitfor event is added, but not found.\n(Excepts more, but not correct)'
                break
        else:
            if not (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                content='Test 7 failed:\nWaitfor event is added, but not found.\n(1:1 no match)'
                break
        
        await sleep(0.3,client.loop)
        
        try:
            await future
        except TimeoutError:
            pass
        else:
            content = f'Test 7 failed:\nExpected `TimeoutError` result, received `None`.'
            break
    
        await sleep(0.1,client.loop)

        try:
            event=waitfors[channel]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                found=False
                for event in event:
                    if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                        found=True
                        break
                
                if found:
                    content='Test 7 failed:\nWaitfor sould be removed, but still found.\n(Expects more and matched)'
                    break
            else:
                if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                    content='Test 7 failed:\nWaitfor event is removed, but still found.\n(1:1 match)'
                    break
        
        content = 'Test 7 passed.'
        break
    
    await client.message_create(channel,content)
    
    # Test 8
    while True:
        future=new_generation_wait_for_reaction(client,message,test_new_generation_match,0.3)
        if __debug__:
            future.__silence__()
            
        waitfors=client.events.reaction_add.waitfors
        try:
            event=waitfors[message]
        except KeyError:
            content='Test 8 failed:\nWaitfor event is added, but not found.\n(None at channel)'
            break
            
        if type(event) is asynclist:
            found=False
            for event in event:
                if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                    found=True
                    break
            
            if not found:
                content='Test 8 failed:\nWaitfor event is added, but not found.\n(Expects more, but not correct)'
                break
        else:
            if not (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                content='Test 8 failed:\nWaitfor event is added, but not found.\n(1:1 no match)'
                break
    
        await event(None,None)
        await sleep(0.1,client.loop)
        
        try:
            await future
        except TimeoutError:
            content = f'Test 8 failed:\nExpected `None` result, received `TimeoutError`.'
            break
    
        await sleep(0.1,client.loop)

        try:
            event=waitfors[message]
        except KeyError:
            pass
        else:
            if type(event) is asynclist:
                found=False
                for event in event:
                    if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                        found=True
                        break
                
                if found:
                    content='Test 8 failed:\nWaitfor event is removed, but still found.\n(Expects more and matched)'
                    break
            else:
                if (type(event) is NewGenerationWaitAndContinue) and (event.future is future):
                    content='Test 8 failed:\nWaitfor event is removed, but still found.\n(1:1 match)'
                    break
        
        content = 'Test 8 passed.'
        break
    
    await client.message_create(channel,content)
    
    await client.message_create(channel,'No more tests left.')
    

@commands
async def test_remove_embed(client, message, content):
    message = await client.message_create(message.channel,'content',Embed('Embed'))
    data={'embed':None}
    
    try:
        await client.http.message_edit(message.channel.id,message.id,data)
    except DiscordException as err:
        with StringIO() as buffer:
            await client.loop.render_exc_async(err,'Test 5 failed:\n\n',file=buffer)
            content=buffer.getvalue()
        await client.message_create(message.channel,content)



