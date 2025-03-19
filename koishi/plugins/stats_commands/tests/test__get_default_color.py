import vampytest
from hata import Color

from ..embed_builders import get_default_color


def _iter_options():
    expected_output = 0x123425
    yield (
        (((5566 << 24) | expected_output) << 22) | 4555,
        Color(expected_output),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_default_color(user_id):
    """
    Tests whether ``get_default_color`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        A user's identifier.
    
    Returns
    -------
    output : ``Color``
    """
    output = get_default_color(user_id)
    vampytest.assert_instance(output, Color)
    return output
