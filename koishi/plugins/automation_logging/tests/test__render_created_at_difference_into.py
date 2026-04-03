from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Activity, ActivityType

from .helpers import DateTimeMock, is_instance_mock

from ..embed_builder_satori import render_created_at_difference_into


def _iter_options__render_created_at_difference_into():
    yield (
        DateTime(2016, 10, 14, 21, 13, 16, tzinfo = TimeZone.utc),
        Activity(activity_type = ActivityType.playing),
        DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
        'Created at: 2016-10-14 21:13:16 [*10 seconds ago*] -> null\n',
    )
    yield (
        None,
        Activity(
            activity_type = ActivityType.playing,
            created_at = DateTime(2016, 10, 14, 21, 13, 16, tzinfo = TimeZone.utc),
        ),
        DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
        'Created at: null -> 2016-10-14 21:13:16 [*10 seconds ago*]\n',
    )
    yield (
        DateTime(2016, 10, 14, 21, 13, 17, tzinfo = TimeZone.utc),
        Activity(
            activity_type = ActivityType.playing,
            created_at = DateTime(2016, 10, 14, 21, 13, 16, tzinfo = TimeZone.utc),
        ),
        DateTime(2016, 10, 14, 21, 13, 26, tzinfo = TimeZone.utc),
        'Created at: 2016-10-14 21:13:17 [*9 seconds ago*] -> 2016-10-14 21:13:16 [*10 seconds ago*]\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_created_at_difference_into()).returning_last())
def test__render_created_at_difference_into(old_value, activity, current_date_time):
    """
    Tests whether ``render_created_at_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `None | DateTime`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_created_at_difference_into, 5, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    
    into = mocked([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
