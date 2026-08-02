import vampytest

from ..top_list_action_counter import TopListActionCounter, top_list_action_counter_increment_with
from ..constants import ACTION_TYPE_BAN, ACTION_TYPE_KICK, ACTION_TYPE_MUTE



def test__top_list_action_counter_increment_with__ban():
    """
    Tests whether ``top_list_action_counter_increment_with`` works as intended.
    
    Case: ban.
    """
    top_list_action_counter = TopListActionCounter()
    
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_BAN)
    
    vampytest.assert_eq(top_list_action_counter.all, 1)
    vampytest.assert_eq(top_list_action_counter.ban, 1)
    
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_BAN)
    
    vampytest.assert_eq(top_list_action_counter.all, 2)
    vampytest.assert_eq(top_list_action_counter.ban, 2)


def test__top_list_action_counter_increment_with__kick():
    """
    Tests whether ``top_list_action_counter_increment_with`` works as intended.
    
    Case: kick.
    """
    top_list_action_counter = TopListActionCounter()
    
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_KICK)
    
    vampytest.assert_eq(top_list_action_counter.all, 1)
    vampytest.assert_eq(top_list_action_counter.kick, 1)
    
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_KICK)
    
    vampytest.assert_eq(top_list_action_counter.all, 2)
    vampytest.assert_eq(top_list_action_counter.kick, 2)


def test__top_list_action_counter_increment_with__mute():
    """
    Tests whether ``top_list_action_counter_increment_with`` works as intended.
    
    Case: mute.
    """
    top_list_action_counter = TopListActionCounter()
    
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_MUTE)
    
    vampytest.assert_eq(top_list_action_counter.all, 1)
    vampytest.assert_eq(top_list_action_counter.mute, 1)
    
    top_list_action_counter_increment_with(top_list_action_counter, ACTION_TYPE_MUTE)
    
    vampytest.assert_eq(top_list_action_counter.all, 2)
    vampytest.assert_eq(top_list_action_counter.mute, 2)

