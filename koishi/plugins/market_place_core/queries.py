__all__ = (
    'delete_market_place_item', 'get_market_place_item', 'get_market_place_item_listing_active',
    'get_market_place_item_listing_inbox', 'get_market_place_item_listing_own_offers', 'insert_market_place_item',
    'update_market_place_item'
)

from itertools import count, islice

from scarletio import copy_docs
from sqlalchemy import and_, or_
from sqlalchemy.sql import asc, desc

from ...bot_utils.models import DB_ENGINE, MARKET_PLACE_ITEM_TABLE, market_place_item_model

from .constants import FINALISED_KEPT_DURATION, MARKET_PLACE_ITEMS
from .market_place_item import MarketPlaceItem


if (DB_ENGINE is None):
    from .constants import MARKET_PLACE_ITEMS_CACHE
    
    COUNTER = iter(count(1))

    def _sort_by_finalises_at_sort_key_getter(item):
        """
        Helper function to get sort key when sorting by `.finalises_at`.
        
        Parameters
        ----------
        item : ``MarketPlaceItem``
            Item to get sort key of.
        
        Returns
        -------
        sort_key : `DateTime`
        """
        return item.finalises_at


async def insert_market_place_item(market_place_item):
    """
    Inserts the market place item into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The item to insert.
    """
    if market_place_item.entry_id:
        return
    
    entry_id = await query_insert_market_place_item(market_place_item)
    MARKET_PLACE_ITEMS[entry_id] = market_place_item
    market_place_item.entry_id = entry_id


async def query_insert_market_place_item(market_place_item):
    """
    Executes a query to insert the market place entry into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The item to insert.
    
    Returns
    -------
    entry_id : `int`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            MARKET_PLACE_ITEM_TABLE.insert().values(
                finalises_at = market_place_item.finalises_at,
                initial_sell_fee = market_place_item.initial_sell_fee,
                item_id = market_place_item.item_id,
                item_flags = market_place_item.item_flags,
                item_amount = market_place_item.item_amount,
                seller_user_id = market_place_item.seller_user_id,
                seller_balance_amount = market_place_item.seller_balance_amount,
            ).returning(    
                market_place_item_model.id,
            ),
        )
        
        entry = await response.fetchone()
        return entry[0]


if (DB_ENGINE is None):
    @copy_docs(query_insert_market_place_item)
    async def query_insert_market_place_item(market_place_item):
        MARKET_PLACE_ITEMS_CACHE.append(market_place_item)
        return next(COUNTER)


async def update_market_place_item(market_place_item):
    """
    Updates the market place item into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The item to update.
    """
    if not market_place_item.entry_id:
        return
    
    await query_update_market_place_item(market_place_item)


async def query_update_market_place_item(market_place_item):
    """
    Executes a query to update the market place entry into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The item to update.
    """
    # Updated before finalisation:
    # - purchaser_user_id
    # - purchaser_balance_amount
    # - finalises_at
    #
    # Updated after finalisation:
    # - flags
    
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            MARKET_PLACE_ITEM_TABLE.update(
                market_place_item_model.id == market_place_item.entry_id
            ).values(
                finalises_at = market_place_item.finalises_at,
                flags = market_place_item.flags,
                purchaser_balance_amount = market_place_item.purchaser_balance_amount,
                purchaser_user_id = market_place_item.purchaser_user_id,
            ),
        )


if (DB_ENGINE is None):
    @copy_docs(query_update_market_place_item)
    async def query_update_market_place_item(market_place_item):
        return


async def delete_market_place_item(market_place_item):
    """
    Deletes the market place item into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The item to delete.
    """
    if not market_place_item.entry_id:
        return
    
    await query_delete_market_place_item(market_place_item)
    try:
        del MARKET_PLACE_ITEMS[market_place_item.entry_id]
    except KeyError:
        pass


async def query_delete_market_place_item(market_place_item):
    """
    Executes a query to delete the market place entry into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item : ``MarketPlaceItem``
        The item to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            MARKET_PLACE_ITEM_TABLE.delete().where(
                market_place_item_model.id == market_place_item.entry_id
            ),
        )


if (DB_ENGINE is None):
    @copy_docs(query_delete_market_place_item)
    async def query_delete_market_place_item(market_place_item):
        try:
            MARKET_PLACE_ITEMS_CACHE.remove(market_place_item)
        except ValueError:
            pass


async def delete_market_place_item_listing(market_place_item_listing):
    """
    Deletes the market place items into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item_listing : ``list<MarketPlaceItem>``
        The items to delete.
    """
    await query_delete_market_place_item_listing(market_place_item_listing)
    
    for market_place_item in market_place_item_listing:
        try:
            del MARKET_PLACE_ITEMS[market_place_item.entry_id]
        except KeyError:
            pass


async def query_delete_market_place_item_listing(market_place_item_listing):
    """
    Executes a query to delete the market place entry into the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    market_place_item_listing : ``list<MarketPlaceItem>``
        The items to delete.
    """
    async with DB_ENGINE.connect() as connector:
        await connector.execute(
            MARKET_PLACE_ITEM_TABLE.delete().where(
                market_place_item_model.id.in_([market_place_item.entry_id for market_place_item in market_place_item_listing])
            ),
        )


if (DB_ENGINE is None):
    @copy_docs(query_delete_market_place_item_listing)
    async def query_delete_market_place_item_listing(market_place_item_listing):
        for market_place_item in market_place_item_listing:
            try:
                MARKET_PLACE_ITEMS_CACHE.remove(market_place_item)
            except ValueError:
                pass


async def get_market_place_item(entry_id):
    """
    Gets the market place item.
    
    Parameters
    ----------
    entry_id : `int`
        The entry's identifier.
    
    Returns
    -------
    market_place_item : ``None | MarketPlaceItem``
    """
    return await query_get_market_place_item(entry_id)


async def query_get_market_place_item(entry_id):
    """
    Executes a query to get the market place items for the given entry identifier.
    
    Parameters
    ----------
    entry_id : `int`
        The entry's identifier.
    
    Returns
    -------
    market_place_item : ``None | MarketPlaceItem``
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            MARKET_PLACE_ITEM_TABLE.select().where(
                and_(
                    market_place_item_model.id == entry_id,
                )
            ),
        )
        
        entry = (await response.fetchone())
    
    if entry is None:
        return
    
    try:
        market_place_item = MARKET_PLACE_ITEMS[entry_id]
    except KeyError:
        market_place_item = MarketPlaceItem.from_entry(entry)
        MARKET_PLACE_ITEMS[entry_id] = market_place_item
    
    return market_place_item


if (DB_ENGINE is None):
    @copy_docs(query_get_market_place_item)
    async def query_get_market_place_item(entry_id):
        for market_place_item in MARKET_PLACE_ITEMS_CACHE:
            if market_place_item.entry_id == entry_id:
                return market_place_item


async def get_market_place_item_listing_own_offers(user_id, now, page_index, page_size):
    """
    Gets the active market place entries for the given seller user's identifier.
    
    Parameters
    ----------
    user_id : `int`
        Seller user's identifier.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index to get.
    
    page_size : `int`
        The page's size to get.
    
    Returns
    -------
    market_place_item_listing_and_has_more : ``(list<MarketPlaceItem>, bool)``
    """
    market_place_item_listing = await query_get_market_place_item_listing_own_offers(user_id, now)
    page_start = page_index * page_size
    page_end = page_start + page_size
    
    return market_place_item_listing[page_start : page_end], (len(market_place_item_listing) > page_end)


async def query_get_market_place_item_listing_own_offers(user_id, now):
    """
    Executes a query to get the market place items for the given seller user's identifier from the database.
    
    Parameters
    ----------
    user_id : `int`
        Seller user's identifier.
    
    now : `DateTime`
        The current time.
    
    Returns
    -------
    market_place_item_listing : ``list<MarketPlaceItem>``
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            MARKET_PLACE_ITEM_TABLE.select().where(
                and_(
                    market_place_item_model.finalises_at > now,
                    market_place_item_model.seller_user_id == user_id,
                )
            ).order_by(
                asc(market_place_item_model.finalises_at),
            ),
        )
        
        entries = (await response.fetchall())
    
    market_place_item_listing = []
    for entry in entries:
        entry_id = entry['id']
        try:
            market_place_item = MARKET_PLACE_ITEMS[entry_id]
        except KeyError:
            market_place_item = MarketPlaceItem.from_entry(entry)
            MARKET_PLACE_ITEMS[entry_id] = market_place_item
        
        market_place_item_listing.append(market_place_item)
    
    return market_place_item_listing


if (DB_ENGINE is None):
    @copy_docs(query_get_market_place_item_listing_own_offers)
    async def query_get_market_place_item_listing_own_offers(user_id, now):
        return sorted(
            (
                market_place_item for market_place_item in MARKET_PLACE_ITEMS_CACHE
                if (market_place_item.finalises_at > now) and (market_place_item.seller_user_id == user_id) 
            ),
            key = _sort_by_finalises_at_sort_key_getter,
        )


async def get_market_place_item_listing_inbox(user_id, now, page_index, page_size):
    """
    Gets the finalised market place entries for the given user's identifier.
    
    Parameters
    ----------
    user_id : `int`
        Seller user's identifier.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index to get.
    
    page_size : `int`
        The page's size to get.
    
    Returns
    -------
    market_place_item_listing_and_has_more : ``(list<MarketPlaceItem>, bool)``
    """
    market_place_item_listing = await query_get_market_place_item_listing_inbox(user_id, now)
    
    finalised_kept_timeout = now - FINALISED_KEPT_DURATION
    market_place_item_listing_to_delete = None
    while market_place_item_listing:
        market_place_item = market_place_item_listing[-1]
        if market_place_item.finalises_at > finalised_kept_timeout:
            break
        
        if market_place_item_listing_to_delete is None:
            market_place_item_listing_to_delete = []
        
        market_place_item_listing_to_delete.append(market_place_item)
        del market_place_item_listing[-1]
        continue
    
    if (market_place_item_listing_to_delete is not None):
        await delete_market_place_item_listing(market_place_item_listing_to_delete)
        market_place_item_listing_to_delete = None
    
    page_start = page_index * page_size
    page_end = page_start + page_size
    
    return market_place_item_listing[page_start : page_end], (len(market_place_item_listing) > page_end)


async def query_get_market_place_item_listing_inbox(user_id, now):
    """
    Executes a query to get the finalised market place items for the given user's identifier from the database.
    
    Parameters
    ----------
    user_id : `int`
        Seller user's identifier.
    
    now : `DateTime`
        The current time.
    
    Returns
    -------
    market_place_item_listing : ``list<MarketPlaceItem>``
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            MARKET_PLACE_ITEM_TABLE.select().where(
                and_(
                    market_place_item_model.finalises_at <= now,
                    or_(
                        market_place_item_model.purchaser_user_id == user_id,
                        market_place_item_model.seller_user_id == user_id,
                    ),
                )
            ).order_by(
                desc(market_place_item_model.finalises_at),
            ),
        )
        
        entries = (await response.fetchall())
    
    market_place_item_listing = []
    for entry in entries:
        entry_id = entry['id']
        try:
            market_place_item = MARKET_PLACE_ITEMS[entry_id]
        except KeyError:
            market_place_item = MarketPlaceItem.from_entry(entry)
            MARKET_PLACE_ITEMS[entry_id] = market_place_item
        
        market_place_item_listing.append(market_place_item)
    
    return market_place_item_listing


if (DB_ENGINE is None):
    @copy_docs(query_get_market_place_item_listing_inbox)
    async def query_get_market_place_item_listing_inbox(user_id, now):
        return sorted(
            (
                market_place_item for market_place_item in MARKET_PLACE_ITEMS_CACHE
                if (
                    (market_place_item.finalises_at <= now)
                    and (
                        (market_place_item.purchaser_user_id == user_id) or 
                        (market_place_item.seller_user_id == user_id)
                    )
                )
            ),
            key = _sort_by_finalises_at_sort_key_getter,
            reverse = True,
        )


async def get_market_place_item_listing_active(item_id, item_flags, now, page_index, page_size):
    """
    Gets the finalised market place entries for the given user's identifier.
    
    Parameters
    ----------
    item_id : `int`
        Item identifier to filter for.
    
    item_flags : `int`
        Item flags to filter for.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index to get.
    
    page_size : `int`
        The page's size to get.
    
    Returns
    -------
    market_place_item_listing_and_has_more : ``(list<MarketPlaceItem>, bool)``
    """
    return await query_get_market_place_item_listing_active(
        item_id, item_flags, now, page_index, page_size
    )


async def query_get_market_place_item_listing_active(item_id, item_flags, now, page_index, page_size):
    """
    Executes a query to get the finalised market place items for the given user's identifier from the database.
    
    Parameters
    ----------
    item_id : `int`
        Item identifier to filter for.
    
    item_flags : `int`
        Item flags to filter for.
    
    now : `DateTime`
        The current time.
    
    page_index : `int`
        The page's index to get.
    
    page_size : `int`
        The page's size to get.
    
    Returns
    -------
    market_place_item_listing_and_has_more : ``(list<MarketPlaceItem>, bool)``
    """
    async with DB_ENGINE.connect() as connector:
        condition = market_place_item_model.finalises_at > now
        
        if item_id:
            condition = and_(
                condition,
                market_place_item_model.item_id == item_id,
            )
        elif item_flags:
            condition = and_(
                condition,
                market_place_item_model.item_flags.op('&')(item_flags) != 0
            )
        
        response = await connector.execute(
            MARKET_PLACE_ITEM_TABLE.select().where(
                condition,
            ).order_by(
                asc(market_place_item_model.finalises_at),
            ).limit(
                page_size + 1,
            ).offset(
                page_size * page_index,
            )
        )
        
        has_more = (response.rowcount > page_size)
        
        entries = (await response.fetchall())
    
    
    market_place_item_listing = []
    for entry in islice(entries, 0, page_size):
        entry_id = entry['id']
        try:
            market_place_item = MARKET_PLACE_ITEMS[entry_id]
        except KeyError:
            market_place_item = MarketPlaceItem.from_entry(entry)
            MARKET_PLACE_ITEMS[entry_id] = market_place_item
        
        market_place_item_listing.append(market_place_item)
    
    return market_place_item_listing, has_more


if (DB_ENGINE is None):
    @copy_docs(query_get_market_place_item_listing_active)
    async def query_get_market_place_item_listing_active(item_id, item_flags, now, page_index, page_size):
        generator = (
            market_place_item for market_place_item in MARKET_PLACE_ITEMS_CACHE
            if market_place_item.finalises_at > now
        )
        
        if item_id:
            generator = (
                market_place_item for market_place_item in generator
                if market_place_item.item_id == item_id
            )
        elif item_flags:
            generator = (
                market_place_item for market_place_item in generator
                if market_place_item.item_flags & item_flags == item_flags
            )
        
        market_place_item_listing = sorted(generator, key = _sort_by_finalises_at_sort_key_getter)
        page_start = page_index * page_size
        page_end = page_start + page_size
        has_more = (len(market_place_item_listing) > page_end)
        return market_place_item_listing[page_start : page_end], has_more
