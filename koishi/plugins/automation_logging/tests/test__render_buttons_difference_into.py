import vampytest
from hata import Activity, ActivityType

from ..embed_builder_satori import render_buttons_difference_into


def _iter_options__render_buttons_difference_into():
    yield (
        ('hey', 'sister'),
        Activity(activity_type = ActivityType.playing, buttons = ('good', 'morning')),
        f'Buttons: \'hey\', \'sister\' -> \'good\', \'morning\'\n',
    )
    
    yield (
        ('hey', 'sister'),
        Activity(activity_type = ActivityType.playing),
        f'Buttons: \'hey\', \'sister\' -> *none*\n',
    )
    yield (
        None,
        Activity(activity_type = ActivityType.playing, buttons = ('good', 'morning')),
        f'Buttons: *none* -> \'good\', \'morning\'\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_buttons_difference_into()).returning_last())
def test__render_buttons_difference_into(old_value, activity):
    """
    Tests whether ``render_buttons_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `None | tuple<str>`
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_buttons_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
