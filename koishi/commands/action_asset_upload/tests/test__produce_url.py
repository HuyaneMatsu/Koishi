import vampytest

from ..rendering import _produce_url


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
def test__produce_url(url):
    """
    Tests whether ``_produce_url`` works as intended.
    
    Parameters
    ----------
    url : `str`
        The to render.
    
    Returns
    -------
    output : `str`
    """
    output = [*_produce_url(url)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
