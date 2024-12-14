import vampytest
from hata import Embed, InteractionEvent, User


from ....bot_utils.constants import COLOR__GAMBLING

from ..player import Player
from ..rendering import build_end_embed_single_player
from ..session import Session


def _iter_options():
    session = Session(None, 1000, InteractionEvent.precreate(202408040050))
    player_user = Player(User.precreate(202408040051, name = 'Remilia'), InteractionEvent.precreate(202408040052))
    player_bot = Player(User.precreate(202408040053, name = 'Chiruno'), InteractionEvent.precreate(202408040054))
    player_win = 0
    
    
    yield (
        session,
        player_user,
        player_bot,
        player_win,
        Embed(
            'How to draw',
            color = COLOR__GAMBLING,
        ).add_field(
            (
                'Remilia\'s\n'
                'cards\' weight: 0'
            ),
            '_ _',
            inline = True,
        ).add_field(
            (
                'Chiruno\'s\n'
                'cards\' weight: 0'
            ),
            '_ _',
            inline = True,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_end_embed_single_player(session, player_user, player_bot, player_win):
    """
    Tests whether ``build_end_embed_single_player`` works as intended.
    
    Parameters
    ----------
    session : ``Session``
        Game session.
    player_user : ``Player``
        The user's player.
    player_bot : ``Player``
        Bot player.
    player_win : `int`
        Whether the player won.
    
    Returns
    -------
    output : ``Embed``
    """
    output = build_end_embed_single_player(session, player_user, player_bot, player_win)
    vampytest.assert_instance(output, Embed)
    return output
