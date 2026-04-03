import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..embed_builders import build_failure_embed_no_target_user


def _iter_options():
    yield (
        Embed(
            'Cannot gift to user',
            'Please select a target user to gift to.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_no_target_user():
    """
    Tests whether ``build_failure_embed_no_target_user`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_no_target_user()
    vampytest.assert_instance(output, Embed)
    return output
