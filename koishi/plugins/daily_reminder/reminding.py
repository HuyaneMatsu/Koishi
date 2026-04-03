__all__ = ()

from itertools import islice

from hata import DiscordException
from scarletio import CauseGroup, copy_docs

from ...bot_utils.models import DB_ENGINE
from ...bots import MAIN_CLIENT

from ..user_settings import get_preferred_client_for_user

from .builders import build_notification_daily_reminder
from .queries import get_entries_to_notify_with_connector, set_entry_as_notified_with_connector
from .requests import try_channel_create, try_message_create, try_user_get


async def notify_user(entry, connector):
    """
    Notifies the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry : `sqlalchemy.engine.result.RowProxy<id: int, user_id: int, preferred_client_id: int>`
        The entry representing a user and its configuration to notify.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    success : `bool`
    """
    entry_id, user_id, preferred_client_id = entry
    user = await try_user_get(user_id, entry_id, connector)
    if user is None:
        return False
    
    client = get_preferred_client_for_user(user, preferred_client_id, None)
    channel = await try_channel_create(client, user_id, entry_id, connector)
    if channel is None:
        return False
    
    embed, components = build_notification_daily_reminder(preferred_client_id)
    message = await try_message_create(client, channel, embed, components, entry_id, connector)
    if message is None:
        return False
    
    await set_entry_as_notified_with_connector(connector, entry_id)
    return True


async def remind_forgot_daily():
    """
    Reminds the users who forgot to claim their daily.
    
    This function is a coroutine.
    """
    async with DB_ENGINE.connect() as connector:
        await remind_forgot_daily_with_connector(connector)


if DB_ENGINE is None:
    @copy_docs(remind_forgot_daily)
    async def remind_forgot_daily():
        pass


async def call_exception_handler(collected_exceptions):
    """
    Calls the main client's exception handlers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    collected_exceptions : `list<DiscordException>
        The collected exceptions while reminding.
    """
    try:
        exception = collected_exceptions[-1]
        collected_exception_length = len(collected_exceptions)
        if collected_exception_length > 1:
            exception.__cause__ = CauseGroup(*islice(collected_exceptions, None, collected_exception_length - 1))
        
        await MAIN_CLIENT.events.error(MAIN_CLIENT, 'remind_forgot_daily', exception)
        
    finally:
        collected_exceptions = None
        exception = None


async def remind_forgot_daily_with_connector(connector):
    """
    Reminds the users who forgot to claim their daily.
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    """
    collected_exceptions = None
    
    results = await get_entries_to_notify_with_connector(connector)
    for entry in results:
        try:
            await notify_user(entry, connector)
        
        except DiscordException as exception:
            if collected_exceptions is None:
                collected_exceptions = []
            collected_exceptions.append(exception)
    
    if collected_exceptions is not None:
        try:
            await call_exception_handler(collected_exceptions)
        finally:
            collected_exceptions = None
