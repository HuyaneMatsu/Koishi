# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath('..'))
# moving to the outer folder, so pers_data will count as a package

MARISA_MODE = (len(sys.argv) == 2 and sys.argv[1].lower() == 'marisa')

import config

hata_path = config.HATA_PATH
if (hata_path is not None):
    sys.path.append(hata_path)

del hata_path

from hata import Client, start_clients, ActivityRich, ActivityTypes
from hata.ext.extension_loader import EXTENSION_LOADER

EXTENSION_LOADER.add_default_variables(MARISA_MODE=MARISA_MODE)

if MARISA_MODE:
    Marisa = Client(config.MARISA_TOKEN,
        client_id = config.MARISA_ID,
            )
    
    EXTENSION_LOADER.add_default_variables(Marisa=Marisa, main_client=Marisa)
    EXTENSION_LOADER.load_extension('marisa', locked=True)
    
    EXTENSION_LOADER.add('testers.test_commands')
    EXTENSION_LOADER.add('testers.ratelimit')
    EXTENSION_LOADER.add('testers.dispatch_tests')
    
else:
    Koishi = Client(config.KOISHI_TOKEN,
        secret = config.KOISHI_SECRET,
        client_id = config.KOISHI_ID,
        activity = ActivityRich('with Satori'),
        shard_count = 2,
            )
    
    Satori = Client(config.SATORI_TOKEN,
        secret = config.SATORI_SECRET,
        client_id = config.SATORI_ID,
        activity = ActivityRich('with Koishi'),
        status = 'dnd',
            )
    
    Flan = Client(config.FLAN_TOKEN,
        client_id = config.FLAN_ID,
        activity = ActivityRich('Chesuto development', type_=ActivityTypes.watching),
        status = 'idle',
            )
    
    EXTENSION_LOADER.add_default_variables(Koishi=Koishi, Satori=Satori, Flan=Flan, main_client=Koishi)
    EXTENSION_LOADER.load_extension('koishi', locked=True)
    EXTENSION_LOADER.load_extension('satori', locked=True)
    EXTENSION_LOADER.load_extension('flan'  , locked=True)

MODULE_NAMES = set()

path = None
for path in os.listdir('modules'):
    if not path.endswith('.py'):
        continue
    
    MODULE_NAMES.add(path[:-3])

if MARISA_MODE:
    if config.ALLOW_MARISA_SNEKBOX:
        for path in list(MODULE_NAMES):
            if path != 'snekbox':
                MODULE_NAMES.remove(path)
    
else:
    if not config.ALLOW_KOISHI_SNEKBOX:
        try:
            MODULE_NAMES.remove('snekbox')
        except KeyError:
            pass

for path in MODULE_NAMES:
    EXTENSION_LOADER.add('modules.'+path)

del path

EXTENSION_LOADER.load_all()

start_clients()
