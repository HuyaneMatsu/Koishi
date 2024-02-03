import vampytest

from hata import Message

from ..cache import CACHE, delete_lock_of, get_lock_for


def test__delete_lock_of():
    """
    Tests whether ``delete_lock_of`` works as intended.
    """
    message = Message.precreate(202401160002)
    
    try:
        output_0 = get_lock_for(message)
        delete_lock_of(message)
        output_1 = get_lock_for(message)
        
        vampytest.assert_is_not(output_0, output_1)
    finally:
        CACHE.clear()
