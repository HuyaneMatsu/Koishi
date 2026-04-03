import vampytest
from hata import Activity, ActivityType

from ..embed_builder_satori import render_details_difference_into


def _iter_options__render_details_difference_into():
    yield (
        'Murasa',
        Activity(activity_type = ActivityType.playing, details = 'Kogasa'),
        'Details: \'Murasa\' -> \'Kogasa\'\n',
    )
    
    yield (
        'Murasa',
        Activity(activity_type = ActivityType.playing),
        'Details: \'Murasa\' -> null\n',
    )
    yield (
        None,
        Activity(activity_type = ActivityType.playing, details = 'Kogasa'),
        'Details: null -> \'Kogasa\'\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_details_difference_into()).returning_last())
def test__render_details_difference_into(old_value, activity):
    """
    Tests whether ``render_details_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `None | str`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_details_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
