# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients
from hata.activity import ActivityGame
from hata.channel import ChannelText
from hata.events import ReactionAddWaitfor, CommandProcesser,               \
    ReactionDeleteWaitfor
from hata.webhook import Webhook
from hata.role import Role
from hata.extension_loader import ExtensionLoader

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
    ChannelText.precreate(555476090382974999),
    Webhook.precreate(555476334210580508),
    role=Role.precreate(538397994421190657),
    color=0x2ad300,
        )

Koishi.events.message_create.append(webhook_sender,webhook_sender.channel)

koishi_extension_loader=ExtensionLoader(Koishi)
koishi_extension_loader.add('ext.test_commands',entry_point='entry',exit_point='exit')
koishi_extension_loader.add('ext.ratelimit_tests',entry_point='entry',exit_point='exit')
koishi_extension_loader.load_all().syncwrap().wait()

############################## SETUP SATORI ##############################


Satori=Client(pers_data.SATORI_TOKEN,
    client_id=pers_data.SATORI_ID,
        )

satori.Koishi=Koishi #sisters, u know

Satori.events(ReactionAddWaitfor)
Satori.events(ReactionDeleteWaitfor)
satori_commands=Satori.events(CommandProcesser(pers_data.SATORI_PREFIX)).shortcut
satori_commands.extend(satori.commands)

satori_extension_loader=ExtensionLoader(Satori)
satori_extension_loader.add('ext.eliza',entry_point='entry',exit_point='exit')
satori_extension_loader.load_all().syncwrap().wait()

############################## SETUP FLAN ##############################

Flan=Client(pers_data.FLAN_TOKEN,
    client_id=pers_data.FLAN_ID,
    status='idle'
        )

Flan.events(ReactionAddWaitfor)
Flan.events(ReactionDeleteWaitfor)

flan_commands=Flan.events(CommandProcesser(pers_data.FLAN_PREFIX)).shortcut
flan_commands.extend(flan.commands)
flan_commands(Koishi.events.message_create.commands['random'][1])
flan_commands(chesuto.chesuto_lobby,'lobby')
flan_commands(chesuto.create_card,)
flan_commands(chesuto.showcard)
flan_commands(chesuto.massadd)
flan_commands(chesuto.showcards)

############################## START ##############################

koishi_commands(Interpreter(locals().copy()),case='execute')
start_clients()

