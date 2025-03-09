__all__ = ('deepen_and_boost_relationship',)

from datetime import datetime as DateTime, timezone as TimeZone
from math import floor

from ...bot_utils.daily import BOOST_INTERVAL


async def deepen_and_boost_relationship(
    source_user_balance,
    target_user_balance,
    relationship_to_deepen,
    spent_balance,
    *,
    save_source_user_balance = 1,
    save_target_user_balance = 1,
    save_relationship_to_deepen = 1,
):
    """
    Deepens relationships and boosts them.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user_balance : ``UserBalance``
        The source user's balance.
    
    target_user_balance : `None | UserBalance`
        The target user's balance.
    
    relationship_to_deepen : `None | Relationship`
        The relationship or the connector relationship between the two users if available.
    
    spent_balance : `int`
        Balance based one what the deepening & boosting should happen.
    
    save_source_user_balance : `int` = `1`, Optional (Keyword only)
        Whether the source user balance should be saved.
    
    save_target_user_balance : `int` = `1`, Optional (Keyword only)
        Whether the target user balance should be saved.
    
    save_relationship_to_deepen : `int` = `1`, Optional (Keyword only)
        Whether the relationship to deepen should be saved.
    """
    relationship_investment_increase = max(floor(spent_balance * 0.01), 2)
    
    while True:
        if (relationship_to_deepen is None):
            # buying for yourself | or someone non related
            
            # If it is someone else half the amount.
            if (target_user_balance is not None):
                relationship_investment_increase >>= 1
            
            source_user_balance.set(
                'relationship_value',
                source_user_balance.relationship_value + relationship_investment_increase
            )
            save_source_user_balance += 1
            break
        
        # Buying for someone related
        
        # If it is an indirect relationship half the amount.
        source_user_id = source_user_balance.user_id
        target_user_id = target_user_balance.user_id
        
        if (
            (relationship_to_deepen.source_user_id != target_user_id) and
            (relationship_to_deepen.target_user_id != target_user_id)
        ):
            relationship_investment_increase >>= 1
        
        # Increment value
        if relationship_to_deepen.source_user_id == source_user_id:
            relationship_to_deepen.set(
                'source_investment',
                relationship_to_deepen.source_investment + relationship_investment_increase
            )
        else:
            relationship_to_deepen.set(
                'target_investment',
                relationship_to_deepen.target_investment + relationship_investment_increase
            )
        
        save_relationship_to_deepen += 1
        
        # Check when the next is available
        if relationship_to_deepen.source_user_id == source_user_id:
            can_boost_at = relationship_to_deepen.source_can_boost_at
        else:
            can_boost_at = relationship_to_deepen.target_can_boost_at
        
        now = DateTime.now(TimeZone.utc)
        if can_boost_at > now:
            break
        
        boosted_amount = max(floor(spent_balance * 0.05), 8)
        if (
            (relationship_to_deepen.source_user_id != target_user_id) and
            (relationship_to_deepen.target_user_id != target_user_id)
        ):
            boosted_amount >>= 1
        
        can_boost_at = now + BOOST_INTERVAL
        
        source_user_id = source_user_balance.user_id
        if relationship_to_deepen.source_user_id == source_user_id:
            relationship_to_deepen.set('source_can_boost_at', can_boost_at)
        else:
            relationship_to_deepen.set('target_can_boost_at', can_boost_at)
        
        source_user_balance.set('balance', source_user_balance.balance + boosted_amount)
        target_user_balance.set('balance', target_user_balance.balance + (boosted_amount >> 1))
        
        save_source_user_balance += 1
        save_target_user_balance += 1
        break
    
    if save_source_user_balance > 1:
        await source_user_balance.save()
    
    if save_target_user_balance > 1:
        await target_user_balance.save()
    
    if save_relationship_to_deepen > 1:
        await relationship_to_deepen.save()
