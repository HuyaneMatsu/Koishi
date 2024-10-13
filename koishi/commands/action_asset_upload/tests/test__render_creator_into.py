import vampytest

from ..rendering import _render_creator_into


def _iter_options():
    yield (
        'sister',
        None,
        (
            '.with_creator(\n'
            '    \'sister\',\n'
            ')'
        ),
    )
    
    yield (
        None,
        (
            ''
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def _render_creator_into(creator):
    """
    Tests whether ``_render_creator_into`` works as intended.
    
    Parameters
    ----------
    creator : `None | str`
        Image creator.
    
    Returns
    -------
    output : `str`
    """
    into = _render_creator_into([], creator)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
