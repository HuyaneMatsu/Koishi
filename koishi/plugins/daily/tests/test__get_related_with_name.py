import vampytest

from hata import ClientUserBase, User

from ..related_completion import get_related_with_name


async def test__get_related_with_name():
    """
    Tests whether ``get_related_with_name`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202411120020
    guild_id = 0
    name = 'remilia'
    related_id_0 = 202411120021
    related_id_1 = 202411120022
    related_name_0 = 'koishi'
    related_name_1 = 'remilia'
    
    async def mock_get_related_ids(input_user_id):
        nonlocal user_id
        nonlocal related_id_0
        nonlocal related_id_1
        
        vampytest.assert_eq(user_id, input_user_id)
        return {related_id_0, related_id_1}
    
    
    async def mock_get_users_unordered(input_user_ids):
        nonlocal related_id_0
        nonlocal related_id_1
        nonlocal related_name_0
        nonlocal related_name_1
        
        vampytest.assert_eq(
            input_user_ids,
            {related_id_0, related_id_1},
        )
        
        user_0 = User.precreate(related_id_0, name = related_name_0)
        user_1 = User.precreate(related_id_1, name = related_name_1)
        
        return [user_0, user_1]
    
    mocked = vampytest.mock_globals(
        get_related_with_name,
        get_related_ids = mock_get_related_ids,
        get_users_unordered = mock_get_users_unordered,
    )
    
    output = await mocked(user_id, guild_id, name)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    vampytest.assert_is_not(output, None)
    vampytest.assert_eq(output.id, related_id_1)
