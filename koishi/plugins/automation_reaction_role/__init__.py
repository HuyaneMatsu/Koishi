from .automation_reaction_role_entry import *
from .automation_reaction_role_item import *
from .commands import *
from .component_builders import *
from .constants import *
from .content_builders import *
from .custom_ids import *
from .events import *
from .helpers import *
from .interactions import *
from .items import *
from .queries import *


__all__ = ()


async def setup(module):
    """
    Called when the plugin is being loaded.
    Loads the auto react roles from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    module : `ModuleType`
        This module.
    """
    await query_load_automation_reaction_role_entries()
