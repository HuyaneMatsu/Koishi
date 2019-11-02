# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients
from hata.activity import ActivityGame
from hata.channel import ChannelText, CHANNELS
from hata.events import (ReactionAddWaitfor,CommandProcesser,
    ReactionDeleteWaitfor,)
from hata.webhook import Webhook
from hata.role import Role
from hata.futures import sleep,render_exc_to_list
from hata.dereaddons_local import alchemy_incendiary
from hata.prettyprint import pconnect
from hata.invite import Invite
from hata.exceptions import DiscordException
import pers_data

import koishi
import satori
import flan

from tools import commit_extractor,MessageDeleteWaitfor
from booru import booru_commands
from interpreter import Interpreter
import chesuto



############################## SETUP KOISHI ##############################
koishi.KOISHI_HELPER.sort()

Koishi=Client(pers_data.KOISHI_TOKEN,
    secret=pers_data.KOISHI_SECRET,
    client_id=pers_data.KOISHI_ID,
    activity=ActivityGame.create(name='with Satori'),
    shard_count=1,
        )

Koishi.events(ReactionAddWaitfor)
Koishi.events(ReactionDeleteWaitfor)
Koishi.events(MessageDeleteWaitfor)
Koishi.events(koishi.once_on_ready)

koishi_commands=Koishi.events(CommandProcesser(koishi.PREFIXES)).shortcut
koishi_commands.extend(koishi.commands)
koishi_commands.extend(booru_commands)
koishi_commands(chesuto.chesuto_lobby,'lobby')
koishi_commands(chesuto.create_card,)
koishi_commands(chesuto.showcard)
koishi_commands(chesuto.massadd)
koishi_commands(chesuto.showcards)

webhook_sender=commit_extractor(
    Koishi,
    ChannelText.precreate(555476090382974999),
    Webhook.precreate(555476334210580508),
    role=Role.precreate(538397994421190657),
    color=0x2ad300,
        )

Koishi.events.message_create.append(webhook_sender,webhook_sender.channel)

############################## SETUP MOKOU ##############################


Satori=Client(pers_data.SATORI_TOKEN,
    client_id=pers_data.SATORI_ID,
        )

satori.Koishi=Koishi #sisters, u know

Satori.events(ReactionAddWaitfor)
Satori.events(ReactionDeleteWaitfor)
satori_commands=Satori.events(CommandProcesser(pers_data.SATORI_PREFIX)).shortcut
satori_commands.extend(satori.commands)


############################## SETUP ELPHELT ##############################

Flan=Client(pers_data.FLAN_TOKEN,
    client_id=pers_data.FLAN_ID,
    status='idle'
        )

Flan.events(ReactionAddWaitfor)
Flan.events(ReactionDeleteWaitfor)

flan_commands=Flan.events(CommandProcesser(pers_data.FLAN_PREFIX)).shortcut
flan_commands.extend(flan.commands)
flan_commands(Koishi.events.message_create.commands['random'])
flan_commands(chesuto.chesuto_lobby,'lobby')
flan_commands(chesuto.create_card,)
flan_commands(chesuto.showcard)
flan_commands(chesuto.massadd)
flan_commands(chesuto.showcards)

############################## TEST COMMANDS ##############################

from hata.others import filter_content
from hata.prettyprint import pchunkify
from hata.ios import ReuAsyncIO
join=os.path.join
import traceback
from hata.events import Pagination

@koishi_commands
async def achievement_create(client,message,content):
    while True:
        if not client.is_owner(message.author):
            text='Owner only'
            break
        
        content=filter_content(content)
        if len(content)<2:
            text='expected at least 2 content parts'
            break

        image_path=join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
        try:
            with (await ReuAsyncIO(image_path)) as file:
                image = await file.read()
                result = await client.achievement_create(
                    content[0],content[1],False,False,image)
        except BaseException as err:
            text=''.join([
                'at create exception occured\n',
                '\nTraceback (most recent call last):\n',
                *traceback.format_tb(err.__traceback__),
                repr(err),'\n',])
        else:
            text=repr(result)
        break
            
    await client.message_create(message.channel,text)
    
@koishi_commands
async def achievement_get_all(client,message,content):
    while True:
        if not client.is_owner(message.author):
            text='Owner only'
            break
        
        try:
            achievements = await client.achievement_get_all()
        except BaseException as err:
            text=''.join([
                'at get all: exception occured\n',
                '\nTraceback (most recent call last):\n',
                *traceback.format_tb(err.__traceback__),
                repr(err),'\n',])
            break

        chunks=pchunkify(achievements)
        pages=[{'content':chunk} for chunk in chunks]
        await Pagination(client,message.channel,pages)
        return

    await client.message_create(message.channel,text)

@koishi_commands
async def achievement_get(client,message,content):
    while True:
        if not client.is_owner(message.author):
            text='Owner only'
            break

        try:
            id_=int(content)
        except ValueError:
            text='pass id pls'
            break
        
        try:
            achievements = await client.achievement_get(id_)
        except BaseException as err:
            text=''.join([
                'at get: exception occured\n',
                '\nTraceback (most recent call last):\n',
                *traceback.format_tb(err.__traceback__),
                repr(err),'\n',])
            break

        chunks=pchunkify(achievements)
        pages=[{'content':chunk} for chunk in chunks]
        await Pagination(client,message.channel,pages)
        return

    await client.message_create(message.channel,text)

@koishi_commands
async def achievement_edit(client,message,content):
    while True:
        if not client.is_owner(message.author):
            text='Owner only'
            break

        try:
            id_=int(content)
        except ValueError:
            text='pass id pls'
            break
        
        try:
            achievement = await client.achievement_edit(id_,name='woaaa')
        except BaseException as err:
            text=''.join([
                'at edit: exception occured\n',
                '\nTraceback (most recent call last):\n',
                *traceback.format_tb(err.__traceback__),
                repr(err),'\n',])
            break

        chunks=pchunkify(achievement)
        pages=[{'content':chunk} for chunk in chunks]
        await Pagination(client,message.channel,pages)
        return

    await client.message_create(message.channel,text)
    
@koishi_commands
async def achievement_delete(client,message,content):
    while True:
        if not client.is_owner(message.author):
            text='Owner only'
            break

        try:
            id_=int(content)
        except ValueError:
            text='pass id pls'
            break
        
        try:
            achievement = await client.achievement_delete(id_)
        except BaseException as err:
            text=''.join([
                'at delete: exception occured\n',
                '\nTraceback (most recent call last):\n',
                *traceback.format_tb(err.__traceback__),
                repr(err),'\n',])
            break

        chunks=pchunkify(achievement)
        pages=[{'content':chunk} for chunk in chunks]
        await Pagination(client,message.channel,pages)
        return

    await client.message_create(message.channel,text)

@koishi_commands
async def user_achievements(client,message,content):
    while True:
        user=message.author
        if not client.is_owner(user):
            text='Owner only'
            break

        try:
            access=koishi.OA2_accesses[user.id]
        except KeyError:
            text='pls give OA link first'
            break
        
        try:
            achievements = await client.user_achievements(access)
        except BaseException as err:
            text=''.join([
                'at user\'s achievements: exception occured\n',
                '\nTraceback (most recent call last):\n',
                *traceback.format_tb(err.__traceback__),
                repr(err),'\n',])
            break

        chunks=pchunkify(achievements)
        pages=[{'content':chunk} for chunk in chunks]
        await Pagination(client,message.channel,pages)
        return

    await client.message_create(message.channel,text)

@koishi_commands
async def user_achievement_update(client,message,content):
    while True:
        if not client.is_owner(message.author):
            text='Owner only'
            break

        try:
            id_=int(content)
        except ValueError:
            text='pass id pls'
            break
        
        try:
            await client.user_achievement_update(message.author,id_,100)
        except BaseException as err:
            text=''.join([
                'at user\'s achievement update: exception occured\n',
                '\nTraceback (most recent call last):\n',
                *traceback.format_tb(err.__traceback__),
                repr(err),'\n',])
            break

        text='success'
        break

    await client.message_create(message.channel,text)
    

@koishi_commands
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

@koishi_commands
async def target_user_type_invite_test_0(client,message,content):
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

@koishi_commands
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

@koishi_commands
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

@koishi_commands
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

@koishi_commands
async def target_user_stream_test_1(client,message,content):
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
        result=repr(data)
        await client.http.invite_delete(data['code'],'just testin')

    await client.message_create(channel,result)

@koishi_commands
async def target_user_stream_test_2(client,message,content):
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

@koishi_commands
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
    
@koishi_commands
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
        text=''.join(Koishi.loop.run_in_exceutor(alchemy_incendiary,render_exc_to_list,(err,),),)
    else:
        text=pconnect(webhook)

    await client.message_create(message.channel,text)

@koishi_commands
async def show_invite_data(client,message,content):
    if not client.is_owner(message.author):
        return
    
    data = await client.http.invite_get(content,{'with_counts':True})
    text=repr(data)
    await client.message_create(message.channel,text)

@koishi_commands
async def show_invite(client,message,content):
    if not client.is_owner(message.author):
        return
    invite = await client.invite_get(content)
    text=pconnect(invite)
    await client.message_create(message.channel,text)

############################## START ##############################

koishi_commands(Interpreter(locals().copy()),case='execute')
start_clients()

