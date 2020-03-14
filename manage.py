# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))

from hata import Client, start_clients, ActivityGame, ActivityWatching
from hata.events import setup_extension
from hata.extension_loader import EXTENSION_LOADER

import pers_data

import koishi
import satori
import flan

from tools import MessageDeleteWaitfor
from booru import booru_commands
from interpreter import Interpreter

koishi.KOISHI_HELPER.sort()

Koishi=Client(pers_data.KOISHI_TOKEN,
    secret=pers_data.KOISHI_SECRET,
    client_id=pers_data.KOISHI_ID,
    activity=ActivityGame.create(name='with Satori'),
    shard_count=1,
        )

Satori=Client(pers_data.SATORI_TOKEN,
    client_id=pers_data.SATORI_ID,
    activity=ActivityGame.create(name='with Koishi'),
    status='dnd',
        )

Flan=Client(pers_data.FLAN_TOKEN,
    client_id=pers_data.FLAN_ID,
    activity=ActivityWatching.create(name='Chesuto development'),
    status='idle',
        )

############################## SETUP KOISHI ##############################

setup_extension(Koishi,koishi.PREFIXES)
Koishi.events(koishi.once_on_ready)
Koishi.events(MessageDeleteWaitfor)

Koishi.commands.extend(koishi.commands)
Koishi.commands.extend(booru_commands)

############################## SETUP SATORI ##############################

satori.Koishi=Koishi #sisters, u know

setup_extension(Satori,pers_data.SATORI_PREFIX)
Satori.commands.extend(satori.commands)

############################## SETUP FLAN ##############################

setup_extension(Flan,pers_data.FLAN_PREFIX)
Flan.events(flan.guild_user_add)

Flan.commands.extend(flan.commands)

############################## START ##############################

EXTENSION_LOADER.add_default_variables(Koishi=Koishi, Satori=Satori, Flan=Flan)
EXTENSION_LOADER.add('ext.eliza')
EXTENSION_LOADER.add('ext.test_commands')
EXTENSION_LOADER.add('ext.ratelimit_tests')
EXTENSION_LOADER.load_all()

Koishi.commands(Interpreter(locals().copy()),name='execute')

start_clients()

