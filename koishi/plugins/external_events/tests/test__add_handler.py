import vampytest

from ..handling import HANDLERS, add_handler


def test__add_handler():
    """
    Tests whether ``add_handler`` works as intended.
    """
    async def handler():
        pass
    
    event_type = 5
    
    
    try:
        add_handler(event_type, handler)
        
        vampytest.assert_eq(
            HANDLERS,
            {
                event_type: handler,
            },
        )
    
    finally:
        HANDLERS.clear()


def test__add_handler__duplicate_registration():
    """
    Tests whether ``add_handler`` works as intended.
    
    Case: duplicate registration.
    """
    async def handler_0():
        pass
    
    async def handler_1():
        pass
    
    event_type = 5
    
    
    try:
        add_handler(event_type, handler_0)
        add_handler(event_type, handler_1)
        
        vampytest.assert_eq(
            HANDLERS,
            {
                event_type: handler_1,
            },
        )
    
    finally:
        HANDLERS.clear()
