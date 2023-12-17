import vampytest

from ..constants import REPLY_CACHE, REPLY_CACHE_MAX_SIZE
from ..spam_protection import is_reply_in_cache


def test__is_reply_in_cache__nope():
    """
    Tests whether ``is_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    reply_cache = type(REPLY_CACHE)()
    
    mocked = vampytest.mock_globals(
        is_reply_in_cache,
        REPLY_CACHE = reply_cache,
        REPLY_CACHE_MAX_SIZE = REPLY_CACHE_MAX_SIZE,
    )
    
    guild_id = 202312140020
    welcome_message_id = 202312140021
    welcomer_id = 202312140022
    
    output = mocked(guild_id, welcome_message_id, welcomer_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)
    vampytest.assert_eq(len(reply_cache), 0)


def test__is_reply_in_cache__yes():
    """
    Tests whether ``is_reply_in_cache`` works as intended.
    
    Case: Not in cache.
    """
    reply_cache = type(REPLY_CACHE)()
    
    mocked = vampytest.mock_globals(
        is_reply_in_cache,
        REPLY_CACHE = reply_cache,
        REPLY_CACHE_MAX_SIZE = REPLY_CACHE_MAX_SIZE,
    )
    
    guild_id = 202312140023
    welcome_message_id = 202312140024
    welcomer_id = 202312140025
    
    reply_cache[guild_id, welcome_message_id, welcomer_id] = None
    
    output = mocked(guild_id, welcome_message_id, welcomer_id)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
    vampytest.assert_eq(len(reply_cache), 1)
