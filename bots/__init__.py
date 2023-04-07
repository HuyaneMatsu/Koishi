from hata import Activity, ActivityType, Client, IntentFlag, Locale
from hata.ext.plugin_loader import add_default_plugin_variables, register_and_load_plugin, register_plugin

import config
from bot_utils.constants import DEFAULT_CATEGORY_NAME, PREFIX__FLAN, PREFIX__MARISA, PREFIX__SATORI
from bot_utils.utils import category_name_rule, random_error_message_getter


from bot_utils import async_engine # replace sync with async database engine.

MARISA_MODE = config.MARISA_MODE
add_default_plugin_variables(MARISA_MODE = MARISA_MODE)

if MARISA_MODE:
    Marisa = Client(
        config.MARISA_TOKEN,
        secret = config.MARISA_SECRET,
        client_id = config.MARISA_ID,
        # intents = IntentFlag() - IntentFlag(0).update_by_keys(message_content = True),
        http_debug_options = 'canary',
        extensions = (
            'command_utils',
            'slash',
            'commands_v2',
            # 'solarlink',
        ),
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
        shard_count = 2,
        intents = IntentFlag().update_by_keys(_17 = 1, _18 = 1, _19 = 1, _21 = 1),
        # assert_application_command_permission_missmatch_at = [GUILD__SUPPORT],
        # enforce_application_command_permissions = True,
    )
    
    add_default_plugin_variables(Marisa = Marisa, COMMAND_CLIENT = Marisa, SLASH_CLIENT = Marisa)
    
    
    register_and_load_plugin('bots.marisa', locked = True)
    
    register_plugin('bots.testers', MAIN_CLIENT = Marisa)
    register_plugin('bots.previews', MAIN_CLIENT = Marisa)

else:
    add_default_plugin_variables(SOLARLINK_VOICE = False)
    
    Koishi = Client(
        config.KOISHI_TOKEN,
        secret = config.KOISHI_SECRET,
        client_id = config.KOISHI_ID,
        activity = Activity('with Kokoro'),
        shard_count = 2,
        should_request_users = False,
        intents = IntentFlag().update_by_keys(
            guild_users = True, # We need this
            guild_presences = True, # Now this too, :KoishiFail:
            _17 = 1,
            _18 = 1,
            _19 = 1,
            _21 = 1, # Gonna catch them all
        ),
        application_id = config.KOISHI_ID,
        extensions = ('command_utils', 'slash', 'top_gg'),
        top_gg_token = config.KOISHI_TOP_GG_TOKEN,
    )
    
    add_default_plugin_variables(Koishi = Koishi, SLASH_CLIENT = Koishi)
    
    Satori = Client(
        config.SATORI_TOKEN,
        secret = config.SATORI_SECRET,
        client_id = config.SATORI_ID,
        activity = Activity('with Koishi'),
        status = 'dnd',
        application_id = config.SATORI_ID,
        extensions = ('command_utils', 'commands_v2', 'slash',),
        prefix = PREFIX__SATORI,
        category_name_rule = category_name_rule,
        default_category_name = DEFAULT_CATEGORY_NAME,
    )
    
    add_default_plugin_variables(Satori=Satori, COMMAND_CLIENT = Satori)
    
    Flan = Client(
        config.FLAN_TOKEN,
        client_id = config.FLAN_ID,
        activity = Activity('Chesuto development', activity_type = ActivityType.watching),
        status = 'idle',
        application_id = config.FLAN_ID,
        intents = IntentFlag() - IntentFlag(0).update_by_keys(message_content = True),
        extensions = ('command_utils', 'commands_v2',),
        default_category_name = 'GENERAL COMMANDS',
        category_name_rule = category_name_rule,
        prefix = PREFIX__FLAN,
    )
    
    add_default_plugin_variables(Flan=Flan)
    
    Nitori = Client(
        config.NITORI_TOKEN,
        client_id = config.NITORI_ID,
        application_id = config.NITORI_ID,
        intents = IntentFlag() - IntentFlag(0).update_by_keys(message_content = True),
        extensions = 'slash',
        random_error_message_getter = random_error_message_getter,
    )
    
    add_default_plugin_variables(Nitori = Nitori)
    
    
    Renes = Client(
        config.RENES_TOKEN,
        client_id = config.RENES_ID,
        application_id = config.RENES_ID,
        extensions = 'slash',
    )
    
    add_default_plugin_variables(Renes = Renes)
    
    
    register_and_load_plugin('bots.koishi', locked = True)
    register_and_load_plugin('bots.satori', locked = True)
    register_and_load_plugin('bots.flan'  , locked = True)
    register_and_load_plugin('bots.nitori', locked = True)
    register_and_load_plugin('bots.renes' , locked = True)



register_plugin('bots.system')
if MARISA_MODE:
    register_plugin('bots.previews')
    register_plugin('bots.testers')
else:
    register_plugin('bots.modules')
