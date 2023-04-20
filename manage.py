import os, sys
os.environ['HATA_DOCS_ENABLED'] = 'True'
os.environ['HATA_API_VERSION'] = '10'
os.environ['HATA_RICH_DISCORD_EXCEPTION'] = 'True'
os.environ['HATA_ALLOW_DEBUG_MESSAGES'] = 'True'
os.environ['HATA_LIBRARY_AGENT_APPENDIX'] = 'KoiBot'
os.environ['HATA_LIBRARY_NAME'] = 'discord.js'
os.environ['HATA_LIBRARY_URL'] = 'https://discord.js.org'
os.environ['HATA_LIBRARY_VERSION'] = '14.6.0'


# Load config
config_path = os.path.split(__file__)[0]
if config_path:
    config_path = os.path.split(config_path)[0]
else:
    # second try.
    config_path = os.path.abspath('..')

if config_path not in sys.path:
    sys.path.append(config_path)

del config_path

import config

# Load hata lib

hata_path = config.HATA_PATH
if (hata_path is not None) and (hata_path not in sys.path):
    sys.path.append(hata_path)

scarletio_path = config.SCARLETIO_PATH
if (scarletio_path is not None) and (scarletio_path not in sys.path):
    sys.path.append(scarletio_path)

del hata_path

import hata.main

# Import things depending on settings and which file is started up.
#
# As self host, turn `RUN_WEBAPP_AS_MAIN` on and run this file.
#
# If hosting, wsgi will import this file, so the bots will not start up. Those need to be started up separately by an
# always running task.

@hata.main.register
def run_webapp():
    """
    Runs the webapp of Koishi.
    """
    from web import WEBAPP
    WEBAPP.run()
    

if __name__ == '__main__':
    from hata import KOKORO
    from hata.ext.plugin_loader import add_default_plugin_variables, load_all_plugin, frame_filter, register_plugin
    from scarletio import write_exception_sync
    
    from bot_utils import async_engine
    from bots import *
    
    MARISA_MODE = config.MARISA_MODE
    
    add_default_plugin_variables(
        MARISA_MODE = MARISA_MODE,
        SOLARLINK_VOICE = MARISA_MODE,
        SOLARLINK_VOICE_ENABLED = False,
        SLASH_CLIENT = SLASH_CLIENT,
        COMMAND_CLIENT = COMMAND_CLIENT,
        MAIN_CLIENT = MAIN_CLIENT,
    )
    
    register_plugin('modules_system')
    if MARISA_MODE:
        register_plugin('modules_previews')
        register_plugin('modules_testers')
    else:
        register_plugin('modules')
    
    try:
        load_all_plugin()
    except BaseException as err:
        write_exception_sync(err, filter = frame_filter)
        
        KOKORO.stop()
        raise SystemExit
    
    if MARISA_MODE:
        from hata.ext.plugin_auto_reloader import start_auto_reloader, warn_auto_reloader_availability
        warn_auto_reloader_availability()
        start_auto_reloader()
    
    hata.main.execute_command_from_system_parameters()


else:
    hata.KOKORO.stop()
    from web import WEBAPP
