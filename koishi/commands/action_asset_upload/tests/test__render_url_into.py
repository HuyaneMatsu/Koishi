import vampytest

from ..rendering import _render_url_into


def _iter_options():
    yield (
        'https://orindance.party/miau',
        (
            'TOUHOU_ACTION_ALL.add(\n'
            '    \'https://orindance.party/miau\',\n'
            ')'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_url_into(url):
    """
    Tests whether ``_render_url_into`` works as intended.
    
    Parameters
    ----------
    url : `str`
        The to render.
    
    Returns
    -------
    output : `str`
    """
    into = _render_url_into([], url)
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    return ''.join(into)
