import vampytest
from hata import DiscordException, ERROR_CODES, User, ZEROUSER

from ..queries import process_entries
from ..constants import PAGE_SIZE


async def test__process_entries():
    """
    Tests whether ``process_entries`` works as intended.
    
    This function is a coroutine.
    """
    async def get_user(user_id):
        return User.precreate(user_id)
    
    mocked = vampytest.mock_globals(process_entries, get_user = get_user)
    
    
    input = [
        (202308230000, 1111),
        (202308230001, 1112),
    ]
    
    page_index = 10
    
    output = await mocked(page_index, input)
    
    vampytest.assert_eq(
        output,
        [
            (page_index * PAGE_SIZE + 1, 1111, User.precreate(202308230000)),
            (page_index * PAGE_SIZE + 2, 1112, User.precreate(202308230001)),
        ],
    )


async def test__process_entries__user_deleted():
    """
    Tests whether ``process_entries`` works as intended.
    
    This function is a coroutine.
    
    Case: User deleted.
    """
    async def get_user(user_id):
        if user_id == 202308230002:
            exception = DiscordException(None, None, None, None)
            exception._code = ERROR_CODES.unknown_user
            raise exception
        
        return User.precreate(user_id)
    
    mocked = vampytest.mock_globals(process_entries, get_user = get_user)
    
    
    input = [
        (202308230002, 1111),
        (202308230003, 1112),
    ]
    
    page_index = 10
    
    output = await mocked(page_index, input)
    
    vampytest.assert_eq(
        output,
        [
            (page_index * PAGE_SIZE + 1, 1111, ZEROUSER),
            (page_index * PAGE_SIZE + 2, 1112, User.precreate(202308230003)),
        ],
    )
