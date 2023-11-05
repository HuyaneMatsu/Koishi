import vampytest

from ..constants import REPLY_CACHE, REPLY_CACHE_MAX_SIZE
from ..spam_protection import is_reply_in_cache


def test__is_reply_in_cache__nope():
    """
    Tests whether ``is_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    mocked = vampytest.mock_globals(
        is_reply_in_cache,
        REPLY_CACHE = type(REPLY_CACHE)(),
        REPLY_CACHE_MAX_SIZE = REPLY_CACHE_MAX_SIZE,
    )
    
    guild_id = 202311050020
    welcome_message_id = 202311050021
    welcomer_id = 202311050022
    
    output = mocked(guild_id, welcome_message_id, welcomer_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__is_reply_in_cache__yes():
    """
    Tests whether ``is_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    mocked = vampytest.mock_globals(
        is_reply_in_cache,
        REPLY_CACHE = type(REPLY_CACHE)(),
        REPLY_CACHE_MAX_SIZE = REPLY_CACHE_MAX_SIZE,
    )
    
    guild_id = 202311050023
    welcome_message_id = 202311050024
    welcomer_id = 202311050025
    
    mocked(guild_id, welcome_message_id, welcomer_id)
    
    output = mocked(guild_id, welcome_message_id, welcomer_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)


def test__is_reply_in_cache__cache_max_size():
    """
    Tests whether ``is_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    reply_cache = type(REPLY_CACHE)()
    
    mocked = vampytest.mock_globals(
        is_reply_in_cache,
        REPLY_CACHE = reply_cache,
        REPLY_CACHE_MAX_SIZE = 1,
    )
    
    guild_id = 202311050025
    welcome_message_id = 202311050026
    welcomer_id = 202311050027
    
    mocked(guild_id, welcome_message_id, welcomer_id)
    
    guild_id = 202311050028
    welcome_message_id = 202311050029
    welcomer_id = 202311050030
    
    mocked(guild_id, welcome_message_id, welcomer_id)
    
    vampytest.assert_eq(len(reply_cache), 1)
