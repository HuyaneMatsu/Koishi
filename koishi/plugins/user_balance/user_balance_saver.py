__all__ = ()

from scarletio import copy_docs

from ...bot_utils.entry_proxy import EntryProxySaver
from ...bot_utils.models import USER_BALANCE_TABLE, user_balance_model


class UserBalanceSaver(EntryProxySaver):
    """
    Used to save user balance.
    
    Attributes
    ----------
    entry_proxy : ``UserBalance``
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
            USER_BALANCE_TABLE.delete().where(
                user_balance_model.id == entry_id,
            )
        )
    
    
    @copy_docs(EntryProxySaver._insert_entry)
    async def _insert_entry(self, connector, entry_proxy):
        response = await connector.execute(
            USER_BALANCE_TABLE.insert().values(
                user_id = entry_proxy.user_id,
                allocated = entry_proxy.allocated,
                balance = entry_proxy.balance,
                count_daily_self = entry_proxy.count_daily_self,
                count_daily_by_related = entry_proxy.count_daily_by_related,
                count_daily_for_related = entry_proxy.count_daily_for_related,
                count_top_gg_vote = entry_proxy.count_top_gg_vote,
                top_gg_voted_at = entry_proxy.top_gg_voted_at,
                daily_can_claim_at = entry_proxy.daily_can_claim_at,
                daily_reminded = entry_proxy.daily_reminded,
                streak = entry_proxy.streak,
                relationship_value = entry_proxy.relationship_value,
                relationship_divorces = entry_proxy.relationship_divorces,
                relationship_slots = entry_proxy.relationship_slots,
            ).returning(
                user_balance_model.id,
            )
        )
        
        result = await response.fetchone()
        return result[0]
    
    
    @copy_docs(EntryProxySaver._update_entry)
    async def _update_entry(self, connector, entry_id, modified_fields):
        await connector.execute(
            USER_BALANCE_TABLE.update(
                user_balance_model.id == entry_id,
            ).values(
                **modified_fields
            )
        )
