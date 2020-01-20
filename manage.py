# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client,start_clients, ActivityGame, ActivityWatching
from hata.events import ReactionAddWaitfor, CommandProcesser,               \
    ReactionDeleteWaitfor
from hata.extension_loader import ExtensionLoader

import pers_data

import koishi
import satori
import flan

from tools import MessageDeleteWaitfor
from booru import booru_commands
from interpreter import Interpreter



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

koishi_extension_loader=ExtensionLoader(Koishi)
koishi_extension_loader.add('ext.test_commands',entry_point='entry',exit_point='exit')
koishi_extension_loader.add('ext.ratelimit_tests',entry_point='entry',exit_point='exit')
koishi_extension_loader.load_all().syncwrap().wait()

############################## SETUP SATORI ##############################


Satori=Client(pers_data.SATORI_TOKEN,
    client_id=pers_data.SATORI_ID,
    activity=ActivityGame.create(name='with Koishi'),
    status='dnd',
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
    activity=ActivityWatching.create(name='Chesuto development'),
    status='idle',
        )

Flan.events(ReactionAddWaitfor)
Flan.events(ReactionDeleteWaitfor)
Flan.events(flan.guild_user_add)

flan_commands=Flan.events(CommandProcesser(pers_data.FLAN_PREFIX)).shortcut
flan_commands.extend(flan.commands)

############################## START ##############################

koishi_commands(Interpreter(locals().copy()),case='execute')
start_clients()

