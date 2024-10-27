import vampytest

from ..embed_builder_satori import render_representation_difference_into


def _iter_options__render_representation_difference_into():
    yield (
        1,
        2,
        '1 -> 2\n',
    )
    
    yield (
        None,
        None,
        'null -> null\n',
    )
    
    yield (
        None,
        1,
        'null -> 1\n',
    )
    
    yield (
        1,
        None,
        '1 -> null\n',
    )


@vampytest._(vampytest.call_from(_iter_options__render_representation_difference_into()).returning_last())
def test__render_representation_difference_into(old_value, new_value):
    """
    Tests whether ``render_representation_difference_into`` works as intended.
    
    Parameters
    ----------
    old_value : `object`
        The old value to render.
    
    new_value : `object`
        The new value to render.
    
    Returns
    -------
    output : `str`
    """
    into = render_representation_difference_into([], old_value, new_value)
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
