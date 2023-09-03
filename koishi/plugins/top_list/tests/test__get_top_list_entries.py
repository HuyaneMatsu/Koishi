import vampytest

from hata import User

from ..constants import PAGE_SIZE
from ..queries import get_top_list_entries


async def test__get_top_list_entries():
    """
    Tests whether ``get_top_list_entries`` works as intended.
    
    This function is a coroutine.
    """
    page_index = 19
    
    user_0 = User.precreate(202308230016, name = 'okuu')
    user_1 = User.precreate(202308230017, name = 'orin')
    
    async def request_top_list_entries(page_index_parameter):
        nonlocal page_index
        vampytest.assert_eq(page_index, page_index_parameter)
        
        return [
            (user_0.id, 1111),
            (user_1.id, 1112),
        ]
    
    
    async def get_user(user_id):
        vampytest.assert_in(user_id, (user_0.id, user_1.id))
        
        return User.precreate(user_id)
    
    
    mocked = vampytest.mock_globals(
        get_top_list_entries,
        request_top_list_entries = request_top_list_entries,
        get_user = get_user,
    )
    
    output = await mocked(page_index)
    
    vampytest.assert_eq(
        output,
        [
            (page_index * PAGE_SIZE + 1, 1111, user_0),
            (page_index * PAGE_SIZE + 2, 1112, user_1),
        ],
    )
