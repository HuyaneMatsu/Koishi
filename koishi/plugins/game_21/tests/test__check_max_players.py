import vampytest

from hata import InteractionEvent, User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_max_players
from ..constants import PLAYERS_MAX
from ..player import Player


def _iter_options():
    player = Player(User.precreate(202408040060), -1, InteractionEvent.precreate(202408040061))
    
    yield (
        [player for index in range(PLAYERS_MAX - 1)],
        False,
    )

    yield (
        [player for index in range(PLAYERS_MAX)],
        True,
    )

    yield (
        [player for index in range(PLAYERS_MAX + 1)],
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_max_players(players):
    """
    Tests whether ``check_max_players`` works as intended.
    
    Parameters
    ----------
    players : `list<Player>`
        A game's players.
    
    Returns
    -------
    aborted : `bool`
    """
    try:
        check_max_players(players)
    except InteractionAbortedError:
        return True
    
    return False
