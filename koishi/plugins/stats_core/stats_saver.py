__all__ = ()

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxySaver
from ...bot_utils.models import STATS_TABLE, stats_model


class StatsSaver(EntryProxySaver):
    """
    Used to save stats.
    
    Attributes
    ----------
    entry_proxy : ``RelationshipRequest``
        The stats to save.
    
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
            STATS_TABLE.delete().where(
                stats_model.id == entry_id,
            )
        )
    
    
    @copy_docs(EntryProxySaver._insert_entry)
    async def _insert_entry(self, connector, entry_proxy):
        response = await connector.execute(
            STATS_TABLE.insert().values(
                stat_housewife = entry_proxy.stat_housewife,
                stat_cuteness = entry_proxy.stat_cuteness,
                stat_bedroom = entry_proxy.stat_bedroom,
                stat_charm = entry_proxy.stat_charm,
                stat_loyalty = entry_proxy.stat_loyalty,
                
                credibility = entry_proxy.credibility,
                
                item_id_costume = entry_proxy.item_id_costume,
                item_id_head = entry_proxy.item_id_head,
                item_id_species = entry_proxy.item_id_species,
                item_id_weapon = entry_proxy.item_id_weapon,
            ).returning(
                stats_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]
    
    
    @copy_docs(EntryProxySaver._update_entry)
    async def _update_entry(self, connector, entry_id, modified_fields):
        await connector.execute(
            STATS_TABLE.update(
                stats_model.id == entry_id,
            ).values(
                **modified_fields
            )
        )
