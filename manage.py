# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients
from hata.activity import ActivityGame
from hata.channel import ChannelText
from hata.events import (ReactionAddWaitfor,CommandProcesser,
    ReactionDeleteWaitfor,)
from hata.webhook import Webhook
from hata.role import Role

import pers_data

import koishi
import mokou
import flan

from tools import commit_extractor,MessageDeleteWaitfor
from booru import booru_commands
from interpreter import Interpreter
import chesuto

############################## SETUP KOISHI ##############################

Koishi=Client(pers_data.KOISHI_TOKEN,
    secret=pers_data.KOISHI_SECRET,
    client_id=pers_data.KOISHI_ID,
    activity=ActivityGame.create(name='with Satori'),
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


Mokou=Client(pers_data.MOKOU_TOKEN,
    client_id=pers_data.MOKOU_ID,
        )

Mokou.events(mokou.message_create)
Mokou.events(mokou.typing)
Mokou.events(mokou.channel_delete)


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


############################## START ##############################

koishi_commands(Interpreter(locals().copy()),case='execute')
start_clients()

