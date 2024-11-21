import vampytest
from hata import Activity, ActivityFlag, ActivityType

from ..embed_builder_satori import render_flags_difference_into


def _iter_options__render_flags_difference_into():
    yield (
        ActivityFlag().update_by_keys(sync = True, play = True),
        Activity(
            activity_type = ActivityType.playing,
            flags = ActivityFlag().update_by_keys(join = True, spectate = True),
        ),
        'Flags: play, sync -> join, spectate\n',
    )
    
    yield (
        ActivityFlag().update_by_keys(sync = True, play = True),
        Activity(activity_type = ActivityType.playing),
        'Flags: play, sync -> *none*\n',
    )
    yield (
        ActivityFlag(),
        Activity(
            activity_type = ActivityType.playing,
            flags = ActivityFlag().update_by_keys(join = True, spectate = True),
        ),
        'Flags: *none* -> join, spectate\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_flags_difference_into()).returning_last())
def test__render_flags_difference_into(old_value, activity):
    """
    Tests whether ``render_flags_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `ActivityFlag`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_flags_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
