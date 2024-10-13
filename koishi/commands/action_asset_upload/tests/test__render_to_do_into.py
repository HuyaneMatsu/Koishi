import vampytest

from ..rendering import _render_to_do_into


def _iter_options():
    yield (
        'sister',
        None,
        (
            '# TODO\n'
        ),
    )
    
    yield (
        {'hey', 'mister'},
        (
            '# TODO hey mister\n'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def _render_to_do_into(unidentified):
    """
    Tests whether ``_render_to_do_into`` works as intended.
    
    Parameters
    ----------
    unidentified : `None | set<str>`
        Unidentified name parts.
    
    Returns
    -------
    output : `str`
    """
    into = _render_to_do_into([], unidentified)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
