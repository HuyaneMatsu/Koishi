__all__ = ()

from scarletio import copy_docs
from sqlalchemy.sql import desc, select

from ...bot_utils.models import DB_ENGINE, user_common_model

from .constants import PAGE_SIZE


async def get_top_list_entries(page_index):
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
    @copy_docs(get_top_list_entries)
    async def get_top_list_entries(page_index):
        return []
