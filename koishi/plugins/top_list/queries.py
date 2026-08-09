__all__ = ()

from hata import DiscordException, ERROR_CODES, ZEROUSER
from scarletio import copy_docs
from sqlalchemy.sql import desc, select

from ...bot_utils.models import DB_ENGINE, user_balance_model, user_stats_model
from ...bot_utils.user_getter import get_user

from .constants import PAGE_SIZE, TOP_LIST_TYPE_BALANCE, TOP_LIST_TYPE_CREDIBILITY


async def request_top_list_balance_entries(page_index):
    """
    Requests top list balance entries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    page_index : `int`
        The page index to request (0 based).
    
    Returns
    -------
    entries : `list<sqlalchemy.engine.result.RowProxy>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_balance_model.user_id,
                    user_balance_model.balance,
                ],
            ).where(
                user_balance_model.balance > 0,
            ).order_by(
                desc(user_balance_model.balance),
            ).limit(
                PAGE_SIZE + 1,
            ).offset(
                PAGE_SIZE * page_index,
            )
        )
        
        return await response.fetchall()


if DB_ENGINE is None:
    @copy_docs(request_top_list_balance_entries)
    async def request_top_list_balance_entries(page_index):
        return []


async def request_top_list_credibility_entries(page_index):
    """
    Requests top list credibility entries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    page_index : `int`
        The page index to request (0 based).
    
    Returns
    -------
    entries : `list<sqlalchemy.engine.result.RowProxy>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            select(
                [
                    user_stats_model.user_id,
                    user_stats_model.credibility,
                ],
            ).where(
                user_stats_model.credibility > 0,
            ).order_by(
                desc(user_stats_model.credibility),
            ).limit(
                PAGE_SIZE + 1,
            ).offset(
                PAGE_SIZE * page_index,
            )
        )
        
        return await response.fetchall()


if DB_ENGINE is None:
    @copy_docs(request_top_list_credibility_entries)
    async def request_top_list_credibility_entries(page_index):
        return []


async def process_entries(page_index, entries):
    """
    Processes the given entries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    
    entries : `list<sqlalchemy.engine.result.RowProxy>`
        Raw entries to process.
    
    Returns
    -------
    processed_entries_and_has_more : ``(list<(ClientUserBase, int)>, bool)``
    """
    processed_entries = []
    
    for index in range(min(len(entries), PAGE_SIZE)):
        user_id, value = entries[index]
        try:
            user = await get_user(user_id)
        except BaseException as err:
            if isinstance(err, ConnectionError):
                return
            
            if isinstance(err, DiscordException):
                if err.code == ERROR_CODES.unknown_user:
                    user = ZEROUSER
                else:
                    raise
            
            else:
                raise
        
        processed_entries.append((user, value))
    
    return processed_entries, (len(entries) > PAGE_SIZE)


async def get_top_list_entries(top_list_type, page_index):
    """
    Requests and processes the given entries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    top_list_type : `int`
        Top list's type.
    
    page_index : `int`
        Page index (0 based).
    
    Returns
    -------
    processed_entries_and_has_more : ``(list<(ClientUserBase, int)>, bool)``
    """
    if top_list_type == TOP_LIST_TYPE_BALANCE:
        request_function = request_top_list_balance_entries
    elif top_list_type == TOP_LIST_TYPE_CREDIBILITY:
        request_function = request_top_list_credibility_entries
    else:
        return [], False
        
    entries = await request_function(page_index)
    return await process_entries(page_index, entries)
