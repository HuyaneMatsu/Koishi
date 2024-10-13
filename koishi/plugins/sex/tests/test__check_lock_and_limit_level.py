import vampytest
from hata import Channel, InteractionEvent, User

from ..constants import SEX_SPAM_LOCKS
from ..spam_lock import check_lock_and_limit_level


def _clear_locks():
    while SEX_SPAM_LOCKS:
        item = SEX_SPAM_LOCKS.popitem()
        item[1].cancel()


async def test__check_lock_and_limit_level__first_trigger():
    """
    tests whether ``check_lock_and_limit_level`` works as intended.
    
    This function is a coroutine.
    
    Case: first trigger.
    """
    user_id = 202410130010
    channel_id = 202410130011
    
    event = InteractionEvent(
        channel = Channel.precreate(channel_id),
        user = User.precreate(user_id),
    )
    level = 7
    
    try:
        output = check_lock_and_limit_level(event, level)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, level)
        
        vampytest.assert_eq(SEX_SPAM_LOCKS.keys(), {channel_id, user_id})
        vampytest.assert_false(all(spam_lock.last_set for spam_lock in SEX_SPAM_LOCKS.values()))
    
    finally:
        _clear_locks()


async def test__check_lock_and_limit_level__repeated_trigger():
    """
    tests whether ``check_lock_and_limit_level`` works as intended.
    
    This function is a coroutine.
    
    Case: repeated trigger.
    """
    user_id = 202410130011
    channel_id = 202410130012
    
    event = InteractionEvent(
        channel = Channel.precreate(channel_id),
        user = User.precreate(user_id),
    )
    level_0 = 6
    level_1 = 7
    
    try:
        check_lock_and_limit_level(event, level_0)
        output = check_lock_and_limit_level(event, level_1)
        
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, 0)
        
        vampytest.assert_eq(SEX_SPAM_LOCKS.keys(), {channel_id, user_id})
        vampytest.assert_true(all(spam_lock.last_set for spam_lock in SEX_SPAM_LOCKS.values()))
    
    finally:
        _clear_locks()
