import vampytest

from ..constants import BLACKLIST
from ..queries import is_user_id_in_blacklist


def test__is_user_id_in_blacklist__false():
    """
    Tests whether ``is_user_id_in_blacklist`` works as intended.
    
    Case: false.
    """
    user_id = 202310170005
    
    try:
        
        output = is_user_id_in_blacklist(user_id)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        BLACKLIST.clear()


def test__is_user_id_in_blacklist__true():
    """
    Tests whether ``is_user_id_in_blacklist`` works as intended.
    
    Case: false.
    """
    user_id = 202310170006
    
    try:
        BLACKLIST[user_id] = 1
        
        output = is_user_id_in_blacklist(user_id)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        BLACKLIST.clear()
