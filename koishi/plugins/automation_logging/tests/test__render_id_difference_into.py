import vampytest
from hata import Activity, ActivityType

from ..embed_builder_satori import render_id_difference_into


def _iter_options__render_id_difference_into():
    yield (
        202410150000,
        Activity(activity_type = ActivityType.playing, activity_id = 202410150001),
        'Id: 202410150000 -> 202410150001\n',
    )
    
    yield (
        202410150002,
        Activity(activity_type = ActivityType.playing),
        'Id: 202410150002 -> 0\n',
    )
    yield (
        0,
        Activity(activity_type = ActivityType.playing, activity_id = 202410150003),
        'Id: 0 -> 202410150003\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_id_difference_into()).returning_last())
def test__render_id_difference_into(old_value, activity):
    """
    Tests whether ``render_id_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `int`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_id_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
