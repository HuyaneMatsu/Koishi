import vampytest

from ..handling import HANDLERS, remove_handler


def test__remove_handler():
    """
    Tests whether ``remove_handler`` works as intended.
    """
    async def handler():
        pass
    
    event_type = 5
    
    
    try:
        HANDLERS[event_type] = handler
        
        remove_handler(event_type, handler)
        
        vampytest.assert_eq(
            HANDLERS,
            {},
        )
    
    finally:
        HANDLERS.clear()


def test__remove_handler__handler_mismatch():
    """
    Tests whether ``remove_handler`` works as intended.
    
    Case: handler mismatch.
    """
    async def handler_0():
        pass
    
    async def handler_1():
        pass
    
    event_type = 5
    
    
    try:
        HANDLERS[event_type] = handler_0
        
        remove_handler(event_type, handler_1)
        
        vampytest.assert_eq(
            HANDLERS,
            {
                event_type: handler_0,
            },
        )
    
    finally:
        HANDLERS.clear()
