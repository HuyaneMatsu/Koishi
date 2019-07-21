# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients
from hata.activity import Activity_game
from hata.channel import Channel_text
from hata.events import (reaction_add_waitfor,command_processer,
    reaction_delete_waitfor,)
from hata.webhook import Webhook
from hata.role import Role

import pers_data

import koishi
import mokou
import elphelt

from tools import commit_extractor,message_delete_waitfor

############################## SETUP KOISHI ##############################

Koishi=Client(pers_data.KOISHI_TOKEN,
    secret=pers_data.KOISHI_SECRET,
    client_id=pers_data.KOISHI_ID,
    activity=Activity_game.create(name='with Satori'),
        )

Koishi.events(reaction_add_waitfor)
Koishi.events(reaction_delete_waitfor)
Koishi.events(message_delete_waitfor)
Koishi.events(koishi.once_on_ready)

koishi_commands=Koishi.events(command_processer(koishi.PREFIXES)).shortcut
koishi_commands.extend(koishi.commands)

webhook_sender=commit_extractor(
    Koishi,
    Channel_text.precreate(555476090382974999),
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

Elphelt=Client(pers_data.ELPHELT_TOKEN,
    client_id=pers_data.ELPHELT_ID,
               status='idle'
        )

Elphelt.events(reaction_add_waitfor)
Elphelt.events(reaction_delete_waitfor)

elphelt_commands=Elphelt.events(command_processer('/')).shortcut
elphelt_commands.extend(elphelt.commands)
elphelt_commands(Koishi.events.message_create.commands['random'])

############################## TEST COMMANDS ##############################

from hata.others import filter_content
from hata.prettyprint import pchunkify
from hata.ios import ReuAsyncIO
join=os.path.join

@koishi_commands
async def achievement_create(client,message,content):
    while True:
        if message.author is not client.owner:
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
                await client.achievement_create(client.id,
                    content[0],content[1],False,False,image)
        except BaseException as err:
            text='at create: '+str(err)
            break
        
        try:
            achievements = await client.achievement_get_all(client.id)
        except BaseException as err:
            text='at get all: '+str(err)
            break

        chunks=pchunkify(achievements)
        pages=[{'content':chunk} for chunk in chunks]
        await Pagination(client,message.channel,pages)
        return

    await client.message_create(message.channel,text)

@koishi_commands
async def achievement_get(client,message,content):
    while True:
        if message.author is not client.owner:
            text='Owner only'
            break
        try:
            achievements = await client.achievement_get_all(client.id)
        except BaseException as err:
            text='at get all: '+str(err)
            break

        chunks=pchunkify(achievements)
        pages=[{'content':chunk} for chunk in chunks]
        await Pagination(client,message.channel,pages)
        return

    await client.message_create(message.channel,text)

@koishi_commands
async def achievements_of_mine(client,message,content):
    if message.author is not client.owner:
        text='Owner only'
        await client.message_create(message.channel,text)
        return

    access=koishi.OA2_accesses[client.owner.id].access

    try:
        achievements = await client.user_achievements(access,client.id)
    except BaseException as err:
        text='at user_achievements: '+str(err)
        await client.message_create(message.channel,text)
        return

    chunks=pchunkify(achievements)
    pages=[{'content':chunk} for chunk in chunks]
    await Pagination(client,message.channel,pages)


    
    
############################## START ##############################

start_clients()

##def start_console():
##    import code
##    shell = code.InteractiveConsole(globals().copy())
##    shell.interact()
    
#start_console()
