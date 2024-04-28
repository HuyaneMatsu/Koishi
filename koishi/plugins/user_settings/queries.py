__all__ = (
    'get_more_user_settings', 'get_more_user_settings_with_connector', 'get_one_user_settings',
    'get_one_user_settings_with_connector', 'save_one_user_settings',
    'save_one_user_settings_with_connector',
)

from scarletio import copy_docs

from ...bot_utils.models import DB_ENGINE, USER_SETTINGS_TABLE, user_settings_model

from .cache import get_more_from_cache, get_one_from_cache, put_more_to_cache, put_none_to_cache, put_one_to_cache
from .helpers import merge_results
from .user_settings import UserSettings


async def get_one_user_settings(user_id):
    """
    Gets user settings for the given user identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    
    Returns
    -------
    user_settings : ``UserSettings``
    """
    user_settings, miss = get_one_from_cache(user_id)
    if miss:
        user_settings = await _query_one_user_settings(user_id)
        if user_settings is None:
            put_none_to_cache(user_id)
            user_settings = UserSettings(user_id)
        else:
            put_one_to_cache(user_settings)
    
    return user_settings


async def get_one_user_settings_with_connector(user_id, connector):
    """
    Gets user settings with the given connector for the given user identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    user_settings : ``UserSettings``
    """
    user_settings, miss = get_one_from_cache(user_id)
    if miss:
        user_settings = await _query_one_user_settings_with_connector(user_id, connector)
        if user_settings is None:
            put_none_to_cache(user_id)
            user_settings = UserSettings(user_id)
        else:
            put_one_to_cache(user_settings)
    
    return user_settings


async def _query_one_user_settings(user_id):
    """
    Queries user settings for the given user identifier.
    used by ``get_one_user_settings`` on cache miss.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    
    Returns
    -------
    user_settings : `None | UserSettings`
    """
    async with DB_ENGINE.connect() as connector:
        return await _query_one_user_settings_with_connector(user_id, connector)


if DB_ENGINE is None:
    @copy_docs(_query_one_user_settings)
    async def _query_one_user_settings(user_id):
        return None


async def _query_one_user_settings_with_connector(user_id, connector):
    """
    Queries user settings with the given connector for the given user identifier.
    used by ``get_one_user_settings_with_connector`` on cache miss.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    user_settings : `None | list<UserSettings>`
    """
    response = await connector.execute(
        USER_SETTINGS_TABLE.select().where(
            user_settings_model.user_id == user_id,
        )
    )
    
    entry = await response.fetchone()
    if entry is None:
        result = None
    else:
        result = UserSettings.from_entry(entry)
    
    return result


if DB_ENGINE is None:
    @copy_docs(_query_one_user_settings_with_connector)
    async def _query_one_user_settings_with_connector(user_id, connector):
        return None


async def get_more_user_settings(user_ids):
    """
    Gets user settings for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    
    Returns
    -------
    user_settings : `None | list<UserSettings>`
    """
    user_settings, misses = get_more_from_cache(user_ids)
    if misses is not None:
        to_merge, misses = await _query_more_user_settings(misses)
        put_more_to_cache(to_merge)
        user_settings = merge_results(user_settings, to_merge)
        
        if misses is not None:
            to_merge = []
            for user_id in misses:
                put_none_to_cache(user_id)
                to_merge.append(UserSettings(user_id))
            
            user_settings = merge_results(user_settings, to_merge)
    
    return user_settings 


async def get_more_user_settings_with_connector(user_ids, connector):
    """
    Gets user settings with the given connector for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    user_settings : `None`, `list<UserSettings>`
    """
    user_settings, misses = get_more_from_cache(user_ids)
    if misses is not None:
        to_merge, misses = await _query_more_user_settings_with_connector(misses, connector)
        put_more_to_cache(to_merge)
        user_settings = merge_results(user_settings, to_merge)
        
        if misses is not None:
            to_merge = []
            for user_id in misses:
                put_none_to_cache(user_id)
                to_merge.append(UserSettings(user_id))
            
            user_settings = merge_results(user_settings, to_merge)
    
    return user_settings 


async def _query_more_user_settings(user_ids):
    """
    gets user settings for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    
    Returns
    -------
    user_settings : `None | list<UserSettings>`
    misses : `None | list<int>`
    """
    async with DB_ENGINE.connect() as connector:
        return await _query_more_user_settings_with_connector(user_ids, connector)


if DB_ENGINE is None:
    @copy_docs(_query_more_user_settings)
    async def _query_more_user_settings(user_ids):
        return None, user_ids


async def _query_more_user_settings_with_connector(user_ids, connector):
    """
    Queries user settings with the given connector for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    user_settings : `None | list<UserSettings>`
    misses : `None | list<int>`
    """
    response = await connector.execute(
        USER_SETTINGS_TABLE.select().where(
            user_settings_model.user_id.in_(
                user_ids,
            ),
        )
    )
    
    if response.rowcount:
        entries = await response.fetchall()
        results = [UserSettings.from_entry(entry) for entry in entries]
        
        for result in results:
            try:
                user_ids.remove(result.user_id)
            except ValueError:
                pass
        
        if not user_ids:
            user_ids = None
    
    else:
        results = None
    
    return results, user_ids


if DB_ENGINE is None:
    @copy_docs(_query_more_user_settings_with_connector)
    async def _query_more_user_settings_with_connector(user_ids, connector):
        return None, user_ids


async def save_one_user_settings(user_settings):
    """
    Saves one user settings.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user settings to save.
    """
    if user_settings:
        await _save_user_settings(user_settings)
        put_one_to_cache(user_settings)
    else:
        await _remove_user_settings(user_settings)
        put_none_to_cache(user_settings.user_id)


async def save_one_user_settings_with_connector(user_settings, connector):
    """
    Saves one user settings.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user settings to save.
    connector : ``AsyncConnection``
        Database connector.
    """
    if user_settings:
        await _save_user_settings_with_connector(user_settings, connector)
        put_one_to_cache(user_settings)
    else:
        await _remove_user_settings_with_connector(user_settings, connector)
        put_none_to_cache(user_settings.user_id)


async def _save_user_settings(user_settings):
    """
    Saves a user settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user settings to add.
    """
    async with DB_ENGINE.connect() as connector:
        await _save_user_settings_with_connector(user_settings, connector)


if DB_ENGINE is None:
    @copy_docs(_save_user_settings)
    async def _save_user_settings(user_settings):
        return None


async def _save_user_settings_with_connector(user_settings, connector):
    """
    Saves a user settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user settings to add.
    connector : ``AsyncConnection``
        Database connector.
    """
    entry_id = user_settings.entry_id
    if entry_id == -1:
        # Add if new.
        response = await connector.execute(
            USER_SETTINGS_TABLE.insert().values(
                user_id = user_settings.user_id,
                user_daily_by_waifu = user_settings.user_daily_by_waifu,
                user_proposal = user_settings.user_proposal,
                user_daily_reminder = user_settings.user_daily_reminder,
                preferred_client_id = user_settings.preferred_client_id,
                preferred_image_source = user_settings.preferred_image_source,
            ).returning(    
                user_settings_model.id,
            )
        )
        
        # Update `.entry_id`
        entry = await response.fetchone()
        user_settings.entry_id = entry[0]
    
    else:
        # Update if exists. This branch should not happen.
        await connector.execute(
            USER_SETTINGS_TABLE.update(
                user_settings_model.id == entry_id,
            ).values(
                user_id = user_settings.user_id,
                user_daily_by_waifu = user_settings.user_daily_by_waifu,
                user_proposal = user_settings.user_proposal,
                user_daily_reminder = user_settings.user_daily_reminder,
                preferred_client_id = user_settings.preferred_client_id,
                preferred_image_source = user_settings.preferred_image_source,
            )
        )


if DB_ENGINE is None:
    @copy_docs(_save_user_settings_with_connector)
    async def _save_user_settings_with_connector(user_settings, connector):
        return None


async def _remove_user_settings(user_settings):
    """
    Adds a user settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user settings to add.
    """
    async with DB_ENGINE.connect() as connector:
        await _remove_user_settings_with_connector(user_settings, connector)


if DB_ENGINE is None:
    @copy_docs(_remove_user_settings)
    async def _remove_user_settings(user_settings):
        return None


async def _remove_user_settings_with_connector(user_settings, connector):
    """
    Adds a user settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user settings to add.
    connector : ``AsyncConnection``
        Database connector.
    """
    entry_id = user_settings.entry_id
    # Do nothing if the entry doesnt exists.
    if entry_id == -1:
        return
    
    await connector.execute(
        USER_SETTINGS_TABLE.delete().where(
            user_settings_model.id == entry_id,
        )
    )


if DB_ENGINE is None:
    @copy_docs(_remove_user_settings_with_connector)
    async def _remove_user_settings_with_connector(user_settings, connector):
        return None
