__all__ = ('insert_external_event', 'insert_external_event_with_connector')

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs, to_json
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import or_

from ...bot_utils.models import DB_ENGINE, EXTERNAL_EVENTS_TABLE, external_events_model

from .external_event import ExternalEvent


if DB_ENGINE:
    from itertools import count
    
    COUNTER = iter(count(1))
    EXTERNAL_EVENTS_CACHE = {}


async def pull_external_events():
    """
    Pulls the external events from the database.
    
    This function is a coroutine.
    
    Returns
    -------
    external_events : ``list<ExternalEvent>``
    """
    try:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                EXTERNAL_EVENTS_TABLE.select().where(
                    or_(
                        external_events_model.trigger_after == None,
                        external_events_model.trigger_after <= DateTime.now(TimeZone.utc),
                    ),
                ),
            )
            entries = await response.fetchall()
    
    except OperationalError:
        return None
    
    if not entries:
        return None
    
    return [ExternalEvent.from_entry(entry) for entry in entries]


if DB_ENGINE is None:
    @copy_docs(pull_external_events)
    async def pull_external_events():
        external_events = None
        
        now = DateTime.now(TimeZone.utc)
        
        for value in EXTERNAL_EVENTS_CACHE:
            trigger_after = value['trigger_after']
            if not ((trigger_after is None) or (trigger_after <= now)):
                continue
            
            if external_events is None:
                external_events = []
            
            external_events.append(ExternalEvent.from_entry(value))
        
        return external_events


async def remove_external_events(external_event_ids):
    """
    Removes the external event from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    external_event_ids : `list<int>`
        Identifiers of external events to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            EXTERNAL_EVENTS_TABLE.delete().where(
                external_events_model.id.in_(external_event_ids)
            )
        )


if DB_ENGINE is None:
    @copy_docs(remove_external_events)
    async def remove_external_events(external_event_ids):
        for external_event_id in external_event_ids:
            try:
                del EXTERNAL_EVENTS_CACHE[external_event_id]
            except KeyError:
                pass


async def insert_external_event(
    client_id = 0,
    event_data = None,
    event_type = 0,
    guild_id = 0,
    trigger_after = None,
    user_id = 0,
):
    """
    Inserts a new external event into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client_id : `int` = `0`, Optional (Keyword only)
        The client's identifier to who this event is related to.
    
    event_data : `None | object` = `None`, Optional (Keyword only)
        Additional event data.
    
    event_type : `int` = `0`, Optional (Keyword only)
        The event's type.
    
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild identifier the event is bound to.
    
    trigger_after : `None | DateTime` = `None`, Optional (Keyword only)
        After when the event should be triggered.
    
    user_id : `int` = `0`, Optional (Keyword only)
        The user to who this event is related to.
    """
    if (event_data is not None):
        event_data = to_json(event_data)
    
    async with DB_ENGINE.connect() as connector:
        await _insert_external_event_with_connector(
            connector,
            client_id,
            event_data,
            event_type,
            guild_id ,
            trigger_after,
            user_id,
        )


if DB_ENGINE is None:
    @copy_docs(insert_external_event)
    async def insert_external_event(
        client_id = 0,
        event_data = None,
        event_type = 0,
        guild_id = 0,
        trigger_after = None,
        user_id = 0,
    ):
        if (event_data is not None):
            event_data = to_json(event_data)
        
        await _insert_external_event_with_connector(
            None,
            client_id,
            event_data,
            event_type,
            guild_id ,
            trigger_after,
            user_id,
        )


async def insert_external_event_with_connector(
    connector,
    client_id = 0,
    event_data = None,
    event_type = 0,
    guild_id = 0,
    trigger_after = None,
    user_id = 0,
):
    """
    Inserts a new external event into the database with the given connector-
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    
    client_id : `int` = `0`, Optional (Keyword only)
        The client's identifier to who this event is related to.
    
    event_data : `None | object` = `None`, Optional (Keyword only)
        Additional event data.
    
    event_type : `int` = `0`, Optional (Keyword only)
        The event's type.
    
    guild_id : `int` = `0`, Optional (Keyword only)
        The guild identifier the event is bound to.
    
    trigger_after : `None | DateTime` = `None`, Optional (Keyword only)
        After when the event should be triggered.
    
    user_id : `int` = `0`, Optional (Keyword only)
        The user to who this event is related to.
    """
    if (event_data is not None):
        event_data = to_json(event_data)
    
    await _insert_external_event_with_connector(
        connector,
        client_id,
        event_data,
        event_type,
        guild_id ,
        trigger_after,
        user_id,
    )

async def _insert_external_event_with_connector(
    connector,
    client_id,
    event_data,
    event_type,
    guild_id ,
    trigger_after,
    user_id,
):
    """
    Internal function to insert the external event into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    
    client_id : `int`
        The client's identifier to who this event is related to.
    
    event_data : `None | object`
        Additional event data.
    
    event_type : `int`
        The event's type.
    
    guild_id : `int`
        The guild identifier the event is bound to.
    
    trigger_after : `None | DateTime`
        After when the event should be triggered.
    
    user_id : `int` = `0`
        The user to who this event is related to.
    """
    await connector.execute(
        EXTERNAL_EVENTS_TABLE.insert().values(
            client_id = client_id,
            user_id = user_id,
            guild_id = guild_id,
            event_type = event_type,
            event_data = event_data,
            trigger_after = trigger_after,
        ),
    )


if DB_ENGINE is None:
    @copy_docs(_insert_external_event_with_connector)
    async def _insert_external_event_with_connector(
        connector,
        client_id,
        event_data,
        event_type,
        guild_id ,
        trigger_after,
        user_id,
    ):
        if (event_data is not None):
            event_data = to_json(event_data)
        
        entry_id = next(COUNTER)
        
        EXTERNAL_EVENTS_CACHE[entry_id] = {
            'event_data': event_data,
            'client_id': client_id,
            'trigger_after': trigger_after,
            'id': entry_id,
            'event_type': event_type,
            'guild_id': guild_id,
            'user_id': user_id,
        }
