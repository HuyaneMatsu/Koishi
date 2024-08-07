import vampytest
from hata import Activity, ActivityType

from ..embed_builder_satori import render_type_difference_into


def test__render_type_difference_into():
    """
    Tests whether ``render_type_difference_into`` works as intended.
    """
    old_type = ActivityType.playing
    new_type = ActivityType.stream
    
    activity = Activity('mister', activity_type = new_type)
    
    output = render_type_difference_into([], old_type, activity)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    result = ''.join(output)
    vampytest.assert_eq(
        result,
        f'Type: {old_type.name!s} ~ {old_type.value!r} -> {new_type.name!s} ~ {new_type.value!r}\n',
    )
