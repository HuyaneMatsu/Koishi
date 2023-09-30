__all__ = (
    'get_more_notification_settings', 'get_more_notification_settings_with_connector', 'get_one_notification_settings',
    'get_one_notification_settings_with_connector', 'save_one_notification_settings',
    'save_one_notification_settings_with_connector',
)

from scarletio import copy_docs

from ...bot_utils.models import NOTIFICATION_SETTINGS_TABLE, DB_ENGINE, notification_settings_model

from .cache import get_more_from_cache, get_one_from_cache, put_more_to_cache, put_none_to_cache, put_one_to_cache
from .helpers import merge_results
from .notification_settings import NotificationSettings


async def get_one_notification_settings(user_id):
    """
    Gets notification settings for the given user identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    
    Returns
    -------
    notification_settings : ``NotificationSettings``
    """
    notification_settings, miss = get_one_from_cache(user_id)
    if miss:
        notification_settings = await _query_one_notification_settings(user_id)
        if notification_settings is None:
            put_none_to_cache(user_id)
            notification_settings = NotificationSettings(user_id)
        else:
            put_one_to_cache(notification_settings)
    
    return notification_settings


async def get_one_notification_settings_with_connector(user_id, connector):
    """
    Gets notification settings with the given connector for the given user identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    notification_settings : ``NotificationSettings``
    """
    notification_settings, miss = get_one_from_cache(user_id)
    if miss:
        notification_settings = await _query_one_notification_settings_with_connector(user_id, connector)
        if notification_settings is None:
            put_none_to_cache(user_id)
            notification_settings = NotificationSettings(user_id)
        else:
            put_one_to_cache(notification_settings)
    
    return notification_settings


async def _query_one_notification_settings(user_id):
    """
    Queries notification settings for the given user identifier.
    used by ``get_one_notification_settings`` on cache miss.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    
    Returns
    -------
    notification_settings : `None | NotificationSettings`
    """
    async with DB_ENGINE.connect() as connector:
        return await _query_one_notification_settings_with_connector(user_id, connector)


if DB_ENGINE is None:
    @copy_docs(_query_one_notification_settings)
    async def _query_one_notification_settings(user_id):
        return None


async def _query_one_notification_settings_with_connector(user_id, connector):
    """
    Queries notification settings with the given connector for the given user identifier.
    used by ``get_one_notification_settings_with_connector`` on cache miss.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to request the settings for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    notification_settings : `None | list<NotificationSettings>`
    """
    response = await connector.execute(
        NOTIFICATION_SETTINGS_TABLE.select().where(
            notification_settings_model.user_id == user_id,
        )
    )
    
    entry = await response.fetchone()
    if entry is None:
        result = None
    else:
        result = NotificationSettings.from_entry(entry)
    
    return result


if DB_ENGINE is None:
    @copy_docs(_query_one_notification_settings_with_connector)
    async def _query_one_notification_settings_with_connector(user_id, connector):
        return None


async def get_more_notification_settings(user_ids):
    """
    Gets notification settings for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    
    Returns
    -------
    notification_settings : `None | list<NotificationSettings>`
    """
    notification_settings, misses = get_more_from_cache(user_ids)
    if misses is not None:
        to_merge, misses = await _query_more_notification_settings(misses)
        put_more_to_cache(to_merge)
        notification_settings = merge_results(notification_settings, to_merge)
        
        if misses is not None:
            to_merge = []
            for user_id in misses:
                put_none_to_cache(user_id)
                to_merge.append(NotificationSettings(user_id))
            
            notification_settings = merge_results(notification_settings, to_merge)
    
    return notification_settings 


async def get_more_notification_settings_with_connector(user_ids, connector):
    """
    Gets notification settings with the given connector for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    notification_settings : `None`, `list<NotificationSettings>`
    """
    notification_settings, misses = get_more_from_cache(user_ids)
    if misses is not None:
        to_merge, misses = await _query_more_notification_settings_with_connector(misses, connector)
        put_more_to_cache(to_merge)
        notification_settings = merge_results(notification_settings, to_merge)
        
        if misses is not None:
            to_merge = []
            for user_id in misses:
                put_none_to_cache(user_id)
                to_merge.append(NotificationSettings(user_id))
            
            notification_settings = merge_results(notification_settings, to_merge)
    
    return notification_settings 


async def _query_more_notification_settings(user_ids):
    """
    gets notification settings for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    
    Returns
    -------
    notification_settings : `None | list<NotificationSettings>`
    misses : `None | list<int>`
    """
    async with DB_ENGINE.connect() as connector:
        return await _query_more_notification_settings_with_connector(user_ids, connector)


if DB_ENGINE is None:
    @copy_docs(_query_more_notification_settings)
    async def _query_more_notification_settings(user_ids):
        return None, user_ids


async def _query_more_notification_settings_with_connector(user_ids, connector):
    """
    Queries notification settings with the given connector for the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `list<int>`
        The user identifiers to request the settings for.
    connector : ``AsyncConnection``
        Data base connector.
    
    Returns
    -------
    notification_settings : `None | list<NotificationSettings>`
    misses : `None | list<int>`
    """
    response = await connector.execute(
        NOTIFICATION_SETTINGS_TABLE.select().where(
            notification_settings_model.user_id.in_(
                user_ids,
            ),
        )
    )
    
    if response.rowcount:
        entries = await response.fetchall()
        results = [NotificationSettings.from_entry(entry) for entry in entries]
        
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
    @copy_docs(_query_more_notification_settings_with_connector)
    async def _query_more_notification_settings_with_connector(user_ids, connector):
        return None, user_ids


async def save_one_notification_settings(notification_settings):
    """
    Saves one notification settings.
    
    This function is a coroutine.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to save.
    """
    if notification_settings:
        await _save_notification_settings(notification_settings)
        put_one_to_cache(notification_settings)
    else:
        await _remove_notification_settings(notification_settings)
        put_none_to_cache(notification_settings.user_id)


async def save_one_notification_settings_with_connector(notification_settings, connector):
    """
    Saves one notification settings.
    
    This function is a coroutine.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to save.
    connector : ``AsyncConnection``
        Data base connector.
    """
    if notification_settings:
        await _save_notification_settings_with_connector(notification_settings, connector)
        put_one_to_cache(notification_settings)
    else:
        await _remove_notification_settings_with_connector(notification_settings, connector)
        put_none_to_cache(notification_settings.user_id)


async def _save_notification_settings(notification_settings):
    """
    Saves a notification settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to add.
    """
    async with DB_ENGINE.connect() as connector:
        await _save_notification_settings_with_connector(notification_settings, connector)


if DB_ENGINE is None:
    @copy_docs(_save_notification_settings)
    async def _save_notification_settings(notification_settings):
        return None


async def _save_notification_settings_with_connector(notification_settings, connector):
    """
    Saves a notification settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to add.
    connector : ``AsyncConnection``
        Data base connector.
    """
    entry_id = notification_settings.entry_id
    if entry_id == -1:
        # Add if new.
        response = await connector.execute(
            NOTIFICATION_SETTINGS_TABLE.insert().values(
                user_id = notification_settings.user_id,
                daily = notification_settings.daily,
                proposal = notification_settings.proposal,
            ).returning(    
                notification_settings_model.id,
            )
        )
        
        # Update `.entry_id`
        entry = await response.fetchone()
        notification_settings.entry_id = entry[0]
    
    else:
        # Update if exists. This branch should not happen.
        await connector.execute(
            NOTIFICATION_SETTINGS_TABLE.update(
                notification_settings_model.id == entry_id,
            ).values(
                user_id = notification_settings.user_id,
                daily = notification_settings.daily,
                proposal = notification_settings.proposal,
            )
        )


if DB_ENGINE is None:
    @copy_docs(_save_notification_settings_with_connector)
    async def _save_notification_settings_with_connector(notification_settings, connector):
        return None


async def _remove_notification_settings(notification_settings):
    """
    Adds a notification settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to add.
    """
    async with DB_ENGINE.connect() as connector:
        await _remove_notification_settings_with_connector(notification_settings, connector)


if DB_ENGINE is None:
    @copy_docs(_remove_notification_settings)
    async def _remove_notification_settings(notification_settings):
        return None


async def _remove_notification_settings_with_connector(notification_settings, connector):
    """
    Adds a notification settings to the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to add.
    connector : ``AsyncConnection``
        Data base connector.
    """
    entry_id = notification_settings.entry_id
    # Do nothing if the entry doesnt exists.
    if entry_id == -1:
        return
    
    await connector.execute(
        NOTIFICATION_SETTINGS_TABLE.delete().where(
            notification_settings_model.id == entry_id,
        )
    )


if DB_ENGINE is None:
    @copy_docs(_remove_notification_settings_with_connector)
    async def _remove_notification_settings_with_connector(notification_settings, connector):
        return None
