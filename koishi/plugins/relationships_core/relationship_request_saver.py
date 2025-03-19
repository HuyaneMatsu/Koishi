__all__ = ()

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxySaver
from ...bot_utils.models import RELATIONSHIP_REQUEST_TABLE, relationship_request_model


class RelationshipRequestSaver(EntryProxySaver):
    """
    Used to save relationship requests.
    
    Attributes
    ----------
    entry_proxy : ``RelationshipRequest``
        The relationship request to save.
    
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
            RELATIONSHIP_REQUEST_TABLE.delete().where(
                relationship_request_model.id == entry_id,
            )
        )
    
    
    @copy_docs(EntryProxySaver._insert_entry)
    async def _insert_entry(self, connector, entry_proxy):
        response = await connector.execute(
            RELATIONSHIP_REQUEST_TABLE.insert().values(
                investment = entry_proxy.investment,
                relationship_type = entry_proxy.relationship_type,
                source_user_id = entry_proxy.source_user_id,
                target_user_id = entry_proxy.target_user_id,
            ).returning(
                relationship_request_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]
    
    
    @copy_docs(EntryProxySaver._update_entry)
    async def _update_entry(self, connector, entry_id, modified_fields):
        await connector.execute(
            RELATIONSHIP_REQUEST_TABLE.update(
                relationship_request_model.id == entry_id,
            ).values(
                **modified_fields
            )
        )
