__all__ = ()

from scarletio import copy_docs
from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE, todo_model

from .to_do import ToDo


async def query_to_dos():
    """
    Requests the to do entries from the database.
    
    This function is a coroutine.
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    todo_model.id,
                    todo_model.name,
                    todo_model.description,
                    todo_model.created_at,
                    todo_model.creator_id,
                ]
            )
        )
        
        results = await response.fetchall()
        for result in results:
            ToDo.from_entry(result)


if (DB_ENGINE is None):
    @copy_docs(query_to_dos)
    async def query_to_dos():
        return
