__all__ = ()

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxySaver
from ...bot_utils.models import GUILD_STATS_TABLE, guild_stats_model


class GuildStatsSaver(EntryProxySaver):
    """
    Used to save guild stats.
    
    Attributes
    ----------
    entry_proxy : ``GuildStats``
        The guild stats to save.
    
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
            GUILD_STATS_TABLE.delete().where(
                guild_stats_model.id == entry_id,
            )
        )
    
    
    @copy_docs(EntryProxySaver._insert_entry)
    async def _insert_entry(self, connector, entry_proxy):
        response = await connector.execute(
            GUILD_STATS_TABLE.insert().values(
                guild_id = entry_proxy.guild_id,
                credibility = entry_proxy.credibility,
            ).returning(
                guild_stats_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]
    
    
    @copy_docs(EntryProxySaver._update_entry)
    async def _update_entry(self, connector, entry_id, modified_fields):
        await connector.execute(
            GUILD_STATS_TABLE.update(
                guild_stats_model.id == entry_id,
            ).values(
                **modified_fields
            )
        )
