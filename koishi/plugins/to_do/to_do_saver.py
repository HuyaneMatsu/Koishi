__all__ = ()

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxySaver
from ...bot_utils.models import TODO_TABLE, todo_model


class ToDoSaver(EntryProxySaver):
    """
    Used to save to-do.
    
    Attributes
    ----------
    entry_proxy : ``ToDo``
        The to-do to save.
    
    ensured_for_deletion : `bool`
        Whether the entry should be deleted.
    
    modified_fields : `None | dict<str, object>`
        The fields to modify.
    
    run_task : `None | Task<.run>`
        Whether the saver is already running.
    """
    __slots__ = ()
    
    @copy_docs(EntryProxySaver._delete_entry)
    async def _delete_entry(self, connector, entry_id):
        await connector.execute(
            TODO_TABLE.delete().where(
                todo_model.id == entry_id,
            )
        )
    
    
    @copy_docs(EntryProxySaver._insert_entry)
    async def _insert_entry(self, connector, entry_proxy):
        response = await connector.execute(
            TODO_TABLE.insert().values(
                created_at = entry_proxy.created_at,
                creator_id = entry_proxy.creator_id,
                description = entry_proxy.description,
                name = entry_proxy.name,
            ).returning(
                todo_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]
    
    
    @copy_docs(EntryProxySaver._update_entry)
    async def _update_entry(self, connector, entry_id, modified_fields):
        await connector.execute(
            TODO_TABLE.update(
                todo_model.id == entry_id,
            ).values(
                **modified_fields
            )
        )
