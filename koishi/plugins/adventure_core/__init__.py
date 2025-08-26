from .action import *
from .adventure import *
from .auto_cancellation import *
from .duration_suggestion_set import *
from .location import *
from .logic import *
from .options import *
from .return_ import *
from .target import *

from .constants import *
from .queries import *


__all__ = (
    *action.__all__,
    *adventure.__all__,
    *auto_cancellation.__all__,
    *duration_suggestion_set.__all__,
    *location.__all__,
    *logic.__all__,
    *options.__all__,
    *return_.__all__,
    *target.__all__,
    
    *constants.__all__,
    *queries.__all__,
)


# ---- add setup code ---

from ...bots import MAIN_CLIENT


async def setup(module):
    """
    Called when the plugin is loaded. If the client is already running, resumes the active adventures.
    """
    if MAIN_CLIENT.running:
        await resume_active_adventures()


# Do not add ready event handler if we are already running.
if not MAIN_CLIENT.running:
    @MAIN_CLIENT.events
    async def ready(client):
        """
        Called when the client is ready. Removes itself of the client and resumes active adventures.
        """
        client.events.remove(ready)
        
        await resume_active_adventures()


def teardown(module):
    """
    Called when the plugin is unloaded. Aborts all active adventures.
    """
    abort_active_adventures()
