import vampytest

from ..constants import WELCOME_CACHE, WELCOME_CACHE_MAX_SIZE
from ..welcome_spam_protection import is_welcome_in_cache


def test__is_welcome_in_cache__nope():
    """
    Tests whether ``is_welcome_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    welcome_cache = type(WELCOME_CACHE)()
    
    mocked = vampytest.mock_globals(
        is_welcome_in_cache,
        WELCOME_CACHE = welcome_cache,
        WELCOME_CACHE_MAX_SIZE = WELCOME_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220010
    welcomed_id = 202502220011
    
    output = mocked(guild_id, welcomed_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    vampytest.assert_eq(len(welcome_cache), 0)


def test__is_welcome_in_cache__yes():
    """
    Tests whether ``is_welcome_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    welcome_cache = type(WELCOME_CACHE)()
    
    mocked = vampytest.mock_globals(
        is_welcome_in_cache,
        WELCOME_CACHE = welcome_cache,
        WELCOME_CACHE_MAX_SIZE = WELCOME_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220012
    welcomed_id = 202502220013
    
    welcome_cache[guild_id, welcomed_id] = None
    
    output = mocked(guild_id, welcomed_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(len(welcome_cache), 1)
