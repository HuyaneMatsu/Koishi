# -*- coding: utf-8 -*-
import os

import config

from hata import Client, start_clients, ActivityRich, ActivityTypes
from hata.ext.extension_loader import EXTENSION_LOADER
from bot_utils.shared import KOISHI_PATH

MARISA_MODE = config.MARISA_MODE

EXTENSION_LOADER.add_default_variables(MARISA_MODE=MARISA_MODE)

LOCAL_DEFAULT_VARIABLES = {}

if MARISA_MODE:
    Marisa = Client(config.MARISA_TOKEN,
        client_id = config.MARISA_ID,
            )
    
    LOCAL_DEFAULT_VARIABLES['Marisa'] = Marisa
    LOCAL_DEFAULT_VARIABLES['main_client'] = Marisa
    
    EXTENSION_LOADER.load_extension('bots.marisa', locked=True, **LOCAL_DEFAULT_VARIABLES)
    
    EXTENSION_LOADER.add('bots.testers.test_commands', **LOCAL_DEFAULT_VARIABLES)
    EXTENSION_LOADER.add('bots.testers.ratelimit', **LOCAL_DEFAULT_VARIABLES)
    EXTENSION_LOADER.add('bots.testers.dispatch_tests', **LOCAL_DEFAULT_VARIABLES)
    
else:
    Koishi = Client(config.KOISHI_TOKEN,
        secret = config.KOISHI_SECRET,
        client_id = config.KOISHI_ID,
        activity = ActivityRich('with Satori'),
        shard_count = 2,
            )
    
    LOCAL_DEFAULT_VARIABLES['Koishi'] = Koishi
    LOCAL_DEFAULT_VARIABLES['main_client'] = Koishi
    
    Satori = Client(config.SATORI_TOKEN,
        secret = config.SATORI_SECRET,
        client_id = config.SATORI_ID,
        activity = ActivityRich('with Koishi'),
        status = 'dnd',
            )
    
    LOCAL_DEFAULT_VARIABLES['Satori'] = Satori
    
    Flan = Client(config.FLAN_TOKEN,
        client_id = config.FLAN_ID,
        activity = ActivityRich('Chesuto development', type_=ActivityTypes.watching),
        status = 'idle',
            )
    
    LOCAL_DEFAULT_VARIABLES['Flan'] = Flan
    
    EXTENSION_LOADER.load_extension('bots.koishi', locked=True, **LOCAL_DEFAULT_VARIABLES)
    EXTENSION_LOADER.load_extension('bots.satori', locked=True, **LOCAL_DEFAULT_VARIABLES)
    EXTENSION_LOADER.load_extension('bots.flan'  , locked=True, **LOCAL_DEFAULT_VARIABLES)

MODULE_NAMES = set()

path = None
for path in os.listdir(os.path.join(KOISHI_PATH, 'bots', 'modules')):
    if not path.endswith('.py'):
        continue
    
    MODULE_NAMES.add(path[:-3])

if MARISA_MODE:
    MARISA_ALLOWED_MODULES = set()
    
    if config.ALLOW_MARISA_SNEKBOX:
        MARISA_ALLOWED_MODULES.add('snekbox')
    
    MARISA_ALLOWED_MODULES.add('voice')
    
    for path in list(MODULE_NAMES):
        if path not in MARISA_ALLOWED_MODULES:
            MODULE_NAMES.remove(path)
    
else:
    if not config.ALLOW_KOISHI_SNEKBOX:
        try:
            MODULE_NAMES.remove('snekbox')
        except KeyError:
            pass

for path in MODULE_NAMES:
    EXTENSION_LOADER.add('bots.modules.'+path, **LOCAL_DEFAULT_VARIABLES)

del path

EXTENSION_LOADER.load_all()
