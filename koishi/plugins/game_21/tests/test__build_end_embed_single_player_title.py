import vampytest

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..rendering import build_end_embed_single_player_title


def _iter_options():
    yield (
        1,
        1000,
        f'How to win {1000!s} {EMOJI__HEART_CURRENCY}',
    )
    
    yield (
        -1,
        1000,
        f'How to lose {1000!s} {EMOJI__HEART_CURRENCY}',
    )
    
    yield (
        0,
        1000,
        f'How to draw',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_end_embed_single_player_title(player_win, amount):
    """
    Tests whether ``build_end_embed_single_player_title`` works as intended.
    
    ----------
    player_win : `int`
        Whether the player won.
    amount : `int`
        The amount lost or won.
    
    Returns
    -------
    output : `str`
    """
    output = build_end_embed_single_player_title(player_win, amount)
    vampytest.assert_instance(output, str)
    return output
