from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Activity, ActivityChange, ActivityUpdate, Status, StatusByPlatform, User

from ..embed_builder_satori import render_presence_update_into

from .helpers import DateTimeMock, is_instance_mock


def _iter_options():
    activity_0 = Activity('hello')
    activity_1 = Activity('lick')
    activity_2 = Activity('innit')
    added_activities = [activity_0]
    updated_activities = [ActivityUpdate(activity = activity_1, old_attributes = {'name': 'stare'})]
    removed_activities = [activity_2]
    
    user = User.precreate(
        202410160000,
        name = 'Flandre',
        status = Status.online,
        status_by_platform = StatusByPlatform(
            desktop = Status.idle,
            web = Status.online,
        ),
        activities = [activity_1, activity_2],
    )
    
    yield (
        user,
        {
            'status': Status.idle,
            'status_by_platform' : StatusByPlatform(
                desktop = Status.idle,
                web = Status.dnd,
            ),
            'activities': ActivityChange(
                added = added_activities,
                updated = updated_activities,
                removed = removed_activities,
            )
        },
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        (
            'User: Flandre (202410160000)\n'
            'At: 2016-05-14 00:00:00\n'
            '\n'
            '**Display status**\n'
            'idle -> online\n'
            '\n'
            '**Statuses by device**\n'
            'desktop: idle -> idle\n'
            'embedded: offline -> offline\n'
            'mobile: offline -> offline\n'
            'web: dnd -> online\n'
            '\n'
            '**Added activity**:\n'
            'Type: playing ~ 0\n'
            'Name: hello\n'
            '\n'
            '**Updated activity**:\n'
            'Name: \'stare\' -> \'lick\'\n'
            '\n'
            '**Removed activity**:\n'
            'Type: playing ~ 0\n'
            'Name: innit\n'
            '\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_presence_update_into(user, old_attributes, current_date_time):
    """
    Tests whether ``render_presence_update_into`` works as intended.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user in context.
    
    old_attributes : `dict<str, object>`
        The user's modified attributes.
    
    current_date_time : `DateTime`
        The current date time. Used for mocking.
    
    Returns
    -------
    output : `str`
    """
    DateTimeMock.set_current(current_date_time)
    mocked = vampytest.mock_globals(
        render_presence_update_into, 4, {'DateTime': DateTimeMock, 'isinstance': is_instance_mock}
    )
    into = mocked([], user, old_attributes)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
