import os
from os.path import join as join_path, isdir as is_folder, isfile as is_file, exists

import config

from hata import Client, ActivityRich, ACTIVITY_TYPES
from hata.ext.extension_loader import EXTENSION_LOADER
from bot_utils.shared import PATH__KOISHI

from bot_utils.shared import category_name_rule, DEFAULT_CATEGORY_NAME, PREFIX__MARISA, PREFIX__FLAN, PREFIX__SATORI

MARISA_MODE = config.MARISA_MODE
EXTENSION_LOADER.add_default_variables(MARISA_MODE=MARISA_MODE)

if MARISA_MODE:
    Marisa = Client(config.MARISA_TOKEN,
        client_id = config.MARISA_ID,
        extensions = ('command_utils', 'slash', 'commands_v2'),
        prefix = PREFIX__MARISA,
        default_category_name = DEFAULT_CATEGORY_NAME,
        category_name_rule = category_name_rule,
    )
    
    EXTENSION_LOADER.add_default_variables(Marisa=Marisa, COMMAND_CLIENT=Marisa, SLASH_CLIENT=Marisa)
    
    EXTENSION_LOADER.load_extension('bots.marisa', locked=True)
    
    EXTENSION_LOADER.add('bots.testers', MAIN_CLIENT=Marisa)

else:
    Koishi = Client(config.KOISHI_TOKEN,
        secret = config.KOISHI_SECRET,
        client_id = config.KOISHI_ID,
        activity = ActivityRich('with Satori'),
        shard_count = 2,
        application_id = config.KOISHI_ID,
        extensions = ('command_utils', 'slash'),
    )
    
    EXTENSION_LOADER.add_default_variables(Koishi=Koishi, SLASH_CLIENT=Koishi)
    
    Satori = Client(config.SATORI_TOKEN,
        secret = config.SATORI_SECRET,
        client_id = config.SATORI_ID,
        activity = ActivityRich('with Koishi'),
        status = 'dnd',
        application_id = config.SATORI_ID,
        extensions = ('command_utils', 'commands_v2',),
        prefix = PREFIX__SATORI,
        category_name_rule = category_name_rule,
        default_category_name = DEFAULT_CATEGORY_NAME,
    )
    
    EXTENSION_LOADER.add_default_variables(Satori=Satori, COMMAND_CLIENT=Satori)
    
    Flan = Client(config.FLAN_TOKEN,
        client_id = config.FLAN_ID,
        activity = ActivityRich('Chesuto development', type_=ACTIVITY_TYPES.watching),
        status = 'idle',
        application_id = config.FLAN_ID,
        extensions = ('command_utils', 'commands_v2',),
        default_category_name = 'GENERAL COMMANDS',
        category_name_rule = category_name_rule,
        prefix = PREFIX__FLAN,
    )
    
    EXTENSION_LOADER.add_default_variables(Flan=Flan)
    
    Nitori = Client(config.NITORI_TOKEN,
        client_id = config.NITORI_ID,
        application_id = config.NITORI_ID,
        extensions = 'slash',
    )
    
    EXTENSION_LOADER.add_default_variables(Nitori=Nitori)
    
    EXTENSION_LOADER.load_extension('bots.koishi', locked=True)
    EXTENSION_LOADER.load_extension('bots.satori', locked=True)
    EXTENSION_LOADER.load_extension('bots.flan'  , locked=True)
    EXTENSION_LOADER.load_extension('bots.nitori', locked=True)

MODULE_NAMES = set()

path = None
for path in os.listdir(os.path.join(PATH__KOISHI, 'bots', 'modules')):
    full_path = os.path.join(PATH__KOISHI, 'bots', 'modules', path)
    if is_file(full_path):
        if not path.endswith('.py'):
            continue
        
        path = path[:-3]
    
    elif is_folder(full_path):
        if path.startswith('_'):
            continue
    else:
        continue
    
    MODULE_NAMES.add(path)

if MARISA_MODE:
    MARISA_ALLOWED_MODULES = set()
    
    if config.ALLOW_MARISA_SNEKBOX:
        MARISA_ALLOWED_MODULES.add('snekbox')
    
    MARISA_ALLOWED_MODULES.add('voice')
    MARISA_ALLOWED_MODULES.add('extensions')
    MARISA_ALLOWED_MODULES.add('google')
    
    for path in list(MODULE_NAMES):
        if path not in MARISA_ALLOWED_MODULES:
            MODULE_NAMES.remove(path)
    
else:
    if not config.ALLOW_KOISHI_SNEKBOX:
        MODULE_NAMES.discard('snekbox')
    
    MODULE_NAMES.discard('witch_craft')
    MODULE_NAMES.discard('google')

for path in MODULE_NAMES:
    EXTENSION_LOADER.add('bots.modules.'+path)

del path

EXTENSION_LOADER.load_all()
