# -*- coding: utf-8 -*-
import os, sys
os.environ['HATA_API_VERSION'] = '8'

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

del hata_path

import hata
# Import things depending on settings and which file is started up.
#
# As self host, turn `RUN_WEBAPP_AS_MAIN` on and run this file.
#
# If hosting, wsgi will import this file, so the bots will not start up. Those need to be started up separatedly by an
# always running task.

if __name__ == '__main__':
    import bots
    hata.start_clients()
    
    if config.RUN_WEBAPP_AS_MAIN:
        from web import WEBAPP
        WEBAPP.run()
else:
    hata.KOKORO.stop()
    from web import WEBAPP
