__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs
from sqlalchemy.sql import or_

from ...bot_utils.models import DB_ENGINE, EXTERNAL_EVENTS_TABLE, external_events_model

from .external_event import ExternalEvent


async def pull_external_events():
    """
    Pulls the external events from the database.
    
    This function is a coroutine.
    
    Returns
    -------
    external_events : `list<ExternalEvent>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            EXTERNAL_EVENTS_TABLE.select().where(
                or_(
                    external_events_model.trigger_after == None,
                    external_events_model.trigger_after >= DateTime.now(TimeZone.utc),
                ),
            ),
        )
        
        external_events = []
        
        entries = await response.fetchall()
        for entry in entries:
            external_events.append(ExternalEvent.from_entry(entry))
        
        return external_events


if DB_ENGINE is None:
    @copy_docs(pull_external_events)
    async def pull_external_events():
        return []


async def remove_external_events(external_event_ids):
    """
    Removes the
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
