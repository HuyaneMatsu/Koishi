from hata import Client
from hata.ext.extension_loader import import_extension
from bot_utils.constants import GUILD__SUPPORT

SLASH_CLIENT: Client

COMMAND = SLASH_CLIENT.interactions(
    None,
    name = 'voice',
    description = 'Voice commands',
    guild = GUILD__SUPPORT,
)

import_extension('.behavior', COMMAND=COMMAND)
import_extension('.filter_add', COMMAND=COMMAND)
import_extension('.filter_list', COMMAND=COMMAND)
import_extension('.filter_remove', COMMAND=COMMAND)
import_extension('.leave', COMMAND=COMMAND)
import_extension('.move', COMMAND=COMMAND)
import_extension('.pause', COMMAND=COMMAND)
import_extension('.play', COMMAND=COMMAND)
import_extension('.queue', COMMAND=COMMAND)
import_extension('.remove', COMMAND=COMMAND)
import_extension('.restart', COMMAND=COMMAND)
import_extension('.resume', COMMAND=COMMAND)
import_extension('.seek', COMMAND=COMMAND)
import_extension('.skip', COMMAND=COMMAND)
import_extension('.stop', COMMAND=COMMAND)
import_extension('.volume', COMMAND=COMMAND)
