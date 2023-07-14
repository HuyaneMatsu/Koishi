import vampytest

from ..parsers_description import render_description_into


def _iter_options():
    yield False, None, ('', False)
    yield False, '', ('', False)
    yield False, 'Satori', ('Satori', True)
    yield False, '\nSatori', ('\nSatori', True)
    yield False, '__Koishi__\nSatori', ('**Koishi**\nSatori', True)
    yield False, '\n__Koishi__\nSatori', ('\n**Koishi**\nSatori', True)
    
    yield True, None, ('', True)
    yield True, '', ('', True)
    yield True, 'Satori', ('\n\nSatori', True)
    yield True, '\nSatori', ('\n\nSatori', True)
    yield True, '__Koishi__\nSatori', ('\n**Koishi**\nSatori', True)
    yield True, '\n__Koishi__\nSatori', ('\n**Koishi**\nSatori', True)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_description_into(field_added, description):
    """
    Tests whether ``render_description_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether any fields were already added.
    description : `null | str`
        Description value.
    
    Returns
    -------
    content : `str`
        The rendered content.
    field_added : `bool`
        Whether any fields were already added.
    """
    into, field_added = render_description_into([], field_added, description)
    return ''.join(into), field_added
