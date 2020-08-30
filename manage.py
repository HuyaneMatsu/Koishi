# -*- coding: utf-8 -*-
import sys, os

sys.path.append(os.path.abspath('..'))
#moving to the outer folder, so pers_data will count as a package
import pers_data

hata_path = pers_data.HATA_PATH
if (hata_path is not None):
    sys.path.append(hata_path)

del hata_path

from hata import Client, start_clients, ActivityRich, ActivityTypes
from hata.ext.extension_loader import EXTENSION_LOADER

Koishi = Client(pers_data.KOISHI_TOKEN,
    secret = pers_data.KOISHI_SECRET,
    client_id = pers_data.KOISHI_ID,
    activity = ActivityRich('with Satori'),
    shard_count = 2,
        )

Satori = Client(pers_data.SATORI_TOKEN,
    secret = pers_data.SATORI_SECRET,
    client_id = pers_data.SATORI_ID,
    activity = ActivityRich('with Koishi'),
    status = 'dnd',
        )

Flan = Client(pers_data.FLAN_TOKEN,
    client_id = pers_data.FLAN_ID,
    activity = ActivityRich('Chesuto development', type_=ActivityTypes.watching),
    status = 'idle',
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
