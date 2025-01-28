import vampytest
from hata import Embed

from ..embed_builders import build_success_embed_purchase_cancelled


def _iter_options():
    yield (
        Embed(
            'Purchase cancelled',
            'The relationship slot purchase has been cancelled.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_success_embed_purchase_cancelled():
    """
    Tests whether ``build_success_embed_purchase_cancelled`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_success_embed_purchase_cancelled()
    vampytest.assert_instance(output, Embed)
    return output
