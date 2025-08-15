import vampytest
from hata import Embed

from ..embed_builders import build_failure_embed_cannot_discard_less_than_one 


def _iter_options():
    yield (
        Embed(
            'Oh no',
            f'You cannot discard less than 1 items.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_cannot_discard_less_than_one():
    """
    Tests whether ``build_failure_embed_cannot_discard_less_than_one`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_cannot_discard_less_than_one()
    vampytest.assert_instance(output, Embed)
    return output
