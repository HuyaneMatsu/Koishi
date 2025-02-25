import vampytest

from ..constants import WELCOME_CACHE, WELCOME_CACHE_MAX_SIZE
from ..welcome_spam_protection import put_welcome_in_cache


def test__put_welcome_in_cache__nope():
    """
    Tests whether ``put_welcome_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    welcome_cache = type(WELCOME_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_welcome_in_cache,
        WELCOME_CACHE = welcome_cache,
        WELCOME_CACHE_MAX_SIZE = WELCOME_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220020
    welcomed_id = 202502220021
    
    output = mocked(guild_id, welcomed_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    vampytest.assert_eq(len(welcome_cache), 1)


def test__put_welcome_in_cache__yes():
    """
    Tests whether ``put_welcome_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    welcome_cache = type(WELCOME_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_welcome_in_cache,
        WELCOME_CACHE = welcome_cache,
        WELCOME_CACHE_MAX_SIZE = WELCOME_CACHE_MAX_SIZE,
    )
    
    guild_id = 202502220023
    welcomed_id = 202502220024
    
    welcome_cache[guild_id, welcomed_id] = None
    
    output = mocked(guild_id, welcomed_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(len(welcome_cache), 1)


def test__put_welcome_in_cache__cache_max_size():
    """
    Tests whether ``put_welcome_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    welcome_cache = type(WELCOME_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_welcome_in_cache,
        WELCOME_CACHE = welcome_cache,
        WELCOME_CACHE_MAX_SIZE = 1,
    )
    
    guild_id = 202502220025
    welcomed_id = 202502220026
    
    welcome_cache[guild_id, welcomed_id] = None
    
    guild_id = 202502220027
    welcomed_id = 202502220028
    
    mocked(guild_id, welcomed_id)
    
    vampytest.assert_eq(len(welcome_cache), 1)
