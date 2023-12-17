import vampytest

from ..constants import REPLY_CACHE, REPLY_CACHE_MAX_SIZE
from ..spam_protection import put_reply_in_cache


def test__put_reply_in_cache__nope():
    """
    Tests whether ``put_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    reply_cache = type(REPLY_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_reply_in_cache,
        REPLY_CACHE = reply_cache,
        REPLY_CACHE_MAX_SIZE = REPLY_CACHE_MAX_SIZE,
    )
    
    guild_id = 202311050020
    welcome_message_id = 202311050021
    welcomer_id = 202311050022
    
    output = mocked(guild_id, welcome_message_id, welcomer_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    vampytest.assert_eq(len(reply_cache), 1)


def test__put_reply_in_cache__yes():
    """
    Tests whether ``put_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    reply_cache = type(REPLY_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_reply_in_cache,
        REPLY_CACHE = reply_cache,
        REPLY_CACHE_MAX_SIZE = REPLY_CACHE_MAX_SIZE,
    )
    
    guild_id = 202311050023
    welcome_message_id = 202311050024
    welcomer_id = 202311050025
    
    reply_cache[guild_id, welcome_message_id, welcomer_id] = None
    
    output = mocked(guild_id, welcome_message_id, welcomer_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(len(reply_cache), 1)


def test__put_reply_in_cache__cache_max_size():
    """
    Tests whether ``put_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    reply_cache = type(REPLY_CACHE)()
    
    mocked = vampytest.mock_globals(
        put_reply_in_cache,
        REPLY_CACHE = reply_cache,
        REPLY_CACHE_MAX_SIZE = 1,
    )
    
    guild_id = 202311050025
    welcome_message_id = 202311050026
    welcomer_id = 202311050027
    
    reply_cache[guild_id, welcome_message_id, welcomer_id] = None
    
    guild_id = 202311050028
    welcome_message_id = 202311050029
    welcomer_id = 202311050030
    
    mocked(guild_id, welcome_message_id, welcomer_id)
    
    vampytest.assert_eq(len(reply_cache), 1)
