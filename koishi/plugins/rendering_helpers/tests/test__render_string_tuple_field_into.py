import vampytest

from ..field_renderers import render_string_tuple_field_into


def _iter_options():
    value_0 = 'Komeiji'
    value_1 = 'Koishi'
    
    yield False, None, False, 'Values', ('Values: *none*', True)
    yield True, None, False, 'Values', ('\nValues: *none*', True)
    
    yield (
        False, (value_0,), False, 'Values',
        (f'Values: {value_0!r}', True),
    )
    yield (
        True, (value_0,), False, 'Values',
        (f'\nValues: {value_0!r}', True),
    )
    yield False, None, True, 'Values', ('', False)
    yield True, None, True, 'Values', ('', True)
    yield (
        False, (value_0,), True, 'Values',
        (f'Values: {value_0!r}', True),
    )
    yield (
        True, (value_0,), True, 'Values',
        (f'\nValues: {value_0!r}', True),
    )
    
    # 2 values
    yield (
        False, (value_0, value_1), True, 'Values',
        (f'Values: {value_0!r}, {value_1!r}', True),
    )
    
    # title
    yield (
        False, (value_0,), True, 'Mister',
        (f'Mister: {value_0!r}', True),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_string_tuple_field_into(field_added, string_tuple, optional, title):
    """
    Tests whether ``render_string_tuple_field_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether a field was already added.
    
    string_tuple : `None | tuple<str>`
        The string tuple to render.
    
    title : `str`
        The title to use.
    
    Returns
    -------
    output : `str`
    field_added : `bool`
    """
    into, field_added = render_string_tuple_field_into(
        [], field_added, string_tuple, optional = optional, title = title
    ) 
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into), field_added
