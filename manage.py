# -*- coding: utf-8 -*-
import sys, os
#moving to the outer folder, so hata ll count as a package and stuffs
sys.path.append(os.path.abspath('..'))
from hata import Client, start_clients, ActivityGame, ActivityWatching
from hata.ext.extension_loader import EXTENSION_LOADER

import pers_data

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

EXTENSION_LOADER.add_default_variables(Koishi=Koishi, Satori=Satori, Flan=Flan)
EXTENSION_LOADER.load_extension('koishi', locked=True)
EXTENSION_LOADER.load_extension('satori', locked=True)
EXTENSION_LOADER.load_extension('flan'  , locked=True)

EXTENSION_LOADER.add('testers.test_commands')
EXTENSION_LOADER.add('testers.ratelimit')
EXTENSION_LOADER.add('testers.dispatch_tests')

path=None
for path in os.listdir('modules'):
    if not path.endswith('.py'):
        continue
    
    EXTENSION_LOADER.add('modules.'+path[:-3])
    
del path

EXTENSION_LOADER.load_all()

start_clients()
