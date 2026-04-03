__all__ = ('main',)

import sys

from hata.main import execute_command_from_system_parameters

import config

from .commands import *


def load_plugins():
    from hata import KOKORO
    from hata.ext.plugin_loader import add_default_plugin_variables, load_all_plugin, frame_filter, register_plugin
    from scarletio import write_exception_sync
    
    from .bots import COMMAND_CLIENT, FEATURE_CLIENTS, MAIN_CLIENT
    
    MARISA_MODE = config.MARISA_MODE
    
    add_default_plugin_variables(
        MARISA_MODE = MARISA_MODE,
        SOLARLINK_VOICE = MARISA_MODE,
        SOLARLINK_VOICE_ENABLED = False,
        FEATURE_CLIENTS = FEATURE_CLIENTS,
        COMMAND_CLIENT = COMMAND_CLIENT,
        MAIN_CLIENT = MAIN_CLIENT,
    )
    
    register_plugin(f'{__spec__.parent}.plugins_system')
    
    if 'vampytest' in sys.modules:
        LOAD_PREVIEWS = True
        LOAD_PLUGINS = True
    else:
        LOAD_PREVIEWS = MARISA_MODE
        LOAD_PLUGINS = not MARISA_MODE
    
    if LOAD_PREVIEWS:
        register_plugin(f'{__spec__.parent}.plugins_previews')
        register_plugin(f'{__spec__.parent}.plugins_testers')
    
    if LOAD_PLUGINS:
        register_plugin(f'{__spec__.parent}.plugins')
    
    try:
        load_all_plugin()
    except BaseException as err:
        write_exception_sync(err, filter = frame_filter)
        
        KOKORO.stop()
        raise SystemExit(1) from None


def main():
    from scarletio import write_exception_sync
    
    try:
        from .bot_utils import async_engine
    except ImportError as exception:
        if not config.MARISA_MODE:
            raise
        
        write_exception_sync(exception)
    
    
    load_plugins()
    if config.MARISA_MODE:
        from hata.ext.plugin_auto_reloader import start_auto_reloader, warn_auto_reloader_availability
        warn_auto_reloader_availability()
        start_auto_reloader()
    
    execute_command_from_system_parameters()
