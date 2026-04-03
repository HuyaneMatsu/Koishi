from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..embed_builder_satori import render_nullable_date_time_into

from .helpers import DateTimeMock, is_instance_mock


def _iter_options__render_nullable_date_time_into():
    yield (
        DateTime(2016, 10, 14, 21, 13, 16, tzinfo = TimeZone.utc),
        DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
        '2016-10-14 21:13:16 [*10 seconds ago*]',
    )
    
    yield (
        None,
        DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
        'null',
    )


@vampytest._(vampytest.call_from(_iter_options__render_nullable_date_time_into()).returning_last())
def test__render_nullable_date_time_into(input_value, current_date_time):
    """
    Tests whether ``render_nullable_date_time_into`` works as intended.
    
    Parameters
    ----------
    input_value : `None | DateTime`
        The value to render.
    
    current_date_time : `DateTime`
        The current date time. Used for mocking.
    
    Returns
    -------
    output : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_nullable_date_time_into, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into = mocked([], input_value)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
