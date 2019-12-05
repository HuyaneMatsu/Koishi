import os
from io import StringIO
from os.path import join
import re

from hata.others import filter_content
from hata.prettyprint import pchunkify
from hata.ios import ReuAsyncIO
from hata.events import Pagination
from hata.client import Achievement
from hata.others import bytes_to_base64, parse_oauth2_redirect_url
from hata.emoji import BUILTIN_EMOJIS, parse_emoji
from hata.futures import sleep, render_exc_to_list, Task
from hata.dereaddons_local import alchemy_incendiary
from hata.prettyprint import pconnect
from hata.invite import Invite
from hata.exceptions import DiscordException
from hata.embed import Embed
from hata.channel import CHANNELS
from hata.events_compiler import ContentParser
from hata.parsers import eventlist
from hata.events import wait_for_message
from weakref import WeakSet

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

# icon cannto be None
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
        
    image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
    with (await ReuAsyncIO(image_path)) as file:
        image = await file.read()

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
        await client.message_create(message.channel,'pass id pls')
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
    
@commands
async def nom(client, message, content):
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
    
    if logs:
        pages=[]
        page=Embed()
        pages.append(page)
        
        index=0
        limit=len(logs)
        field_count=0
        
        while True:
            if index==limit:
                break
                
            page.add_field(f'entry {index}',logs[index])
            
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

