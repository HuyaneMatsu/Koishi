__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from scarletio import copy_docs
from sqlalchemy import and_, or_
from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE, MARKET_PLACE_ITEM_TABLE, market_place_item_model, user_settings_model

from ..user_settings import USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION
from ..market_place_core import (
    MARKET_PLACE_ITEM_FLAG_PURCHASER_RETRIEVED, MARKET_PLACE_ITEM_FLAG_PURCHASER_FINALISATION_NOTIFICATION_DELIVERED,
    MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED, MARKET_PLACE_ITEM_FLAG_SELLER_FINALISATION_NOTIFICATION_DELIVERED
)

if (DB_ENGINE is None):
    from ..market_place_core import MARKET_PLACE_ITEMS_CACHE
    from ..user_settings import USER_SETTINGS_CACHE, USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT


MARKET_PLACE_ITEM_FLAG_MASK_PURCHASER = (
    MARKET_PLACE_ITEM_FLAG_PURCHASER_RETRIEVED | MARKET_PLACE_ITEM_FLAG_PURCHASER_FINALISATION_NOTIFICATION_DELIVERED
)
MARKET_PLACE_ITEM_FLAG_MASK_SELLER = (
    MARKET_PLACE_ITEM_FLAG_SELLER_RETRIEVED | MARKET_PLACE_ITEM_FLAG_SELLER_FINALISATION_NOTIFICATION_DELIVERED
)


NOTIFICATION_FLAG_MASK = 1 << USER_SETTINGS_NOTIFICATION_FLAG_SHIFT_MARKET_PLACE_ITEM_FINALISATION


async def get_entries_to_notify_with_connector(connector):
    """
    Gets entries which should be notified.
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    FV
    Returns
    -------
    results : `list<sqlalchemy.engine.result.RowProxy<int, int, int, int, int, int, int, int, int, int>>`
    """
    response = await connector.execute(
        select(
            [
                market_place_item_model.id,
                market_place_item_model.flags,
                market_place_item_model.seller_user_id,
                market_place_item_model.purchaser_user_id,
                
                market_place_item_model.item_id,
                market_place_item_model.item_amount,
                market_place_item_model.seller_balance_amount,
                market_place_item_model.purchaser_balance_amount,
                
                user_settings_model.user_id,
                user_settings_model.preferred_client_id,
            ],
        ).where(
            and_(
                market_place_item_model.finalises_at <= DateTime.now(TimeZone.utc),
                or_(
                    and_(
                        user_settings_model.user_id == market_place_item_model.seller_user_id,
                        market_place_item_model.flags.op('&')(MARKET_PLACE_ITEM_FLAG_MASK_SELLER) == 0,
                    ),
                    and_(
                        user_settings_model.user_id != 0,
                        user_settings_model.user_id == market_place_item_model.purchaser_user_id,
                        market_place_item_model.flags.op('&')(MARKET_PLACE_ITEM_FLAG_MASK_PURCHASER) == 0,
                    ),
                ),
                user_settings_model.notification_flags.op('&')(NOTIFICATION_FLAG_MASK) != 0,
            )
        )
    )
    
    return await response.fetchall()


if DB_ENGINE is None:
    @copy_docs(get_entries_to_notify_with_connector)
    async def get_entries_to_notify_with_connector(connector):
        remind_before = DateTime.now(TimeZone.utc)
        results = []
        
        for market_place_item in MARKET_PLACE_ITEMS_CACHE:
            if not (market_place_item.finalises_at <= remind_before):
                continue
            
            for user_id, flag_mask in (
                (market_place_item.seller_user_id, MARKET_PLACE_ITEM_FLAG_MASK_SELLER),
                (market_place_item.purchaser_user_id, MARKET_PLACE_ITEM_FLAG_MASK_PURCHASER),
            ):
                if not user_id:
                    continue
                
                user_settings = USER_SETTINGS_CACHE.get(user_id, None)
                if (user_settings is None):
                    notification_flags = USER_SETTINGS_NOTIFICATION_FLAG_DEFAULT
                    preferred_client_id = 0
                else:
                    notification_flags = user_settings.notification_flags
                    preferred_client_id = user_settings.preferred_client_id
                
                if not (market_place_item.flags & flag_mask == 0):
                    continue
                
                if not (notification_flags & NOTIFICATION_FLAG_MASK != 0):
                    continue
                
                results.append((
                    market_place_item.entry_id,
                    market_place_item.flags,
                    market_place_item.seller_user_id,
                    market_place_item.purchaser_user_id,
                    
                    market_place_item.item_id,
                    market_place_item.item_amount,
                    market_place_item.seller_balance_amount,
                    market_place_item.purchaser_balance_amount,
                    
                    user_id,
                    preferred_client_id,
                ))
        
        return results


async def set_entry_as_notified_with_connector(connector, entry_id, mark_seller):
    """
    Sets the entry as notified.
    
    This function is a coroutine.
    
    Parameters
    ----------
    connector : ``AsyncConnection``
        Database connector.
    
    entry_id : `int`
        The entry's id to interact with.
    
    mark_seller : `bool`
        Whether to mark the seller (or the purchaser).
    """
    if mark_seller:
        flag = MARKET_PLACE_ITEM_FLAG_SELLER_FINALISATION_NOTIFICATION_DELIVERED
    else:
        flag = MARKET_PLACE_ITEM_FLAG_PURCHASER_FINALISATION_NOTIFICATION_DELIVERED
    
    await connector.execute(
        MARKET_PLACE_ITEM_TABLE.update(
            market_place_item_model.id == entry_id,
        ).values(
            flags = market_place_item_model.flags.op('|')(flag),
        )
    )


if DB_ENGINE is None:
    @copy_docs(set_entry_as_notified_with_connector)
    async def set_entry_as_notified_with_connector(connector, entry_id, mark_seller):
        if mark_seller:
            flag = MARKET_PLACE_ITEM_FLAG_SELLER_FINALISATION_NOTIFICATION_DELIVERED
        else:
            flag = MARKET_PLACE_ITEM_FLAG_PURCHASER_FINALISATION_NOTIFICATION_DELIVERED
        
        for market_place_item in MARKET_PLACE_ITEMS_CACHE:
            if market_place_item.entry_id == entry_id:
                market_place_item.flags |= flag
                break
