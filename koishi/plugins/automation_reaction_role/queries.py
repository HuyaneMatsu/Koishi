__all__ = (
    'query_delete_automation_reaction_role_entry', 'query_delete_automation_reaction_role_entry_listing',
    'query_load_automation_reaction_role_entries', 'query_save_automation_reaction_role_entry',
    'query_update_automation_reaction_role_entry'
)

from itertools import count

from scarletio import copy_docs

from ...bot_utils.models import DB_ENGINE, AUTOMATION_REACTION_ROLE_TABLE, automation_reaction_role_model

from .automation_reaction_role_entry import AutomationReactionRoleEntry
from .constants import ENTRY_DATA_VERSION, AUTOMATION_REACTION_ROLE_BY_GUILD_ID, AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID
from .items import pack_items


COUNTER = iter(count(1))


async def query_save_automation_reaction_role_entry(automation_reaction_role_entry):
    """
    Saves the given auto react role entry into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The entry to save.
    """
    if automation_reaction_role_entry.entry_id:
        return
    
    entry_id = await _query_save_automation_reaction_role_entry_entry(automation_reaction_role_entry)
    automation_reaction_role_entry.entry_id = entry_id
    
    AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[automation_reaction_role_entry.message.id] = automation_reaction_role_entry
    
    try:
        automation_reaction_role_entries = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[
            automation_reaction_role_entry.message.guild_id
        ]
    except KeyError:
        automation_reaction_role_entries = []
        AUTOMATION_REACTION_ROLE_BY_GUILD_ID[automation_reaction_role_entry.message.guild_id] = (
            automation_reaction_role_entries
        )
    
    automation_reaction_role_entries.append(automation_reaction_role_entry)


async def _query_save_automation_reaction_role_entry_entry(automation_reaction_role_entry):
    """
    Executes a save query.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The entry to save.
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            AUTOMATION_REACTION_ROLE_TABLE.insert().values(
                message_id = automation_reaction_role_entry.message.id,
                channel_id = automation_reaction_role_entry.message.channel_id,
                guild_id = automation_reaction_role_entry.message.guild_id,
                
                flags = automation_reaction_role_entry.flags,
                data = pack_items(automation_reaction_role_entry.items, ENTRY_DATA_VERSION),
                data_version = ENTRY_DATA_VERSION,
            ).returning(
                automation_reaction_role_model.id
            )
        )
        
        result = await response.fetchone()
        return result[0]


if DB_ENGINE is None:
    @copy_docs(_query_save_automation_reaction_role_entry_entry)
    async def _query_save_automation_reaction_role_entry_entry(automation_reaction_role_entry):
        return next(COUNTER)


async def query_update_automation_reaction_role_entry(automation_reaction_role_entry):
    """
    Updates the given auto react role entry in the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The entry to update.
    """
    if not automation_reaction_role_entry.entry_id:
        return
    
    await _query_update_automation_reaction_role_entry(automation_reaction_role_entry)


async def _query_update_automation_reaction_role_entry(automation_reaction_role_entry):
    """
    Executes update query.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The entry to update.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            AUTOMATION_REACTION_ROLE_TABLE.update().values(
                flags = automation_reaction_role_entry.flags,
                data = pack_items(automation_reaction_role_entry.items, ENTRY_DATA_VERSION),
                data_version = ENTRY_DATA_VERSION,
            ).where(
                automation_reaction_role_model.id == automation_reaction_role_entry.entry_id,
            ),
        )


if DB_ENGINE is None:
    @copy_docs(_query_update_automation_reaction_role_entry)
    async def _query_update_automation_reaction_role_entry(automation_reaction_role_entry):
        pass


def _remove_automation_reaction_role_entry_from_cache(automation_reaction_role_entry):
    """
    Removes the given auto react role from cache.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The auto react role to remove.
    """
    try:
        del AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[automation_reaction_role_entry.message.id]
    except KeyError:
        pass
    
    try:
        automation_reaction_role_entries = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[
            automation_reaction_role_entry.message.guild_id
        ]
    except KeyError:
        pass
    else:
        try:
            automation_reaction_role_entries.remove(automation_reaction_role_entry)
        except KeyError:
            pass
        else:
            if not automation_reaction_role_entries:
                del AUTOMATION_REACTION_ROLE_BY_GUILD_ID[automation_reaction_role_entry.message.guild_id]


async def query_delete_automation_reaction_role_entry(automation_reaction_role_entry):
    """
    Deletes the given auto react role entry from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The entry to delete.
    """
    _remove_automation_reaction_role_entry_from_cache(automation_reaction_role_entry)
    await _query_delete_automation_reaction_role_entry(automation_reaction_role_entry)


async def _query_delete_automation_reaction_role_entry(automation_reaction_role_entry):
    """
    Executes delete query.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entry : ``AutomationReactionRoleEntry``
        The entry to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            AUTOMATION_REACTION_ROLE_TABLE.delete().where(
                automation_reaction_role_model.id == automation_reaction_role_entry.entry_id,
            ),
        )


if DB_ENGINE is None:
    @copy_docs(_query_delete_automation_reaction_role_entry)
    async def _query_delete_automation_reaction_role_entry(automation_reaction_role_entry):
        pass


async def query_delete_automation_reaction_role_entry_listing(automation_reaction_role_entries):
    """
    Deletes the given auto react role entries from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entries : ``list<AutomationReactionRoleEntry>``
        The entries to delete.
    """
    for automation_reaction_role_entry in automation_reaction_role_entries:
        _remove_automation_reaction_role_entry_from_cache(automation_reaction_role_entry)
    
    await _query_delete_automation_reaction_role_entry_listing(automation_reaction_role_entries)


async def _query_delete_automation_reaction_role_entry_listing(automation_reaction_role_entries):
    """
    Executes delete queries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    automation_reaction_role_entries : ``list<AutomationReactionRoleEntry>``
        The entries to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            AUTOMATION_REACTION_ROLE_TABLE.delete().where(
                automation_reaction_role_model.id.in_([
                    automation_reaction_role_entry.entry_id
                    for automation_reaction_role_entry in automation_reaction_role_entries
                ]),
            ),
        )


if DB_ENGINE is None:
    @copy_docs(_query_delete_automation_reaction_role_entry_listing)
    async def _query_delete_automation_reaction_role_entry_listing(automation_reaction_role_entries):
        pass


async def query_load_automation_reaction_role_entries():
    """
    Gets all the auto react role entries.
    Does not return them, just puts them in the cache.
    
    This function is a coroutine.
    """
    results = await _query_get_automation_reaction_role_entries()
    for result in results:
        automation_reaction_role_entry = AutomationReactionRoleEntry.from_entry(result)
        
        # Insert to cache
        AUTOMATION_REACTION_ROLE_BY_MESSAGE_ID[automation_reaction_role_entry.message.id] = (
            automation_reaction_role_entry
        )
        
        guild_id = automation_reaction_role_entry.message.guild_id
        try:
            automation_reaction_role_entry_listing = AUTOMATION_REACTION_ROLE_BY_GUILD_ID[guild_id]
        except KeyError:
            automation_reaction_role_entry_listing = []
            AUTOMATION_REACTION_ROLE_BY_GUILD_ID[guild_id] = automation_reaction_role_entry_listing
        
        automation_reaction_role_entry_listing.append(automation_reaction_role_entry)


async def _query_get_automation_reaction_role_entries():
    """
    Executes a get auto react role entries query.
    
    This function is a coroutine.
    
    Returns
    -------
    entries : `list<sqlalchemy.engine.result.RowProxy>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(AUTOMATION_REACTION_ROLE_TABLE.select())
        return (await response.fetchall())
    

if DB_ENGINE is None:
    @copy_docs(_query_get_automation_reaction_role_entries)
    async def _query_get_automation_reaction_role_entries():
        return []
