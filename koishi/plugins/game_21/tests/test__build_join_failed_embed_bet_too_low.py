import vampytest

from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING, EMOJI__HEART_CURRENCY

from ..constants import BET_MIN
from ..rendering import build_join_failed_embed_bet_too_low


def _iter_options():
    yield (
        Embed(
            'Ohoho',
            f'You must bet at least {BET_MIN!s} {EMOJI__HEART_CURRENCY}',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_failed_embed_bet_too_low():
    """
    Tests whether ``build_join_failed_embed_bet_too_low`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_join_failed_embed_bet_too_low()
    vampytest.assert_instance(output, Embed)
    return output
