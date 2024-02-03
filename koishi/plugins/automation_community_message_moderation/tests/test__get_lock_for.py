import vampytest

from hata import Message
from scarletio import Lock

from ..cache import CACHE, get_lock_for


def test__get_lock_for__output():
    """
    Tests whether ``get_lock_for`` works as intended.
    
    Case: output type check.
    """
    message = Message.precreate(202401160000)
    
    try:
        output = get_lock_for(message)
        
        vampytest.assert_instance(output, Lock)
    finally:
        CACHE.clear()


def test__get_lock_for__repeated_access():
    """
    Tests whether ``get_lock_for`` works as intended.
    
    Case: test repeated access.
    """
    message = Message.precreate(202401160001)
    
    try:
        output_0 = get_lock_for(message)
        output_1 = get_lock_for(message)
        
        vampytest.assert_is(output_0, output_1)
    finally:
        CACHE.clear()
