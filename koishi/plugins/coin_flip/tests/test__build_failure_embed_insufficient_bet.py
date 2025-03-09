import vampytest
from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..constants import BET_MIN
from ..embed_builders import build_failure_embed_insufficient_bet


def _iter_options():
    yield (
        Embed(
            'Insufficient bet',
            f'You must be at least {BET_MIN} {EMOJI__HEART_CURRENCY}.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_failure_embed_insufficient_bet():
    """
    Tests whether ``build_failure_embed_insufficient_bet`` works as intend.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_failure_embed_insufficient_bet()
    vampytest.assert_instance(output, Embed)
    return output
