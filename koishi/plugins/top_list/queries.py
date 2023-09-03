__all__ = ()

from hata import DiscordException, ERROR_CODES, ZEROUSER
from scarletio import copy_docs
from sqlalchemy.sql import desc, select

from ...bot_utils.models import DB_ENGINE, user_common_model
from ...bot_utils.user_getter import get_user

from .constants import PAGE_SIZE


async def request_top_list_entries(page_index):
    """
    Gets top list entries.
    
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
                    user_common_model.user_id,
                    user_common_model.total_love,
                ]
            ).where(
                user_common_model.total_love != 0,
            ).order_by(
                desc(user_common_model.total_love),
            ).limit(
                PAGE_SIZE,
            ).offset(
                PAGE_SIZE * page_index,
            )
        )
        
        return await response.fetchall()


if DB_ENGINE is None:
    @copy_docs(request_top_list_entries)
    async def request_top_list_entries(page_index):
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
    processed_entries : `list<(int, int, ClientUserBase)`
    """
    processed_entries = []

    for number, (user_id, total_hearts) in enumerate(entries, (page_index * 20) + 1):
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
        
        processed_entries.append((number, total_hearts, user))
    
    return processed_entries


async def get_top_list_entries(page_index):
    """
    Requests and processes the given entries.
    
    This function is a coroutine.
    
    Parameters
    ----------
    page_index : `int`
        Page index (0 based).
    
    Returns
    -------
    processed_entries : `list<(int, int, ClientUserBase)`
    """
    entries = await request_top_list_entries(page_index)
    return await process_entries(page_index, entries)
