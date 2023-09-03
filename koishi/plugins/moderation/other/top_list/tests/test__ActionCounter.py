import vampytest

from ..action_counter import ActionCounter
from ..constants import TYPE_BAN, TYPE_KICK, TYPE_MUTE


def test__ActionCounter__new():
    """
    Tests whether ``ActionCounter.__new__`` works as intended.
    """
    action_counter = ActionCounter()
    
    vampytest.assert_instance(action_counter, ActionCounter)
    
    vampytest.assert_instance(action_counter.all, int)
    vampytest.assert_instance(action_counter.ban, int)
    vampytest.assert_instance(action_counter.kick, int)
    vampytest.assert_instance(action_counter.mute, int)
    
    vampytest.assert_eq(action_counter.all, 0)
    vampytest.assert_eq(action_counter.ban, 0)
    vampytest.assert_eq(action_counter.kick, 0)
    vampytest.assert_eq(action_counter.mute, 0)


def test__ActionCounter__increment_with__ban():
    """
    Tests whether ``ActionCounter.increment_with`` works as intended.
    
    Case: ban.
    """
    action_counter = ActionCounter()
    
    action_counter.increment_with(TYPE_BAN)
    
    vampytest.assert_eq(action_counter.all, 1)
    vampytest.assert_eq(action_counter.ban, 1)
    
    action_counter.increment_with(TYPE_BAN)
    
    vampytest.assert_eq(action_counter.all, 2)
    vampytest.assert_eq(action_counter.ban, 2)


def test__ActionCounter__increment_with__kick():
    """
    Tests whether ``ActionCounter.increment_with`` works as intended.
    
    Case: kick.
    """
    action_counter = ActionCounter()
    
    action_counter.increment_with(TYPE_KICK)
    
    vampytest.assert_eq(action_counter.all, 1)
    vampytest.assert_eq(action_counter.kick, 1)
    
    action_counter.increment_with(TYPE_KICK)
    
    vampytest.assert_eq(action_counter.all, 2)
    vampytest.assert_eq(action_counter.kick, 2)


def test__ActionCounter__increment_with__mute():
    """
    Tests whether ``ActionCounter.increment_with`` works as intended.
    
    Case: mute.
    """
    action_counter = ActionCounter()
    
    action_counter.increment_with(TYPE_MUTE)
    
    vampytest.assert_eq(action_counter.all, 1)
    vampytest.assert_eq(action_counter.mute, 1)
    
    action_counter.increment_with(TYPE_MUTE)
    
    vampytest.assert_eq(action_counter.all, 2)
    vampytest.assert_eq(action_counter.mute, 2)


def test__ActionCounter__repr():
    """
    tests whether ``ActionCounter.__repr__`` works as intended.
    """
    action_counter = ActionCounter()
    action_counter.increment_with(TYPE_BAN, 1)
    action_counter.increment_with(TYPE_KICK, 2)
    action_counter.increment_with(TYPE_MUTE, 3)
    
    output = repr(action_counter)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(action_counter.__class__.__name__, output)
    
    vampytest.assert_in('all = 6', output)
    vampytest.assert_in('ban = 1', output)
    vampytest.assert_in('kick = 2', output)
    vampytest.assert_in('mute = 3', output)
