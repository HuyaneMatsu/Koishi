import vampytest
from hata import InteractionEvent, User

from ..helpers import get_love_distribution
from ..player import Player


def _iter_options():
    player_0 = Player(User.precreate(202408040034), -1, InteractionEvent.precreate(202408040035))
    player_1 = Player(User.precreate(202408040036), 1, InteractionEvent.precreate(202408040037))
    player_2 = Player(User.precreate(202408040034), 2, InteractionEvent.precreate(202408040035))
    player_3 = Player(User.precreate(202408040036), 3, InteractionEvent.precreate(202408040037))
    
    
    yield (
        None,
        [player_0, player_1, player_2, player_3],
        1000,
        [
            (1, 1000, 0.0, True), 
            (2, 1000, 0.0, True),
            (3, 1000, 0.0, True),
        ],
    )
    
    yield (
        None,
        [player_0, player_1, player_2, player_3],
        1000,
        [
            (1, 1000, 0.0, True), 
            (2, 1000, 0.0, True),
            (3, 1000, 0.0, True),
        ],
    )

    yield (
        [player_0, player_1],
        [player_2, player_3],
        1000,
        [
            (1, 1000,  1.0, True), 
            (2, 1000, -1.0, True),
            (3, 1000, -1.0, True),
        ],
    )

    yield (
        [player_1],
        [player_0, player_2, player_3],
        1000,
        [
            (1, 1000,  3.0, True), 
            (2, 1000, -1.0, True),
            (3, 1000, -1.0, True),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_love_distribution(winners, losers, amount):
    """
    Tests whether ``get_love_distribution`` works as intended.
    
    Parameters
    ----------
    winners : `None | list<Player>`
        The winning players.
    losers : `None | list<Player>`
        The losing players.
    amount : `int`
        The bet amount.
    
    Returns
    -------
    output : `list<(int, int, int, bool)>`
    """
    output = get_love_distribution(winners, losers, amount)
    vampytest.assert_instance(output, list)
    return output
