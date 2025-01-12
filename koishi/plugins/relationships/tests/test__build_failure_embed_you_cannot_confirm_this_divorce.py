import vampytest
from hata import Embed

from ..embed_builders import build_failure_embed_you_cannot_confirm_this_divorce


def _iter_options():
    yield (
        Embed(
            'Divorcing cannot be confirmed',
            'You are not part of this engagement, so you cannot confirm it.',
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_you_cannot_confirm_this_divorce():
    """
    Tests whether ``build_failure_embed_you_cannot_confirm_this_divorce`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_you_cannot_confirm_this_divorce()
    vampytest.assert_instance(output, Embed)
    return output
