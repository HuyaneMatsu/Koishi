import vampytest
from hata import Client
from scarletio import skip_ready_cycle

from ..external_event import ExternalEvent
from ..looping import loop_step


async def test__loop_step():
    """
    Tests whether ``loop_step`` works as intended.
    
    This function is a coroutine.
    """
    pull_step = 0
    remove_step = 0
    handler_0_called = 0
    handler_1_called = 0
    raised_exception = ValueError('poppo')
    
    external_event_0 = ExternalEvent(
        event_type = 10000,
        user_id = 202411270000,
    )
    external_event_0.entry_id = 1
    
    external_event_1 = ExternalEvent(
        event_type = 10001,
        user_id = 202411270001,
    )
    external_event_1.entry_id = 2
    
    
    async def pull_external_events_mock():
        nonlocal pull_step
        nonlocal external_event_0
        nonlocal external_event_1
        
        if pull_step == 0:
            result = [external_event_0, external_event_1]
        
        else:
            raise RuntimeError
        
        pull_step += 1
        return result
    
    
    async def remove_external_events_mock(entry_ids):
        nonlocal remove_step
        nonlocal external_event_0
        nonlocal external_event_1
        
        if remove_step == 0:
            expected_entry_ids = [external_event_0.entry_id, external_event_1.entry_id]
        
        else:
            raise RuntimeError
        
        remove_step += 1
        vampytest.assert_eq(entry_ids, expected_entry_ids)
    
    
    async def handler_0(external_event):
        nonlocal handler_0_called
        nonlocal external_event_0
        
        handler_0_called += 1
        vampytest.assert_eq(external_event, external_event_0)
    
    
    async def handler_1(external_event):
        nonlocal handler_1_called
        nonlocal external_event_1
        nonlocal raised_exception
        
        handler_1_called += 1
        vampytest.assert_eq(external_event, external_event_1)
        raise raised_exception
    
    
    handlers_mock = {
        external_event_0.event_type: handler_0,
        external_event_1.event_type: handler_1,
    }
    
    client_id = 202411270004
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    captured_errors = []
    
    async def error_handler_mock(client, location, error):
        nonlocal captured_errors
        captured_errors.append((client, location, error))
    
    client.events.error = error_handler_mock
    
    
    mocked = vampytest.mock_globals(
        loop_step,
        pull_external_events = pull_external_events_mock,
        remove_external_events = remove_external_events_mock,
        MAIN_CLIENT = client,
        HANDLERS = handlers_mock,
    )
    
    try:
        await mocked()
        await skip_ready_cycle()
        
        vampytest.assert_eq(pull_step, 1)
        vampytest.assert_eq(remove_step, 1)
        vampytest.assert_eq(handler_0_called, 1)
        vampytest.assert_eq(handler_1_called, 1)
        vampytest.assert_eq(captured_errors, [(client, 'loop_step', raised_exception)])
        
    finally:
        client._delete()
        client = None
