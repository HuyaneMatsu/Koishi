__all__ = ()

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxySaver
from ...bot_utils.models import RELATIONSHIP_TABLE, relationship_model


class RelationshipSaver(EntryProxySaver):
    """
    Used to save relationships.
    
    Attributes
    ----------
    entry_proxy : ``Relationship``
        The user balance to save.
    
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
            RELATIONSHIP_TABLE.delete().where(
                relationship_model.id == entry_id,
            )
        )
    
    
    @copy_docs(EntryProxySaver._insert_entry)
    async def _insert_entry(self, connector, entry_proxy):
        response = await connector.execute(
            RELATIONSHIP_TABLE.insert().values(
                relationship_type = entry_proxy.relationship_type,
                source_can_boost_at = entry_proxy.source_can_boost_at,
                source_investment = entry_proxy.source_investment,
                source_user_id = entry_proxy.source_user_id,
                target_can_boost_at = entry_proxy.target_can_boost_at,
                target_investment = entry_proxy.target_investment,
                target_user_id = entry_proxy.target_user_id,
            ).returning(
                relationship_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]
    
    
    @copy_docs(EntryProxySaver._update_entry)
    async def _update_entry(self, connector, entry_id, modified_fields):
        await connector.execute(
            RELATIONSHIP_TABLE.update(
                relationship_model.id == entry_id,
            ).values(
                **modified_fields
            )
        )
