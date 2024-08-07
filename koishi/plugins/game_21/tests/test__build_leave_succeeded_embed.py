import vampytest

from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..rendering import build_leave_succeeded_embed


def _iter_options():
    yield (
        Embed(
            '21 multi-player game left.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_leave_succeeded_embed():
    """
    Tests whether ``build_leave_succeeded_embed`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_leave_succeeded_embed()
    vampytest.assert_instance(output, Embed)
    return output
