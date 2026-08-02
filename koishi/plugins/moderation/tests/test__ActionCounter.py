import vampytest

from ..top_list_action_counter import TopListActionCounter, top_list_action_counter_increment_with
from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE


def test__TopListActionCounter__new():
    """
    Tests whether ``TopListActionCounter.__new__`` works as intended.
    """
    top_list_action_counter = TopListActionCounter()
    
    vampytest.assert_instance(top_list_action_counter, TopListActionCounter)
    
    vampytest.assert_instance(top_list_action_counter.all, int)
    vampytest.assert_instance(top_list_action_counter.ban, int)
    vampytest.assert_instance(top_list_action_counter.kick, int)
    vampytest.assert_instance(top_list_action_counter.mute, int)
    
    vampytest.assert_eq(top_list_action_counter.all, 0)
    vampytest.assert_eq(top_list_action_counter.ban, 0)
    vampytest.assert_eq(top_list_action_counter.kick, 0)
    vampytest.assert_eq(top_list_action_counter.mute, 0)


def test__TopListActionCounter__repr():
    """
    tests whether ``TopListActionCounter.__repr__`` works as intended.
    """
    top_list_action_counter = TopListActionCounter()
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_BAN, 1)
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_KICK, 2)
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_MUTE, 3)
    
    output = repr(top_list_action_counter)
    vampytest.assert_instance(output, str)
    
    vampytest.assert_in(type(top_list_action_counter).__name__, output)
    
    vampytest.assert_in('all = 6', output)
    vampytest.assert_in('ban = 1', output)
    vampytest.assert_in('kick = 2', output)
    vampytest.assert_in('mute = 3', output)
