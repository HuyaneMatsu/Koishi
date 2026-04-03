from time import monotonic

import vampytest
from scarletio import TimerHandle

from ..constants import SEX_RESET_AFTER
from ..spam_lock import SexSpamLock


def _assert_fields_set(spam_lock):
    """
    Asserts whether every fields are set of the spam lock.
    
    Parameters
    ----------
    spam_lock : ``SexSpamLock``
        The spam lock to test.
    """
    vampytest.assert_instance(spam_lock, SexSpamLock)
    vampytest.assert_instance(spam_lock.entity_id, int)
    vampytest.assert_instance(spam_lock.handle, TimerHandle, nullable = True)
    vampytest.assert_instance(spam_lock.last_set, float)
    vampytest.assert_instance(spam_lock.max_level, int)


async def test__SexSpamLock__new():
    """
    Tests whether ``SexSpamLock.__new__`` works as intended.
    
    This function is a coroutine.
    """
    entity_id = 202410130000
    max_level = 7
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        _assert_fields_set(spam_lock)
    
        vampytest.assert_eq(spam_lock.entity_id, entity_id)
        vampytest.assert_eq(spam_lock.max_level, max_level)
        vampytest.assert_is_not(spam_lock.handle, None)
        vampytest.assert_not(spam_lock.last_set)
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__repr():
    """
    Tests whether ``SexSpamLock.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    entity_id = 202410130001
    max_level = 7
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        output = repr(spam_lock)
        vampytest.assert_instance(output, str)
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__set_max_level__over():
    """
    Tests whether ``SexSpamLock.set_max_level`` works as intended.
    
    This function is a coroutine.
    
    Case: over.
    """
    entity_id = 202410130002
    max_level = 7
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        output = spam_lock.set_max_level(8)
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, 0)
        
        vampytest.assert_true(spam_lock.last_set)
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__set_max_level__under():
    """
    Tests whether ``SexSpamLock.set_max_level`` works as intended.
    
    This function is a coroutine.
    
    Case: under.
    """
    entity_id = 202410130003
    max_level = 7
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        output = spam_lock.set_max_level(6)
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, 6)
        
        vampytest.assert_true(spam_lock.last_set)
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__set_max_level__equal():
    """
    Tests whether ``SexSpamLock.set_max_level`` works as intended.
    
    This function is a coroutine.
    
    Case: equal.
    """
    entity_id = 202410130004
    max_level = 7
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        output = spam_lock.set_max_level(max_level)
        vampytest.assert_instance(output, int)
        vampytest.assert_eq(output, max_level)
        
        vampytest.assert_true(spam_lock.last_set)
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__expires_at__last_set_set():
    """
    Tests whether ``SexSpamLock.expires_at`` works as intended.
    
    This function is a coroutine.
    
    Case: `last_set` set.
    """
    entity_id = 202410130005
    max_level = 7
    last_set = 5.5
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        spam_lock.last_set = last_set
        
        output = spam_lock.expires_at
        vampytest.assert_instance(output, float)
        vampytest.assert_eq(output, last_set + SEX_RESET_AFTER)
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__expires_at__last_set_unset():
    """
    Tests whether ``SexSpamLock.expires_at`` works as intended.
    
    This function is a coroutine.
    
    Case: `last_set` unset.
    """
    entity_id = 202410130006
    max_level = 7
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        output = spam_lock.expires_at
        vampytest.assert_instance(output, float)
        vampytest.assert_true(output > monotonic())
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__cancel():
    """
    Tests whether ``SexSpamLock.cancel`` works as intended.
    
    This function is a coroutine.
    """
    entity_id = 202410130007
    max_level = 7
    last_set = 5.5
    
    spam_lock = SexSpamLock(entity_id, max_level)
    try:
        spam_lock.last_set = last_set
        
        spam_lock.cancel()
        
        vampytest.assert_false(spam_lock.last_set)
        vampytest.assert_is(spam_lock.handle, None)
    
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__call__last_set_unset():
    """
    Tests whether ``SexSpamLock.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: `last_set` unset.
    """
    entity_id = 202410130008
    max_level = 7
    
    spam_lock = SexSpamLock(entity_id, max_level)
    spam_lock.cancel()
    
    try:
        spam_lock()
        
        vampytest.assert_false(spam_lock.last_set)
        vampytest.assert_is(spam_lock.handle, None)
        
    finally:
        spam_lock.cancel()


async def test__SexSpamLock__call__last_set_set():
    """
    Tests whether ``SexSpamLock.__call__`` works as intended.
    
    This function is a coroutine.
    
    Case: `last_set` set.
    """
    entity_id = 202410130009
    max_level = 7
    last_set = monotonic()
    
    spam_lock = SexSpamLock(entity_id, max_level)
    spam_lock.cancel()
    
    try:
        spam_lock.last_set = last_set
        spam_lock()
        
        vampytest.assert_false(spam_lock.last_set)
        vampytest.assert_is_not(spam_lock.handle, None)
        
    finally:
        spam_lock.cancel()
