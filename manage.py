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

Flan=Client(pers_data.ELPHELT_TOKEN,
    client_id=pers_data.ELPHELT_ID,
    status='idle'
        )

Flan.events(ReactionAddWaitfor)
Flan.events(ReactionDeleteWaitfor)

flan_commands=Flan.events(CommandProcesser('/')).shortcut
flan_commands.extend(flan.commands)
flan_commands(Koishi.events.message_create.commands['random'])
flan_commands(chesuto.chesuto_lobby,'lobby')
flan_commands(chesuto.create_card,)
flan_commands(chesuto.showcard)

############################## TEST COMMANDS ##############################

from hata.ios import ReuAsyncIO
from hata.embed import Embed

@koishi_commands
async def embedimage(client,message,content):
    path=os.path.join(os.path.abspath('.'),'images','0000000C_touhou_komeiji_koishi.png')
    embed=Embed('Here is an image from attachment')
    embed.add_image('attachment://image.png')
    
    with await ReuAsyncIO(path,'rb') as file:
        await client.message_create(message.channel,embed=embed,file=('image.png',file))
    
############################## START ##############################

koishi_commands(Interpreter(locals().copy()),case='execute')
start_clients()

