__all__ = (
    'add_user_id_to_blacklist', 'add_user_id_to_blacklist_with_connector', 'is_user_id_in_blacklist',
    'remove_user_id_from_blacklist', 'remove_user_id_from_blacklist_with_connector'
)

from scarletio import copy_docs

from ...bot_utils.models import BLACKLIST_TABLE, DB_ENGINE, blacklist_model

from .constants import BLACKLIST


def is_user_id_in_blacklist(user_id):
    """
    Returns whether the given user identifier is blacklisted.
    
    Parameters
    ----------
    user_id : `int`
        user identifier to check for.
    
    Returns
    -------
    is_blacklisted : `bool`
    """
    return user_id in BLACKLIST.keys()


async def add_user_id_to_blacklist(user_id):
    """
    Adds the user's identifier to the blacklist.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to add.
    
    Returns
    -------
    added : `bool`
    """
    if BLACKLIST.get(user_id, 0) != 0:
        return False
    
    entry_id = await _add_user_id_to_blacklist(user_id)
    BLACKLIST[user_id] = entry_id
    return True


async def add_user_id_to_blacklist_with_connector(user_id, connector):
    """
    Adds the user's identifier to the blacklist with the given connector.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to add.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    added : `bool`
    """
    if BLACKLIST.get(user_id, 0) != 0:
        return False
    
    entry_id = await _add_user_id_to_blacklist_with_connector(user_id, connector)
    BLACKLIST[user_id] = entry_id
    return True


async def _add_user_id_to_blacklist(user_id):
    """
    Adds an entry to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to add.
    
    Returns
    -------
    entry_id : `int`
    """
    async with DB_ENGINE.connect() as connector:
        await _add_user_id_to_blacklist_with_connector(user_id, connector)


async def _add_user_id_to_blacklist_with_connector(user_id, connector):
    """
    Adds an entry to the database with the given connector.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to add.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    entry_id : `int`
    """
    response = await connector.execute(
        BLACKLIST_TABLE.insert().values(
            user_id = user_id,
        ).returning(    
            blacklist_model.id,
        )
    )
    
    # Return `.entry_id`
    entry = await response.fetchone()
    return entry[0]


if DB_ENGINE is None:
    @copy_docs(_add_user_id_to_blacklist)
    async def _add_user_id_to_blacklist(user_id):
        return -1


if DB_ENGINE is None:
    @copy_docs(_add_user_id_to_blacklist_with_connector)
    async def _add_user_id_to_blacklist_with_connector(user_id, connector):
        return -1


async def remove_user_id_from_blacklist(user_id):
    """
    Removes a user by its identifier from the blacklist.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to remove.
    
    Returns
    -------
    removed : `bool`
    """
    entry_id = BLACKLIST.get(user_id, 0)
    if entry_id == 0:
        return False
    
    await _remove_entry_id_from_blacklist(entry_id)
    
    try:
        del BLACKLIST[user_id]
    except KeyError:
        pass
    
    return True


async def remove_user_id_from_blacklist_with_connector(user_id, connector):
    """
    Removes a user by its identifier from the blacklist with the given connector.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to remove.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    removed : `bool`
    """
    entry_id = BLACKLIST.get(user_id, 0)
    if entry_id == 0:
        return False
    
    await _remove_entry_id_from_blacklist_with_connector(entry_id, connector)
    
    try:
        del BLACKLIST[user_id]
    except KeyError:
        pass
    
    return True


async def _remove_entry_id_from_blacklist(entry_id):
    """
    Removes an entry from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        The entry's identifier to remove.
    """
    async with DB_ENGINE.connect() as connector:
        await _remove_entry_id_from_blacklist_with_connector(entry_id, connector)


async def _remove_entry_id_from_blacklist_with_connector(entry_id, connector):
    """
    Removes an entry from the database with the given connector.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        The entry's identifier to remove.
    connector : ``AsyncConnection``
        Database connector.
    """
    await connector.execute(
        BLACKLIST_TABLE.delete().where(
            blacklist_model.id == entry_id,
        )
    )


if DB_ENGINE is None:
    @copy_docs(_remove_entry_id_from_blacklist)
    async def _remove_entry_id_from_blacklist(entry_id):
        return None


if DB_ENGINE is None:
    @copy_docs(_remove_entry_id_from_blacklist_with_connector)
    async def _remove_entry_id_from_blacklist_with_connector(entry_id, connector):
        return None
