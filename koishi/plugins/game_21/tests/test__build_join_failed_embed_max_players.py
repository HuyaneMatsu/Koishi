import vampytest

from hata import Embed

from ....bot_utils.constants import COLOR__GAMBLING

from ..constants import PLAYERS_MAX
from ..rendering import build_join_failed_embed_max_players


def _iter_options():
    yield (
        Embed(
            'Ohoho',
            f'Max {PLAYERS_MAX!s} players are allowed.',
            color = COLOR__GAMBLING,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_join_failed_embed_max_players():
    """
    Tests whether ``build_join_failed_embed_max_players`` works as intended.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_join_failed_embed_max_players()
    vampytest.assert_instance(output, Embed)
    return output
