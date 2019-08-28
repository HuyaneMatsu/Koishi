# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients
from hata.activity import Activity_game
from hata.channel import Channel_text
from hata.events import (ReactionAddWaitfor,CommandProcesser,
    ReactionDeleteWaitfor,)
from hata.webhook import Webhook
from hata.role import Role

import pers_data

import koishi
import mokou
import elphelt

from tools import commit_extractor,MessageDeleteWaitfor
from booru import booru_commands
from interpreter import Interpreter
import chesuto

############################## SETUP KOISHI ##############################

Koishi=Client(pers_data.KOISHI_TOKEN,
    secret=pers_data.KOISHI_SECRET,
    client_id=pers_data.KOISHI_ID,
    activity=Activity_game.create(name='with Satori'),
        )

Koishi.events(ReactionAddWaitfor)
Koishi.events(ReactionDeleteWaitfor)
Koishi.events(MessageDeleteWaitfor)
Koishi.events(koishi.once_on_ready)

koishi_commands=Koishi.events(CommandProcesser(koishi.PREFIXES)).shortcut
koishi_commands.extend(koishi.commands)
koishi_commands.extend(booru_commands)
koishi_commands(chesuto.chesuto_lobby,'lobby')

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

Elphelt.events(ReactionAddWaitfor)
Elphelt.events(ReactionDeleteWaitfor)

elphelt_commands=Elphelt.events(CommandProcesser('/')).shortcut
elphelt_commands.extend(elphelt.commands)
elphelt_commands(Koishi.events.message_create.commands['random'])
elphelt_commands(chesuto.chesuto_lobby,'lobby')

############################## TEST COMMANDS ##############################

from hata.events_compiler import ContentParser

@koishi_commands
@ContentParser(
    'condition, flags=r, default="not client.is_owner(message.author)"',
    'str, mode="1+"')
async def test(client,message,strings):
    await client.message_create(message.channel,'\n'.join(strings))

    
############################## START ##############################

koishi_commands(Interpreter(locals().copy()),case='execute')
start_clients()

