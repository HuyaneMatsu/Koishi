import vampytest
from hata import Client, DiscordException
from scarletio import CauseGroup

from ..reminding import call_exception_handler


async def test__call_exception_handler__single():
    """
    Tests whether ``call_exception_handler`` works as intended.
    
    This function is a coroutine.
    
    Case: Single exception.
    """
    client_id = 202303010000
    exception_0 = DiscordException(None, None, None, None)
    collected_exceptions = [exception_0]
    error_event_handler_called = True
    
    async def error_event_handler(input_client, location, input_exception):
        nonlocal client
        nonlocal exception_0
        nonlocal error_event_handler_called
        
        vampytest.assert_is(input_client, client)
        vampytest.assert_instance(location, str)
        vampytest.assert_is(input_exception, exception_0)
        vampytest.assert_eq(input_exception.__cause__, None)
        
        error_event_handler_called = True
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.events.error = error_event_handler
    
    mocked = vampytest.mock_globals(
        call_exception_handler,
        MAIN_CLIENT = client,
    )
    
    try:
        await mocked(collected_exceptions)
        
        vampytest.assert_true(error_event_handler_called)
    finally:
        client._delete()
        client = None
    

async def test__call_exception_handler__multiple():
    """
    Tests whether ``call_exception_handler`` works as intended.
    
    This function is a coroutine.
    
    Case: Single exception.
    """
    client_id = 202303010001
    exception_0 = DiscordException(None, None, None, None)
    exception_1 = DiscordException(None, None, None, None)
    exception_2 = DiscordException(None, None, None, None)
    collected_exceptions = [exception_0, exception_1, exception_2]
    error_event_handler_called = True
    
    async def error_event_handler(input_client, location, input_exception):
        nonlocal client
        nonlocal exception_0
        nonlocal error_event_handler_called
        
        vampytest.assert_is(input_client, client)
        vampytest.assert_instance(location, str)
        vampytest.assert_is(input_exception, exception_2)
        vampytest.assert_eq(input_exception.__cause__, CauseGroup(exception_0, exception_1))
        
        error_event_handler_called = True
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.events.error = error_event_handler
    
    mocked = vampytest.mock_globals(
        call_exception_handler,
        MAIN_CLIENT = client,
    )
    
    try:
        await mocked(collected_exceptions)
        
        vampytest.assert_true(error_event_handler_called)
    finally:
        client._delete()
        client = None
