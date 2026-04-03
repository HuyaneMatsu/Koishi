import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..embed_builders import build_failure_embed_no_balance


def _iter_options():
    yield (
        True,
        Embed(
            'Not enough hearts',
            'Like a flower...\nWhithering to the dust.',
            color = COLOR__GAMBLING,
        ),
    )
    
    yield (
        False,
        Embed(
            'Not enough hearts',
            'You do not have any hearts to gift.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_no_balance(with_allocated):
    """
    Tests whether ``build_failure_embed_no_balance`` works as intended.
    
    Parameters
    ----------
    with_allocated : `bool`
        Whether the allocated balance amount is already calculated in.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_no_balance(with_allocated)
    vampytest.assert_instance(output, Embed)
    return output
