from os.path import join as join_paths, isdir as is_folder, isfile as is_file
from os import listdir as list_directory

import config

from hata import Client, ActivityRich, ACTIVITY_TYPES, IntentFlag
from hata.ext.extension_loader import EXTENSION_LOADER
from bot_utils.constants import PATH__KOISHI, DEFAULT_CATEGORY_NAME, PREFIX__MARISA, PREFIX__FLAN, PREFIX__SATORI
from bot_utils.utils import random_error_message_getter, category_name_rule
from bot_utils import async_engine # replace sync with async database engine.

MARISA_MODE = config.MARISA_MODE
EXTENSION_LOADER.add_default_variables(MARISA_MODE=MARISA_MODE)

if MARISA_MODE:
    Marisa = Client(
        config.MARISA_TOKEN,
        client_id = config.MARISA_ID,
        # intents = IntentFlag() - IntentFlag(0).update_by_keys(message_content=True),
        http_debug_options = 'canary',
        extensions = ('command_utils', 'slash', 'commands_v2', 'solarlink'),
        prefix = PREFIX__MARISA,
        default_category_name = DEFAULT_CATEGORY_NAME,
        category_name_rule = category_name_rule,
    )
    
    EXTENSION_LOADER.add_default_variables(Marisa=Marisa, COMMAND_CLIENT=Marisa, SLASH_CLIENT=Marisa)
    
    EXTENSION_LOADER.load_extension('bots.marisa', locked=True)
    
    EXTENSION_LOADER.add('bots.testers', MAIN_CLIENT=Marisa)

else:
    EXTENSION_LOADER.add_default_variables(SOLARLINK_VOICE=False)
    
    Koishi = Client(
        config.KOISHI_TOKEN,
        secret = config.KOISHI_SECRET,
        client_id = config.KOISHI_ID,
        activity = ActivityRich('with Satori'),
        shard_count = 2,
        intents = IntentFlag().update_by_keys(
            guild_users = False,
            guild_presences = False,
        ),
        application_id = config.KOISHI_ID,
        extensions = ('command_utils', 'slash', 'top_gg'),
        top_gg_token = config.KOISHI_TOP_GG_TOKEN,
    )
    
    EXTENSION_LOADER.add_default_variables(Koishi=Koishi, SLASH_CLIENT=Koishi)
    
    Satori = Client(
        config.SATORI_TOKEN,
        secret = config.SATORI_SECRET,
        client_id = config.SATORI_ID,
        activity = ActivityRich('with Koishi'),
        status = 'dnd',
        application_id = config.SATORI_ID,
        extensions = ('command_utils', 'commands_v2', 'slash',),
        prefix = PREFIX__SATORI,
        category_name_rule = category_name_rule,
        default_category_name = DEFAULT_CATEGORY_NAME,
    )
    
    EXTENSION_LOADER.add_default_variables(Satori=Satori, COMMAND_CLIENT=Satori)
    
    Flan = Client(
        config.FLAN_TOKEN,
        client_id = config.FLAN_ID,
        activity = ActivityRich('Chesuto development', type_=ACTIVITY_TYPES.watching),
        status = 'idle',
        application_id = config.FLAN_ID,
        intents = IntentFlag() - IntentFlag(0).update_by_keys(message_content=True),
        extensions = ('command_utils', 'commands_v2',),
        default_category_name = 'GENERAL COMMANDS',
        category_name_rule = category_name_rule,
        prefix = PREFIX__FLAN,
    )
    
    EXTENSION_LOADER.add_default_variables(Flan=Flan)
    
    Nitori = Client(
        config.NITORI_TOKEN,
        client_id = config.NITORI_ID,
        application_id = config.NITORI_ID,
        intents = IntentFlag() - IntentFlag(0).update_by_keys(message_content=True),
        extensions = 'slash',
        random_error_message_getter = random_error_message_getter,
    )
    
    EXTENSION_LOADER.add_default_variables(Nitori=Nitori)
    
    EXTENSION_LOADER.load_extension('bots.koishi', locked=True)
    EXTENSION_LOADER.load_extension('bots.satori', locked=True)
    EXTENSION_LOADER.load_extension('bots.flan'  , locked=True)
    EXTENSION_LOADER.load_extension('bots.nitori', locked=True)

MODULE_NAMES = set()

path = None
for path in list_directory(join_paths(PATH__KOISHI, 'bots', 'modules')):
    full_path = join_paths(PATH__KOISHI, 'bots', 'modules', path)
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
    
    MARISA_ALLOWED_MODULES.add('extensions')
    MARISA_ALLOWED_MODULES.add('google')
    MARISA_ALLOWED_MODULES.add('log')
    
    for path in list(MODULE_NAMES):
        if path not in MARISA_ALLOWED_MODULES:
            MODULE_NAMES.remove(path)
    
else:
    if not config.ALLOW_KOISHI_SNEKBOX:
        MODULE_NAMES.discard('snekbox')
    
    MODULE_NAMES.discard('witch_craft')
    MODULE_NAMES.discard('google')

for path in MODULE_NAMES:
    EXTENSION_LOADER.add('bots.modules.' + path)

del path

EXTENSION_LOADER.load_all()
