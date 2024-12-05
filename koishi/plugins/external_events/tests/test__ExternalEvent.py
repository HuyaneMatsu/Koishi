from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import from_json, to_json

from ..external_event import ExternalEvent


def _assert_fields_set(external_event):
    """
    Asserts whether every field of the given external event are set.
    
    Parameters
    ----------
    external_event : ``ExternalEvent``
        The external event to test.
    """
    vampytest.assert_instance(external_event, ExternalEvent)
    vampytest.assert_instance(external_event.client_id, int)
    vampytest.assert_instance(external_event.entry_id, int)
    vampytest.assert_instance(external_event.event_data, object)
    vampytest.assert_instance(external_event.event_type, int)
    vampytest.assert_instance(external_event.guild_id, int)
    vampytest.assert_instance(external_event.trigger_after, DateTime, nullable = True)
    vampytest.assert_instance(external_event.user_id, int)


def test__ExternalEvent__new__no_fields():
    """
    Tests whether ``ExternalEvent.__new__`` works as intended.
    
    Case: no fields given.
    """
    external_event = ExternalEvent()
    _assert_fields_set(external_event)


def test__ExternalEvent__new__all_fields():
    """
    Tests whether ``ExternalEvent.__new__`` works as intended.
    
    Case: all fields given.
    """
    client_id = 202411260000
    event_data = {'source': 'kokoro'}
    event_type = 2
    guild_id = 202412040000
    trigger_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202411260001
    
    external_event = ExternalEvent(
        client_id = client_id,
        event_data = event_data,
        event_type = event_type,
        guild_id = guild_id,
        trigger_after = trigger_after,
        user_id = user_id,
    )
    _assert_fields_set(external_event)
    
    vampytest.assert_eq(external_event.client_id, client_id)
    vampytest.assert_eq(external_event.event_data, event_data)
    vampytest.assert_eq(external_event.event_type, event_type)
    vampytest.assert_eq(external_event.guild_id, guild_id)
    vampytest.assert_eq(external_event.trigger_after, trigger_after)
    vampytest.assert_eq(external_event.user_id, user_id)
    

def test__ExternalEvent__new__from_entry():
    """
    Tests whether ``ExternalEvent.from_entry`` works as intended.
    """
    client_id = 202411260002
    entry_id = 56
    event_data = {'source': 'kokoro'}
    event_type = 2
    guild_id = 202412040001
    trigger_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202411260003
    
    entry = {
        'client_id': client_id,
        'id': entry_id,
        'event_data': to_json(event_data),
        'event_type': event_type,
        'guild_id': guild_id,
        'trigger_after': trigger_after,
        'user_id': user_id,
    }
    
    external_event = ExternalEvent.from_entry(entry)
    _assert_fields_set(external_event)
    
    vampytest.assert_eq(external_event.client_id, client_id)
    vampytest.assert_eq(external_event.entry_id, entry_id)
    vampytest.assert_eq(external_event.event_data, event_data)
    vampytest.assert_eq(external_event.event_type, event_type)
    vampytest.assert_eq(external_event.guild_id, guild_id)
    vampytest.assert_eq(external_event.trigger_after, trigger_after)
    vampytest.assert_eq(external_event.user_id, user_id)
    

def test__ExternalEvent__repr():
    """
    Tests whether ``ExternalEvent.__repr__`` works as intended.
    """
    client_id = 202411260004
    event_data = {'source': 'kokoro'}
    event_type = 2
    guild_id = 202412040002
    trigger_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202411260005
    
    external_event = ExternalEvent(
        client_id = client_id,
        event_data = event_data,
        event_type = event_type,
        guild_id = guild_id,
        trigger_after = trigger_after,
        user_id = user_id,
    )
    
    output = repr(external_event)
    vampytest.assert_instance(output, str)
    vampytest.assert_in(type(external_event).__name__, output)


def _iter_options__eq():
    client_id = 202411260006
    event_data = {'source': 'kokoro'}
    event_type = 2
    guild_id = 202412040003
    trigger_after = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    user_id = 202411260007
    
    keyword_parameters = {
        'client_id': client_id,
        'event_data': event_data,
        'event_type': event_type,
        'guild_id': guild_id,
        'trigger_after': trigger_after,
        'user_id': user_id,
    }
    
    yield (
        keyword_parameters,
        keyword_parameters,
        True,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'client_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'event_data': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'event_type': 1,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'guild_id': 0,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'trigger_after': None,
        },
        False,
    )
    
    yield (
        keyword_parameters,
        {
            **keyword_parameters,
            'user_id': 0,
        },
        False,
    )


@vampytest._(vampytest.call_from(_iter_options__eq()).returning_last())
def test__ExternalEvent__eq(keyword_parameters_0, keyword_parameters_1):
    """
    Tests whether ``ExternalEvent.__eq__`` works as intended.
    
    Parameters
    ----------
    keyword_parameters_0 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    keyword_parameters_1 : `dict<str, object>`
        Keyword parameters to create instance with.
    
    Returns
    -------
    output : `bool`
    """
    external_event_0 = ExternalEvent(**keyword_parameters_0)
    external_event_1 = ExternalEvent(**keyword_parameters_1)
    
    output = external_event_0 == external_event_1
    vampytest.assert_instance(output, bool)
    return output
