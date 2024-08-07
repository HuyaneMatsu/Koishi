__all__ = ()

from itertools import count
from math import floor

from scarletio import RichAttributeErrorBaseType, copy_docs
from sqlalchemy.sql import select

from ...bot_utils.models import DB_ENGINE, user_common_model, USER_COMMON_TABLE


async def query_user_entry_id_and_available_love_with_connector(user_id, connector):
    """
    Queries how the user's entry's identifier and its available love.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier.
    connector : ``AsyncConnection``
        Database connector.
    
    Returns
    -------
    entry_id : `int`
    available_love : `int`
    """
    response = await connector.execute(
        select(
            [
                user_common_model.id,
                user_common_model.total_love,
                user_common_model.total_allocated,
            ]
        ).where(
            user_common_model.user_id == user_id,
        )
    )
    result = await response.fetchone()

    if result is None:
        available_love = 0
        entry_id = -1
    
    else:
        entry_id, total_love, total_allocated = result
        available_love = total_love - total_allocated
    
    return entry_id, available_love


if DB_ENGINE is None:
    COUNTER = iter(count(1 << 60))
    
    @copy_docs(query_user_entry_id_and_available_love_with_connector)
    async def query_user_entry_id_and_available_love_with_connector(user_id, connector):
        return next(COUNTER), 1000


async def allocate_love_with_connector_with_connector(entry_id, amount, connector):
    """
    Allocates an amount of love.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        The owner entry's identifier.
    amount : `int`
        The amount to allocate.
    connector : ``AsyncConnection``
        Database connector.
    """
    if entry_id == -1:
        return
    
    await connector.execute(
        USER_COMMON_TABLE.update(
            user_common_model.id == entry_id,
        ).values(
            total_allocated = user_common_model.total_allocated + amount,
        )
    )


if DB_ENGINE is None:
    @copy_docs(allocate_love_with_connector_with_connector)
    async def allocate_love_with_connector_with_connector(entry_id, amount, connector):
        return None


async def modify_user_hearts(entry_id, amount, multiplier, unallocate):
    """
    Modifies the amount of hearts a user has.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        The owner entry's identifier.
    amount : `int`
        The amount to allocate.
    multiplier : `int`
        Whether to increase the user's or decrease. Can be `0` if it should not be modified.
    unallocate : `bool`
        Whether the user's hearts should be unallocated.
    """
    if entry_id == -1:
        return
    
    async with DB_ENGINE.connect() as connector:
        await modify_user_hearts_with_connector(entry_id, amount, multiplier, unallocate, connector)


if DB_ENGINE is None:
    @copy_docs(modify_user_hearts)
    async def modify_user_hearts(entry_id, amount, increase, unallocate):
        return None


async def batch_modify_user_hearts(items):
    """
    Modifies multiple user's hearts.
    
    This function is a coroutine.
    
    Parameters
    ----------
    items : `list<(int, int, int, bool)>`
        The `entry_id`, `amount`, `increase`, `unallocate` as a tuple.
    """
    if not items:
        return
    
    async with DB_ENGINE.connect() as connector:
        for entry_id, amount, multiplier, unallocate in items:
            await modify_user_hearts_with_connector(entry_id, amount, multiplier, unallocate, connector)


if DB_ENGINE is None:
    @copy_docs(batch_modify_user_hearts)
    async def batch_modify_user_hearts(items):
        return None


async def modify_user_hearts_with_connector(entry_id, amount, multiplier, unallocate, connector):
    """
    Modifies the amount of hearts a user has.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry_id : `int`
        The owner entry's identifier.
    amount : `int`
        The amount to allocate.
    multiplier : `float`
        Whether to increase the user's or decrease. Can be `0` if it should not be modified.
    unallocate : `bool`
        Whether the user's hearts should be unallocated.
    connector : ``AsyncConnection``
        Database connector.
    """
    expression = USER_COMMON_TABLE.update(
        user_common_model.id == entry_id,
    )
    
    if multiplier:
        expression = expression.values(
            total_love = user_common_model.total_love + floor(amount * multiplier),
        )
    
    if unallocate:
        expression = expression.values(
            total_allocated = user_common_model.total_allocated - amount,
        )
    
    await connector.execute(expression)


if DB_ENGINE is None:
    @copy_docs(modify_user_hearts_with_connector)
    async def modify_user_hearts_with_connector(entry_id, amount, increase, unallocate, connector):
        return None


if DB_ENGINE is None:
    class DB_ENGINE_TYPE(RichAttributeErrorBaseType):
        __slots__ = ()
        
        def connect(self):
            return self
        
        async def __aenter__(self):
            return self
        
        async def __aexit__(self, exception_type, exception_value, exception_traceback):
            pass
    
    DB_ENGINE = DB_ENGINE_TYPE()
