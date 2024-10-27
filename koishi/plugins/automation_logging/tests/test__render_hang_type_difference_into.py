import vampytest
from hata import Activity, ActivityType, HangType

from ..embed_builder_satori import render_hang_type_difference_into


def _iter_options__render_hang_type_difference_into():
    old_type = HangType.gaming
    new_type = HangType.eating
    
    yield (
        old_type,
        Activity(activity_type = ActivityType.hanging, hang_type = new_type),
        f'Hang type: {old_type.name!s} ~ {old_type.value!r} -> {new_type.name!s} ~ {new_type.value!r}\n',
    )
    

@vampytest._(vampytest.call_from(_iter_options__render_hang_type_difference_into()).returning_last())
def test__render_hang_type_difference_into(old_value, activity):
    """
    Tests whether ``render_hang_type_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : ``HangType``
        The old value to render.
    
    activity : ``Activity``
        The updated activity.
    
    Returns
    -------
    output : `str`
    """
    into = render_hang_type_difference_into([], old_value, activity)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
