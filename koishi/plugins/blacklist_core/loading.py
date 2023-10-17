__all__ = ()

from scarletio import copy_docs

from ...bot_utils.models import DB_ENGINE, BLACKLIST_TABLE

from .constants import BLACKLIST


async def load():
    """
    Loads the entries from the database.
    
    This function is a coroutine.
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(BLACKLIST_TABLE.select())
        for entry in (await response.fetchall()):
            BLACKLIST[entry['user_id']] = entry['id']


# Do nothing if no DB
if DB_ENGINE is None:
    @copy_docs(load)
    async def load():
        pass


async def setup(module):
    """
    Called after the plugin is loaded. Pulls all entries from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    module : ``ModuleType``
        This module.
    """
    await load()
