from hata import ACTIVITY_TYPES, ActivityRich, Client, IntentFlag, Locale
from hata.ext.extension_loader import EXTENSION_LOADER

import config
from bot_utils.constants import DEFAULT_CATEGORY_NAME, PREFIX__FLAN, PREFIX__MARISA, PREFIX__SATORI, GUILD__SUPPORT
from bot_utils.utils import category_name_rule, random_error_message_getter

from bot_utils import async_engine # replace sync with async database engine.

MARISA_MODE = config.MARISA_MODE
EXTENSION_LOADER.add_default_variables(MARISA_MODE=MARISA_MODE)

if MARISA_MODE:
    Marisa = Client(
        config.MARISA_TOKEN,
        secret = config.MARISA_SECRET,
        client_id = config.MARISA_ID,
        # intents = IntentFlag() - IntentFlag(0).update_by_keys(message_content=True),
        http_debug_options = 'canary',
        extensions = ('command_utils', 'slash', 'commands_v2', 'solarlink'),
        prefix = PREFIX__MARISA,
        default_category_name = DEFAULT_CATEGORY_NAME,
        category_name_rule = category_name_rule,
        translation_table = {
            Locale.english_us: {
                'cat-feeder': 'feed-ya-meow',
                'Feed the cat!': 'Owner hungry!'
            },
            Locale.english_gb: {
                'cat-feeder': 'feed-ya-meow',
                'Feed the cat!': 'Owner hungry!'
            },
        },
        assert_application_command_permission_missmatch_at = [GUILD__SUPPORT],
        enforce_application_command_permissions = True,
    )
    
    EXTENSION_LOADER.add_default_variables(Marisa=Marisa, COMMAND_CLIENT=Marisa, SLASH_CLIENT=Marisa)
    
    
    EXTENSION_LOADER.load_extension('bots.marisa', locked=True)
    
    EXTENSION_LOADER.add('bots.testers', MAIN_CLIENT=Marisa)
    EXTENSION_LOADER.add('bots.previews', MAIN_CLIENT=Marisa)

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


EXTENSION_LOADER.add('bots.system')
if MARISA_MODE:
    EXTENSION_LOADER.add('bots.previews')
    EXTENSION_LOADER.add('bots.testers')
else:
    EXTENSION_LOADER.add('bots.modules')
