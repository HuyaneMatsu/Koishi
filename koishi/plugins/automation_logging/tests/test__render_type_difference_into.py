import vampytest
from hata import Activity, ActivityType

from ..embed_builder_satori import render_type_difference_into


def _iter_options__render_type_difference_into():
    old_type = ActivityType.playing
    new_type = ActivityType.stream
    
    yield (
        old_type,
        Activity(activity_type = new_type),
        f'Type: {old_type.name!s} ~ {old_type.value!r} -> {new_type.name!s} ~ {new_type.value!r}\n',
    )
    

@vampytest._(vampytest.call_from(_iter_options__render_type_difference_into()).returning_last())
def test__render_type_difference_into(old_value, activity):
    """
    Tests whether ``render_type_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : ``ActivityType``
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_type_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
