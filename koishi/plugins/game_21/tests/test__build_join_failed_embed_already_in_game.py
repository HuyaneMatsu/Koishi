import vampytest

from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..rendering import build_join_failed_embed_already_in_game


def _iter_options():
    yield (
        Embed(
            'Ohoho',
            'You are already in a game.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_failed_embed_already_in_game():
    """
    Tests whether ``build_join_failed_embed_already_in_game`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_join_failed_embed_already_in_game()
    vampytest.assert_instance(output, Embed)
    return output
