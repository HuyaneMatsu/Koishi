import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..embed_builders import build_failure_embed_invalid_amount


def _iter_options():
    yield (
        Embed(
            'Invalid gift amount',
            'Cannot gift non-positive amount of hearts. >:3',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_invalid_amount():
    """
    Tests whether ``build_failure_embed_invalid_amount`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_invalid_amount()
    vampytest.assert_instance(output, Embed)
    return output
