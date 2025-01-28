import vampytest
from hata import Embed

from ..embed_builders import build_failure_embed_self_propose


def _iter_options():
    yield (
        Embed(
            'Self targeting not allowed',
            (
                'You cannot propose to yourself.'
            ),
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_self_propose():
    """
    Tests whether ``build_failure_embed_self_propose`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_self_propose()
    vampytest.assert_instance(output, Embed)
    return output
