import vampytest
from hata import Embed

from ..embed_builders import build_failure_embed_no_item_like 


def _iter_options():
    yield (
        'pudding',
        Embed(
            'Oh no',
            'Could not discard pudding, you do not have such an item.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_no_item_like(value):
    """
    Tests whether ``build_failure_embed_no_item_like`` works as intended.
    
    Parameters
    ----------
    value : `str`
        The item's name to select.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_no_item_like(value)
    vampytest.assert_instance(output, Embed)
    return output
