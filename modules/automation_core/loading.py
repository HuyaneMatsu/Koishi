__all__ = ()

from scarletio import copy_docs

from bot_utils.models import DB_ENGINE, AUTOMATION_CONFIGURATION_TABLE

from .automation_configuration import AutomationConfiguration
from .presets import apply_presets


async def load():
    """
    Loads the entries from the database.
    
    This function is a coroutine.
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(AUTOMATION_CONFIGURATION_TABLE.select())
        for entry in (await response.fetchall()):
            AutomationConfiguration.from_entry(entry)


# Apply presets if we do not have DB
if DB_ENGINE is None:
    @copy_docs(load)
    async def load():
        apply_presets()


async def setup(module):
    """
    Called after the module is loaded. Pulls all entries from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    await load()
