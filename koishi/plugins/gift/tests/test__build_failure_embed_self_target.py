import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..embed_builders import build_failure_embed_self_target


def _iter_options():
    yield (
        Embed(
            'Cannot gift to user',
            'You cannot gift hearts to yourself, my little lonely potato.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_self_target():
    """
    Tests whether ``build_failure_embed_self_target`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_self_target()
    vampytest.assert_instance(output, Embed)
    return output
