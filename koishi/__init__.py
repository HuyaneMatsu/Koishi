__all__ = ()

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

config_path = os.path.dirname(config_path)

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


if 'vampytest' in sys.modules:
    from .cli import load_plugins
    load_plugins()
