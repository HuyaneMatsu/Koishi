__all__ = ()

from datetime import timedelta as TimeDelta

import vampytest
from hata import Client, Message
from scarletio import LOOP_TIME, TimerHandle

from ..constants import EVENT_MODE_HEART
from ..session import Session


def _assert_fields_set(session):
    """
    Asserts whether all fields of the given session are set.
    
    Parameters
    ----------
    session : ``Session``
        The instance to check.
    """
    vampytest.assert_instance(session, Session)
    vampytest.assert_instance(session.amount, int)
    vampytest.assert_instance(session.client, Client)
    vampytest.assert_instance(session.ends_at_loop_time, float)
    vampytest.assert_instance(session.event_mode, int)
    vampytest.assert_instance(session.message, Message)
    vampytest.assert_instance(session.update_handle, TimerHandle, nullable = True)
    vampytest.assert_instance(session.user_ids, set, nullable = True)
    vampytest.assert_instance(session.user_limit, int)


def test__Session__new():
    """
    Tests whether ``Session.__new__`` works as intended.
    """
    client_id = 2302511150000
    message_id = 2302511150001
    channel_id = 2302511150002
    
    event_mode = EVENT_MODE_HEART
    duration = TimeDelta(days = 1)
    amount = 100
    user_limit = 333
    
    client = Client(
        f'token_{client_id:x}',
        client_id = client_id,
    )
    
    try:
        message = Message.precreate(
            message_id,
            channel_id = channel_id,
        )
        
        session = Session(
            client,
            message,
            event_mode,
            duration,
            amount,
            user_limit,
        )
        
        _assert_fields_set(session)
        
        vampytest.assert_eq(session.amount, amount)
        vampytest.assert_is(session.client, client)
        vampytest.assert_true(session.ends_at_loop_time > LOOP_TIME())
        vampytest.assert_eq(session.event_mode, event_mode)
        vampytest.assert_is(session.message, message)
        vampytest.assert_is(session.update_handle, None)
        vampytest.assert_is(session.user_ids, None)
        vampytest.assert_eq(session.user_limit, user_limit)
        
    finally:
        client._delete()
        client = None


def test__Session__repr():
    """
    Tests whether ``Session.__repr__`` works as intended.
    """
    client_id = 2302511150003
    message_id = 2302511150004
    channel_id = 2302511150005
    
    event_mode = EVENT_MODE_HEART
    duration = TimeDelta(days = 1)
    amount = 100
    user_limit = 333
    
    client = Client(
        f'token_{client_id:x}',
        client_id = client_id,
    )
    
    try:
        message = Message.precreate(
            message_id,
            channel_id = channel_id,
        )
        
        session = Session(
            client,
            message,
            event_mode,
            duration,
            amount,
            user_limit,
        )
        
        output = repr(session)
        vampytest.assert_instance(output, str)
        
    finally:
        client._delete()
        client = None
