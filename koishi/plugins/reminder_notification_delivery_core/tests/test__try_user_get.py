import vampytest
from hata import DiscordException, ERROR_CODES, User

from ..requests import try_user_get


async def test__try_user_get__success():
    """
    Tests whether ``try_user_get`` works as intended.
    
    Case: Success.
    
    This function is a coroutine.
    """
    user_id = 202402280001
    
    user = User.precreate(user_id)
    
    async def get_user(input_user_id):
        nonlocal user
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return user
    
    
    mocked = vampytest.mock_globals(
        try_user_get,
        get_user = get_user,
    )
    
    output = await mocked(user_id)
    vampytest.assert_eq(output, (user, False))


async def test__try_user_get__deleted():
    """
    Tests whether ``try_user_get`` works as intended.
    
    Case: User deleted.
    
    This function is a coroutine.
    """
    user_id = 202402280002
    
    exception = DiscordException(None, None, None, None)
    exception.status = 400
    exception.code = ERROR_CODES.unknown_user
    
    async def get_user(input_user_id):
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        nonlocal exception
        raise exception
    
    
    mocked = vampytest.mock_globals(
        try_user_get,
        get_user = get_user,
    )
    
    output = await mocked(user_id)

    vampytest.assert_eq(output, (None, True))
